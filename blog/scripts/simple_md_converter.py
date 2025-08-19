#!/usr/bin/env python3
"""
Simple Markdown to HTML converter for Joyce's Blog
No external dependencies required - uses only Python standard library
"""

import os
import re
import json
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
    
    def calculate_reading_time(self, content):
        """Calculate reading time based on word count"""
        word_count = len(content.split())
        reading_time = max(1, round(word_count / 200))
        return reading_time
    
    def create_filename(self, title):
        """Create a URL-friendly filename from title"""
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return f"{filename}.html"
    
    def convert_markdown_file(self, md_file_path):
        """Convert a single markdown file to HTML"""
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        metadata, markdown_content = self.parse_frontmatter(content)
        
        # Extract metadata with defaults
        title = metadata.get('title', 'Untitled')
        date_str = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
        tags = metadata.get('tags', [])
        summary = metadata.get('summary', '')
        
        # Convert date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_iso = date_obj.strftime('%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_iso = datetime.now().strftime('%Y-%m-%d')
            date_formatted = datetime.now().strftime('%B %d, %Y')
        
        # Convert markdown to HTML
        html_content = self.simple_markdown_to_html(markdown_content)
        
        # Calculate reading time
        reading_time = self.calculate_reading_time(markdown_content)
        
        # Generate tags HTML
        tags_html = ""
        if tags:
            tag_elements = [f'<span class="tag">{tag}</span>' for tag in tags]
            tags_html = '\n                        '.join(tag_elements)
        
        # Create filename
        filename = metadata.get('filename') or self.create_filename(title)
        if not filename.endswith('.html'):
            filename += '.html'
        
        # HTML template
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Joyce's Blog</title>
    <link rel="stylesheet" href="../blog-styles.css">
    <link rel="stylesheet" href="../templates/article-styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="nav">
                <a href="/" class="site-title">Back to Joyce's Playground</a>
                <div class="nav-links">
                    <a href="/blog/" class="nav-link">Home</a>
                    <a href="#archives" class="nav-link">Archives</a>
                    <a href="#tags" class="nav-link">Tags</a>
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
                        <time datetime="{date_iso}">{date_formatted}</time>
                        <span class="reading-time">{reading_time} min</span>
                        <span class="author">Joyce Gu</span>
                    </div>
                    <div class="article-tags">
                        {tags_html}
                    </div>
                </header>

                <!-- Article Content -->
                <div class="article-content">
                    {html_content}
                </div>

                <!-- Article Footer -->
                <footer class="article-footer">
                    <div class="article-navigation">
                        <a href="/blog/" class="nav-prev">← Back to Blog</a>
                        <a href="#" class="nav-next">Next Article →</a>
                    </div>
                    
                    <div class="article-share">
                        <p>Share this article:</p>
                        <div class="share-buttons">
                            <a href="https://twitter.com/intent/tweet?text={title}&url=https://yoursite.com/blog/posts/{filename}" class="share-button" target="_blank">Twitter</a>
                            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://yoursite.com/blog/posts/{filename}" class="share-button" target="_blank">LinkedIn</a>
                            <a href="#" class="share-button" onclick="navigator.clipboard.writeText(window.location.href); alert('Link copied to clipboard!')">Copy Link</a>
                        </div>
                    </div>
                </footer>
            </article>
        </main>
    </div>

    <script src="../blog-script.js"></script>
</body>
</html>'''
        
        # Write HTML file
        output_path = self.posts_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Converted: {md_file_path.name} → {filename}")
        
        return {
            'title': title,
            'filename': filename,
            'date_iso': date_iso,
            'date_formatted': date_formatted,
            'reading_time': reading_time,
            'tags': tags,
            'summary': summary or f"{markdown_content[:150]}..." if len(markdown_content) > 150 else markdown_content,
        }
    
    def convert_all_markdown(self):
        """Convert all markdown files"""
        md_files = list(self.markdown_dir.glob('*.md'))
        if not md_files:
            print(f"📝 No markdown files found in {self.markdown_dir}")
            return []
        
        articles = []
        for md_file in sorted(md_files):
            try:
                article_info = self.convert_markdown_file(md_file)
                articles.append(article_info)
            except Exception as e:
                print(f"❌ Error converting {md_file.name}: {e}")
        
        return articles
    
    def update_blog_index(self, articles):
        """Update the blog index with articles"""
        if not articles:
            return
        
        # Sort articles by date (newest first)
        articles.sort(key=lambda x: x['date_iso'], reverse=True)
        
        # Generate article items HTML
        articles_html = []
        for article in articles:
            article_html = f'''                <article class="post-item">
                    <div class="post-content">
                        <h3 class="post-title">
                            <a href="posts/{article['filename']}">{article['title']}</a>
                        </h3>
                        <p class="post-summary">{article['summary']}</p>
                    </div>
                    <div class="post-meta">
                        <time datetime="{article['date_iso']}">{article['date_formatted']}</time>
                        <span class="reading-time">{article['reading_time']} min</span>
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
        
        # Update the blog index
        pattern = r'<!-- Posts List -->.*?</section>'
        updated_content = re.sub(pattern, new_posts_section, current_content, flags=re.DOTALL)
        
        with open(blog_index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated blog index with {len(articles)} articles")

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
