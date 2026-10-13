#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for Joyce's Blog
No external dependencies required - uses only Python standard library
"""

import os
import re
import json
import html
from urllib.parse import quote
from datetime import datetime
from pathlib import Path

class SimpleBlogConverter:
    def __init__(self):
        self.blog_dir = Path(__file__).parent.parent
        self.markdown_dir = self.blog_dir / "markdown"
        self.posts_dir = self.blog_dir / "posts"
        
        # Ensure directories exist
        self.posts_dir.mkdir(exist_ok=True)
        self.markdown_dir.mkdir(exist_ok=True)
        
    def parse_frontmatter(self, content):
        """Parse simple frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                lines = content.split('\n')
                frontmatter_lines = []
                content_lines = []
                in_frontmatter = True
                skip_first = True
                
                for line in lines:
                    if skip_first and line.strip() == '---':
                        skip_first = False
                        continue
                    if line.strip() == '---' and in_frontmatter:
                        in_frontmatter = False
                        continue
                    if in_frontmatter:
                        frontmatter_lines.append(line)
                    else:
                        content_lines.append(line)
                
                # Parse simple key: value pairs
                metadata = {}
                for line in frontmatter_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        if key == 'tags':
                            # Parse tags as comma-separated values
                            metadata[key] = [tag.strip() for tag in value.split(',')]
                        else:
                            metadata[key] = value
                
                return metadata, '\n'.join(content_lines)
            except:
                return {}, content
        return {}, content
    
    def simple_markdown_to_html(self, markdown_text):
        """Convert basic markdown to HTML using regex"""
        html = markdown_text
        
        # Headers
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Code blocks
        html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Blockquotes
        html = re.sub(r'^> (.*$)', r'<blockquote><p>\1</p></blockquote>', html, flags=re.MULTILINE)
        
        # Lists
        lines = html.split('\n')
        in_ul = False
        in_ol = False
        result_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Unordered lists
            if stripped.startswith('- '):
                if not in_ul:
                    result_lines.append('<ul>')
                    in_ul = True
                if in_ol:
                    result_lines.append('</ol>')
                    in_ol = False
                result_lines.append(f'<li>{stripped[2:]}</li>')
            # Ordered lists
            elif re.match(r'^\d+\. ', stripped):
                if not in_ol:
                    result_lines.append('<ol>')
                    in_ol = True
                if in_ul:
                    result_lines.append('</ul>')
                    in_ul = False
                content = re.sub(r'^\d+\. ', '', stripped)
                result_lines.append(f'<li>{content}</li>')
            else:
                if in_ul:
                    result_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    result_lines.append('</ol>')
                    in_ol = False
                result_lines.append(line)
        
        # Close any open lists
        if in_ul:
            result_lines.append('</ul>')
        if in_ol:
            result_lines.append('</ol>')
        
        html = '\n'.join(result_lines)
        
        # Paragraphs (simple approach)
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                html_paragraphs.append(f'<p>{para}</p>')
            elif para:
                html_paragraphs.append(para)
        
        return '\n\n'.join(html_paragraphs)
    
    CJK_RE = re.compile(r'[㐀-䶿一-鿿豈-﫿]')
    LATIN_WORD_RE = re.compile(r'[A-Za-z0-9]+(?:[\'’-][A-Za-z0-9]+)*')

    def detect_lang(self, text):
        """Guess 'zh' or 'en' from the share of Chinese characters"""
        cjk = len(self.CJK_RE.findall(text))
        words = len(self.LATIN_WORD_RE.findall(text))
        if cjk + words == 0:
            return 'en'
        return 'zh' if cjk / (cjk + words) > 0.3 else 'en'

    def calculate_reading_time(self, content):
        """Reading time: ~400 Chinese characters or ~200 English words per minute"""
        cjk = len(self.CJK_RE.findall(content))
        words = len(self.LATIN_WORD_RE.findall(content))
        return max(1, round(cjk / 400 + words / 200))

    def create_filename(self, title):
        """Create a URL-friendly filename from title"""
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return f"{filename}.html"

    def load_translation_groups(self):
        """
        blog/translations.json lists posts that are translations of each other,
        by markdown filename (without .md), e.g.
        {"groups": [["增长黑客阅读笔记", "hacking-growth-reading-notes"]]}
        Useful for pairs written by hand in Notion. Posts can also set
        `translation_key` in their frontmatter instead.
        """
        path = self.blog_dir / "translations.json"
        if not path.exists():
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            print(f"⚠️  Could not read translations.json: {e}")
            return {}
        mapping = {}
        for group in data.get('groups', []):
            if group:
                for stem in group:
                    mapping[stem] = group[0]
        return mapping

    def load_article(self, md_file_path, translation_groups):
        """Parse a markdown file into an article dict (no HTML written yet)"""
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata, markdown_content = self.parse_frontmatter(content)

        title = metadata.get('title', 'Untitled')
        date_str = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
        tags = metadata.get('tags', [])
        summary = metadata.get('summary', '')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            date_obj = datetime.now()

        filename = metadata.get('filename') or self.create_filename(title)
        if not filename.endswith('.html'):
            filename += '.html'

        lang = metadata.get('lang', '').lower()
        if lang not in ('zh', 'en'):
            lang = self.detect_lang(title + '\n' + markdown_content)

        stem = md_file_path.stem
        translation_key = (
            metadata.get('translation_key')
            or translation_groups.get(stem)
            or stem
        )

        if not summary:
            summary = f"{markdown_content[:150]}..." if len(markdown_content) > 150 else markdown_content

        return {
            'title': title,
            'filename': filename,
            'date_iso': date_obj.strftime('%Y-%m-%d'),
            'date_formatted': date_obj.strftime('%B %d, %Y'),
            'reading_time': self.calculate_reading_time(markdown_content),
            'tags': tags,
            'summary': summary,
            'lang': lang,
            'translation_key': translation_key,
            'ai_translated': metadata.get('ai_translated', '').lower() == 'true',
            'markdown': markdown_content,
            'source_name': md_file_path.name,
        }

    def render_article(self, article, translation):
        """Write the HTML page for one article; `translation` is the other-language version or None"""
        title = html.escape(article['title'])
        filename = article['filename']
        lang = article['lang']
        html_lang = 'zh-CN' if lang == 'zh' else 'en'
        html_content = self.simple_markdown_to_html(article['markdown'])
        post_url = f"https://joycegu.github.io/CuriousBuild/blog/posts/{quote(filename)}"

        tags_html = ""
        if article['tags']:
            tag_elements = [f'<span class="tag">{html.escape(tag)}</span>' for tag in article['tags']]
            tags_html = '\n                        '.join(tag_elements)

        alternate_links = f'<link rel="alternate" hreflang="{lang}" href="{quote(filename)}">'
        translation_html = ""
        if translation:
            other = translation['lang']
            alternate_links += f'\n    <link rel="alternate" hreflang="{other}" href="{quote(translation["filename"])}">'
            # Label is written in the target language so readers of that language can find it
            label = '阅读中文版 →' if other == 'zh' else 'Read in English →'
            translation_html = (
                f'<a class="translation-link" href="{quote(translation["filename"])}" '
                f'lang="{"zh-CN" if other == "zh" else "en"}">{label}</a>'
            )

        ai_note_html = ""
        if article['ai_translated']:
            ai_note_html = '<p class="ai-translation-note" data-i18n="post.aiTranslated">This version was translated with AI from the original article.</p>'

        html_template = f'''<!DOCTYPE html>
<html lang="{html_lang}" data-content-lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Joyce's Blog</title>
    {alternate_links}
    <link rel="stylesheet" href="../blog-styles.css">
    <link rel="stylesheet" href="../templates/article-styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="nav">
                <a href="../../" class="site-title" data-i18n="nav.backToPlayground">Back to Joyce's Playground</a>
                <div class="nav-links">
                    <a href="../" class="nav-link" data-i18n="nav.home">Home</a>
                    <a href="#archives" class="nav-link" data-i18n="nav.archives">Archives</a>
                    <a href="#tags" class="nav-link" data-i18n="nav.tags">Tags</a>
                    <span data-lang-toggle></span>
                </div>
            </div>
        </header>

        <!-- Article Content -->
        <main class="main">
            <article class="article">
                <!-- Article Header -->
                <header class="article-header">
                    <h1 class="article-title">{title}</h1>
                    <div class="article-meta">
                        <time datetime="{article['date_iso']}" data-i18n-date>{article['date_formatted']}</time>
                        <span class="reading-time" data-minutes="{article['reading_time']}">{article['reading_time']} min</span>
                        <span class="author">Joyce Gu</span>
                        {translation_html}
                    </div>
                    <div class="article-tags">
                        {tags_html}
                    </div>
                    {ai_note_html}
                </header>

                <!-- Article Content -->
                <div class="article-content">
                    {html_content}
                </div>

                <!-- Article Footer -->
                <footer class="article-footer">
                    <div class="article-navigation">
                        <a href="../" class="nav-prev" data-i18n="post.backToBlog">← Back to Blog</a>
                        <a href="#" class="nav-next" data-i18n="post.next">Next Article →</a>
                    </div>
                    
                    <div class="article-share">
                        <p data-i18n="post.share">Share this article:</p>
                        <div class="share-buttons">
                            <a href="https://twitter.com/intent/tweet?text={quote(article['title'])}&url={quote(post_url, safe='')}" class="share-button" target="_blank">Twitter</a>
                            <a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(post_url, safe='')}" class="share-button" target="_blank">LinkedIn</a>
                            <a href="#" class="share-button" data-i18n="post.copyLink" onclick="navigator.clipboard.writeText(window.location.href); alert(window.I18n ? I18n.t('post.copied') : 'Link copied to clipboard!'); return false;">Copy Link</a>
                        </div>
                    </div>
                </footer>
            </article>
        </main>
    </div>

    <script src="../../i18n.js"></script>
    <script src="../blog-script.js"></script>
</body>
</html>'''

        output_path = self.posts_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)

        print(f"✅ Converted: {article['source_name']} → {filename} [{lang}]")

    def find_translations(self, articles):
        """Map each article filename to its other-language version (or None)"""
        by_key = {}
        for article in articles:
            by_key.setdefault(article['translation_key'], []).append(article)
        result = {}
        for article in articles:
            others = [a for a in by_key[article['translation_key']]
                      if a is not article and a['lang'] != article['lang']]
            result[article['filename']] = others[0] if others else None
        return result

    def convert_all_markdown(self):
        """Convert all markdown files"""
        md_files = list(self.markdown_dir.glob('*.md'))
        if not md_files:
            print(f"📝 No markdown files found in {self.markdown_dir}")
            return []

        translation_groups = self.load_translation_groups()
        articles = []
        for md_file in sorted(md_files):
            try:
                articles.append(self.load_article(md_file, translation_groups))
            except Exception as e:
                print(f"❌ Error reading {md_file.name}: {e}")

        translations = self.find_translations(articles)
        active_html = set()
        for article in articles:
            translation = translations[article['filename']]
            article['has_translation'] = translation is not None
            try:
                self.render_article(article, translation)
                active_html.add(article['filename'])
            except Exception as e:
                print(f"❌ Error converting {article['source_name']}: {e}")

        for html_path in list(self.posts_dir.glob('*.html')):
            if html_path.name not in active_html:
                html_path.unlink(missing_ok=True)
                print(f"🗑 Removed orphan HTML: {html_path.name}")

        return [a for a in articles if a['filename'] in active_html]

    def update_blog_index(self, articles):
        """Update the blog index with articles"""
        if not articles:
            return

        # Sort articles by date (newest first)
        articles.sort(key=lambda x: x['date_iso'], reverse=True)

        # Each post is tagged with its language. When the UI is in one language,
        # blog-styles.css hides posts that also exist in that language and shows
        # a small badge on posts that are only available in the other one.
        articles_html = []
        for article in articles:
            badge_key = f"blog.onlyIn.{article['lang']}"
            badge_text = '中文' if article['lang'] == 'zh' else 'EN'
            article_html = f'''                <article class="post-item" lang="{'zh-CN' if article['lang'] == 'zh' else 'en'}" data-lang="{article['lang']}" data-has-translation="{'true' if article['has_translation'] else 'false'}">
                    <div class="post-content">
                        <h3 class="post-title">
                            <a href="posts/{quote(article['filename'])}">{html.escape(article['title'])}</a>
                            <span class="post-lang-badge" data-i18n="{badge_key}">{badge_text}</span>
                        </h3>
                        <p class="post-summary">{html.escape(article['summary'])}</p>
                    </div>
                    <div class="post-meta">
                        <time datetime="{article['date_iso']}" data-i18n-date>{article['date_formatted']}</time>
                        <span class="reading-time" data-minutes="{article['reading_time']}">{article['reading_time']} min</span>
                        <span class="author">Joyce Gu</span>
                    </div>
                </article>'''
            articles_html.append(article_html)

        # Read current blog index
        blog_index_path = self.blog_dir / "index.html"
        with open(blog_index_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Replace the posts section
        posts_section = '\n'.join(articles_html)
        new_posts_section = f'''            <!-- Posts List -->
            <section class="posts">
{posts_section}
            </section>'''

        # Update the blog index (lambda so backslashes in content aren't treated as escapes)
        pattern = r'<!-- Posts List -->.*?</section>'
        updated_content = re.sub(pattern, lambda _: new_posts_section, current_content, flags=re.DOTALL)

        with open(blog_index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"✅ Updated blog index with {len(articles)} articles")

        self.generate_search_index(articles)

        # RSS feeds: feed.xml has everything; feed-en.xml / feed-zh.xml follow the
        # post-list rule (each post once, in that language when available), which is
        # what email newsletters should read so subscribers don't get duplicates
        self.generate_rss_feed(articles)
        for lang in ('en', 'zh'):
            in_lang = [a for a in articles if a['lang'] == lang or not a['has_translation']]
            self.generate_rss_feed(in_lang, feed_name=f'feed-{lang}.xml', lang=lang)

    def generate_search_index(self, articles):
        """Write posts.json, which the blog's search box loads"""
        entries = []
        for article in articles:
            plain = re.sub(r'[#*`>\[\]()_~|-]', ' ', article['markdown'])
            entries.append({
                'title': article['title'],
                'summary': article['summary'],
                'date': article['date_iso'],
                'url': f"posts/{quote(article['filename'])}",
                'lang': article['lang'],
                'has_translation': article['has_translation'],
                'tags': article['tags'],
                'content': ' '.join(plain.split())[:3000],
            })
        with open(self.blog_dir / "posts.json", 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=1)
        print(f"✅ Generated search index with {len(entries)} articles")

    def generate_rss_feed(self, articles, feed_name='feed.xml', lang=None):
        """Generate an RSS feed for the blog"""
        from email.utils import formatdate
        import time
        
        # Sort articles by date (newest first)
        sorted_articles = sorted(articles, key=lambda x: x['date_iso'], reverse=True)
        
        # Take only the latest 10 articles for RSS
        recent_articles = sorted_articles[:10]
        
        # RSS template
        rss_template = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <channel>
        <title>{channel_title}</title>
        <link>https://joycegu.github.io/CuriousBuild/blog/</link>
        <description>{channel_description}</description>
        <language>{channel_language}</language>
        <lastBuildDate>{last_build_date}</lastBuildDate>
        <atom:link href="https://joycegu.github.io/CuriousBuild/blog/{feed_name}" rel="self" type="application/rss+xml"/>
        <generator>Joyce's Blog Generator</generator>
        <ttl>1440</ttl>
{items}
    </channel>
</rss>'''

        # Generate RSS items
        items = []
        for article in recent_articles:
            # Convert date to RFC 822 format
            try:
                article_date = datetime.strptime(article['date_iso'], '%Y-%m-%d')
                pub_date = formatdate(time.mktime(article_date.timetuple()))
            except:
                pub_date = formatdate()
            
            # Clean summary for RSS (remove HTML if any)
            clean_summary = article['summary'].replace('<', '&lt;').replace('>', '&gt;')
            
            item = f'''        <item>
            <title><![CDATA[{article['title']}]]></title>
            <link>https://joycegu.github.io/CuriousBuild/blog/posts/{quote(article['filename'])}</link>
            <guid>https://joycegu.github.io/CuriousBuild/blog/posts/{quote(article['filename'])}</guid>
            <description><![CDATA[{clean_summary}]]></description>
            <pubDate>{pub_date}</pubDate>
            <dc:creator>Joyce Gu</dc:creator>
        </item>'''
            items.append(item)
        
        # Current timestamp for lastBuildDate
        last_build_date = formatdate()
        
        # Generate final RSS content
        if lang == 'zh':
            channel = ('Joyce 的数字花园', '关于技术、增长和生活的思考与发现。', 'zh-cn')
        else:
            channel = ("Joyce's Digital Garden",
                       'Thoughts, discoveries, and adventures in technology, growth, and life insights.',
                       'en-us')
        rss_content = rss_template.format(
            channel_title=channel[0],
            channel_description=channel[1],
            channel_language=channel[2],
            feed_name=feed_name,
            last_build_date=last_build_date,
            items='\n'.join(items)
        )
        
        # Write RSS file
        rss_path = self.blog_dir / feed_name
        with open(rss_path, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        
        print(f"✅ Generated {feed_name} with {len(recent_articles)} articles")

def main():
    converter = SimpleBlogConverter()
    
    print("🔄 Converting Markdown files to HTML...")
    articles = converter.convert_all_markdown()
    
    if articles:
        print(f"\n📝 Updating blog index...")
        converter.update_blog_index(articles)
        print(f"\n🎉 Successfully processed {len(articles)} articles!")
    else:
        print("\n📝 No articles to process.")
        print(f"💡 Create markdown files in: {converter.markdown_dir}")

if __name__ == "__main__":
    main()
