#!/usr/bin/env python3
"""
把网站需要公开的文件复制到 dist/，供 Cloudflare Pages 发布

Cloudflare Pages 设置：Build command 填 `python3 build_site.py`，Build output directory 填 `dist`。
只复制下面列出的文件，所以 Python 脚本、markdown 原稿、workflow 等源码不会被发布出去。
网站新增了需要公开的文件时，记得加到 PUBLIC_PATHS 里。
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'

PUBLIC_PATHS = [
    # 主页
    'index.html',
    'styles.css',
    'custom.css',
    'script.js',
    'fruits-config.js',
    'i18n.js',
    'images',
    # 博客（HTML 由 blog/build.py 生成并提交在仓库里）
    'blog/index.html',
    'blog/blog-styles.css',
    'blog/blog-script.js',
    'blog/subscribe-config.js',
    'blog/posts.json',
    'blog/posts',
    'blog/templates/article-styles.css',
    'blog/feed*.xml',
]


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    count = 0
    for pattern in PUBLIC_PATHS:
        matches = sorted(ROOT.glob(pattern))
        if not matches:
            raise SystemExit(f'❌ Missing public file: {pattern}')
        for src in matches:
            dest = DIST / src.relative_to(ROOT)
            if src.is_dir():
                shutil.copytree(src, dest)
                count += sum(1 for p in dest.rglob('*') if p.is_file())
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                count += 1
    print(f'✅ Copied {count} public files to {DIST.name}/')


if __name__ == '__main__':
    main()
