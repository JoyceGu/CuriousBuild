#!/usr/bin/env python3
"""
用 Claude 把博客文章翻译成另一种语言（译文会顺带润色，原文不动）

用法（GitHub Action 每天同步 Notion 后运行，也可以本地跑）：
   python3 blog/scripts/ai_translate.py
   为 blog/markdown/ 里还没有另一种语言版本的文章生成润色过的译文，
   写成新的 markdown 文件（frontmatter 带 ai_translated: true）。
   原文没改就不会重复翻译；原文更新后译文会自动重新生成。
   人工写好的译文（在 translations.json 或 Translation Key 里配对的）永远不会被覆盖。
   原文本身不会被修改。

   --direction zh2en  只把中文翻成英文
   --direction both   中英互译（默认）
   --dry-run          只列出要翻译的文章，不调用 API

两种调用方式（环境变量 BLOG_AI_BACKEND 指定，不填时自动选择）：
   claude-code  用 Claude Code CLI，走你的 Claude 订阅额度，不需要 API key。
                本地登录过 Claude Code 即可；GitHub Action 里用 CLAUDE_CODE_OAUTH_TOKEN
                （本地运行 `claude setup-token` 生成）。没有 ANTHROPIC_API_KEY 时默认用它。
   api          用 Anthropic API，需要 ANTHROPIC_API_KEY。
文章 frontmatter 里写 `ai_translate: false` 可以让某篇文章不自动翻译。
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from simple_md_converter import SimpleBlogConverter

MODEL = os.getenv('BLOG_AI_MODEL', 'claude-sonnet-5-5')
BACKEND = os.getenv('BLOG_AI_BACKEND') or ('api' if os.getenv('ANTHROPIC_API_KEY') else 'claude-code')
LANG_NAMES = {'zh': 'Simplified Chinese', 'en': 'English'}

STYLE_GUIDE = """\
The author is Joyce, who writes a personal blog about technology, growth, careers and life, \
mostly as reading notes and reflections. Her voice is candid, warm and a little playful: \
she uses emoji, internet-style emoticons and the occasional English word inside Chinese sentences.

Formatting rules (always):
- Keep the Markdown structure exactly: headings, lists, bold/italic, blockquotes, line breaks between paragraphs.
- Keep every link URL, image and code block unchanged. Do not translate code.
- Do not add, remove or summarize content. Every paragraph in the input has a counterpart in the output.
- Quoted material (blockquotes, book excerpts) is translated faithfully, not rewritten.
- Output the article body only, without YAML frontmatter.
- Chinese text uses full-width Chinese punctuation (，。！？：；“”《》), with ASCII punctuation kept only inside code, URLs and English phrases.
"""

TRANSLATE_SYSTEM = STYLE_GUIDE + """
Task: translate the post into {target}. The translation should read as if Joyce had written it in \
{target} herself: natural and polished, keeping her tone, humor, emoji and opinions. Smooth out awkward \
phrasing rather than translating word for word. Mixed-language terms (for example "IC", "PM", "inspiring" \
inside Chinese text) should come out the way a native {target} writer would put them.

Also return:
- title: the post title in {target}
- summary: one or two plain-text sentences in {target} (no Markdown, under 160 characters) for the post list, written in Joyce's own first-person voice
- slug: {slug_rule}
"""

SLUG_RULES = {
    'en': 'a short URL slug in lowercase English words joined by hyphens, e.g. "hacking-growth-reading-notes"',
    'zh': 'a short URL slug for the Chinese version: a few Chinese characters, optionally with ASCII words and hyphens, no spaces or punctuation',
}

TRANSLATION_SCHEMA = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'summary': {'type': 'string'},
        'slug': {'type': 'string'},
        'body': {'type': 'string'},
    },
    'required': ['title', 'summary', 'slug', 'body'],
    'additionalProperties': False,
}

def other_lang(lang):
    return 'en' if lang == 'zh' else 'zh'


def source_hash(article):
    text = article['title'] + '\n' + article['markdown'].strip()
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def one_line(text):
    return ' '.join(str(text).split())


def clean_slug(slug, lang):
    slug = slug.strip().lower()
    if lang == 'en':
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    else:
        slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s_]+', '-', slug).strip('-')
    return slug[:80]


def call_claude(client, system, user_content, schema):
    if BACKEND == 'claude-code':
        return call_claude_code(system, user_content, schema)
    return call_claude_api(client, system, user_content, schema)


def call_claude_code(system, user_content, schema):
    """Run Claude Code headless (no tools) and read its schema-validated output"""
    cmd = [
        'claude', '-p',
        '--model', MODEL,
        '--output-format', 'json',
        '--json-schema', json.dumps(schema),
        '--system-prompt', system,
        '--tools', '',
        '--no-session-persistence',
    ]
    env = dict(os.environ, CLAUDE_CODE_MAX_OUTPUT_TOKENS='64000')
    proc = subprocess.run(cmd, input=user_content, capture_output=True, text=True,
                          timeout=900, env=env)
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError(f'Claude Code failed: {(proc.stderr or proc.stdout).strip()[:500]}')
    if data.get('is_error') or data.get('structured_output') is None:
        raise RuntimeError(f"Claude Code error: {str(data.get('result'))[:500]}")
    return data['structured_output']


def call_claude_api(client, system, user_content, schema):
    """Single structured-output request; streams so long articles don't hit HTTP timeouts"""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        betas=['server-side-fallback-2026-07-01'],
        fallbacks='default',
        output_config={
            'effort': 'high',
            'format': {'type': 'json_schema', 'schema': schema},
        },
        system=system,
        messages=[{'role': 'user', 'content': user_content}],
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == 'refusal':
        raise RuntimeError('Claude declined this request')
    if message.stop_reason == 'max_tokens':
        raise RuntimeError('Response was cut off (article too long for one request)')
    text = next((b.text for b in message.content if b.type == 'text'), None)
    if text is None:
        raise RuntimeError('No text in response')
    return json.loads(text)


def make_client():
    if BACKEND == 'claude-code':
        if not shutil.which('claude'):
            print('❌ 找不到 claude 命令，请先安装 Claude Code: npm install -g @anthropic-ai/claude-code')
            sys.exit(1)
        return None
    try:
        import anthropic
    except ImportError:
        print('❌ 需要先安装 SDK: pip install anthropic')
        sys.exit(1)
    return anthropic.Anthropic()


def frontmatter_value(md_path, key):
    converter = SimpleBlogConverter()
    with open(md_path, 'r', encoding='utf-8') as f:
        meta, _ = converter.parse_frontmatter(f.read())
    return meta.get(key)


def write_markdown(path, fields, body):
    lines = ['---'] + [f'{k}: {v}' for k, v in fields.items() if v not in (None, '')] + ['---', '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' + body.strip() + '\n')


def plan_translations(converter, direction):
    """Return (jobs, orphans): articles needing a translation, and stale AI translations to delete"""
    groups = converter.load_translation_groups()
    articles = []
    for md_path in sorted(converter.markdown_dir.glob('*.md')):
        article = converter.load_article(md_path, groups)
        article['path'] = md_path
        articles.append(article)

    by_key = {}
    for article in articles:
        by_key.setdefault(article['translation_key'], []).append(article)

    jobs, orphans = [], []
    for key, group in by_key.items():
        originals = [a for a in group if not a['ai_translated']]
        ai_copies = [a for a in group if a['ai_translated']]
        if not originals:
            orphans.extend(ai_copies)
            continue
        for original in originals:
            target = other_lang(original['lang'])
            if direction == 'zh2en' and original['lang'] != 'zh':
                continue
            if frontmatter_value(original['path'], 'ai_translate') == 'false':
                continue
            if any(a['lang'] == target for a in originals):
                continue  # 已有人工译文
            existing = next((a for a in ai_copies if a['lang'] == target), None)
            digest = source_hash(original)
            if existing and frontmatter_value(existing['path'], 'source_hash') == digest:
                continue  # 原文没变
            jobs.append((original, target, existing, digest))
    return jobs, orphans


def translate_article(client, converter, original, target, existing, digest):
    system = TRANSLATE_SYSTEM.format(target=LANG_NAMES[target], slug_rule=SLUG_RULES[target])
    user = f"Title: {original['title']}\n\n{original['markdown'].strip()}"
    result = call_claude(client, system, user, TRANSLATION_SCHEMA)

    if existing:
        out_path = existing['path']
        slug = out_path.stem
    else:
        slug = clean_slug(result['slug'], target) or f"{original['path'].stem}-{target}"
        taken = {p.stem for p in converter.markdown_dir.glob('*.md')}
        base, n = slug, 2
        while slug in taken:
            slug, n = f'{base}-{n}', n + 1
        out_path = converter.markdown_dir / f'{slug}.md'

    tags = ', '.join(original['tags']) if original['tags'] else ''
    write_markdown(out_path, {
        'title': one_line(result['title']),
        'date': original['date_iso'],
        'tags': tags,
        'summary': one_line(result['summary']),
        'filename': slug,
        'lang': target,
        'translation_key': original['translation_key'],
        'ai_translated': 'true',
        'source_file': original['path'].name,
        'source_hash': digest,
        # 和原文同一个 Notion 页面：原文在 Notion 下线时，同步脚本会一起删除译文
        'notion_page_id': frontmatter_value(original['path'], 'notion_page_id'),
    }, result['body'])
    return out_path


def run_translate(args):
    converter = SimpleBlogConverter()
    jobs, orphans = plan_translations(converter, args.direction)

    for orphan in orphans:
        print(f"🗑  原文已不存在，删除 AI 译文: {orphan['path'].name}")
        if not args.dry_run:
            orphan['path'].unlink(missing_ok=True)

    if not jobs:
        print('✅ 所有文章都已有对应语言版本，无需翻译')
        return 0

    for original, target, existing, _ in jobs:
        action = '更新' if existing else '新建'
        print(f"📝 待翻译（{action}）: {original['path'].name} [{original['lang']} → {target}]")
    if args.dry_run:
        return 0

    client = make_client()
    failures = 0
    for original, target, existing, digest in jobs:
        try:
            out_path = translate_article(client, converter, original, target, existing, digest)
            print(f"✅ 已生成: {out_path.name}")
        except Exception as e:
            failures += 1
            print(f"❌ 翻译失败 {original['path'].name}: {e}")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description='Translate blog posts with Claude')
    parser.add_argument('--direction', choices=['zh2en', 'both'],
                        default=os.getenv('BLOG_TRANSLATE_DIRECTION', 'both'))
    parser.add_argument('--dry-run', action='store_true')
    return run_translate(parser.parse_args())


if __name__ == '__main__':
    sys.exit(main())
