#!/usr/bin/env python3
"""
Markdown to HTML converter for Joyce's Blog
Converts markdown files to HTML using the blog template
"""

import os
import re
import markdown
import yaml
from datetime import datetime
from pathlib import Path

class BlogConverter:
    def __init__(self):
        self.blog_dir = Path(__file__).parent.parent
        self.markdown_dir = self.blog_dir / "markdown"
        self.posts_dir = self.blog_dir / "posts"
        self.templates_dir = self.blog_dir / "templates"
        
        # Ensure directories exist
        self.posts_dir.mkdir(exist_ok=True)
        
        # HTML template
        self.html_template = self._load_template()
        
    def _load_template(self):
        """Load the HTML template for articles"""
        return '''<!DOCTYPE html>
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
                <a href="../../" class="site-title">Back to Joyce's Playground</a>
                <div class="nav-links">
                    <a href="../" class="nav-link">Home</a>
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
                    {content}
                </div>

                <!-- Article Footer -->
                <footer class="article-footer">
                    <div class="article-navigation">
                        <a href="../" class="nav-prev">← Back to Blog</a>
                        <a href="#" class="nav-next">Next Article →</a>
                    </div>
                    
                    <div class="article-share">
                        <p>Share this article:</p>
                        <div class="share-buttons">
                            <a href="https://twitter.com/intent/tweet?text={title}&url={url}" class="share-button" target="_blank">Twitter</a>
                            <a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" class="share-button" target="_blank">LinkedIn</a>
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

    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                _, frontmatter, markdown_content = content.split('---', 2)
                metadata = yaml.safe_load(frontmatter.strip())
                return metadata, markdown_content.strip()
            except:
                return {}, content
        return {}, content
    
    def calculate_reading_time(self, content):
        """Calculate reading time based on word count (200 words per minute)"""
        word_count = len(content.split())
        reading_time = max(1, round(word_count / 200))
        return reading_time
    
    def generate_tags_html(self, tags):
        """Generate HTML for tags"""
        if not tags:
            return ""
        
        tags_html = []
        for tag in tags:
            tags_html.append(f'<span class="tag">{tag}</span>')
        return "\n                        ".join(tags_html)
    
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
        
        # Convert date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_iso = date_obj.strftime('%Y-%m-%d')
            date_formatted = date_obj.strftime('%B %d, %Y')
        except:
            date_iso = datetime.now().strftime('%Y-%m-%d')
            date_formatted = datetime.now().strftime('%B %d, %Y')
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code', 'tables'])
        html_content = md.convert(markdown_content)
        
        # Calculate reading time
        reading_time = self.calculate_reading_time(markdown_content)
        
        # Generate tags HTML
        tags_html = self.generate_tags_html(tags)
        
        # Create filename
        filename = metadata.get('filename') or self.create_filename(title)
        if not filename.endswith('.html'):
            filename += '.html'
        
        # Generate final HTML
        final_html = self.html_template.format(
            title=title,
            date_iso=date_iso,
            date_formatted=date_formatted,
            reading_time=reading_time,
            tags_html=tags_html,
            content=html_content,
            url=f"https://joycegu.github.io/CuriousBuild/blog/posts/{filename}"
        )
        
        # Write HTML file
        output_path = self.posts_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"✅ Converted: {md_file_path.name} → {filename}")
        
        return {
            'title': title,
            'filename': filename,
            'date_iso': date_iso,
            'date_formatted': date_formatted,
            'reading_time': reading_time,
            'tags': tags,
            'summary': metadata.get('summary', ''),
        }
    
    def convert_all_markdown(self):
        """Convert all markdown files in the markdown directory"""
        if not self.markdown_dir.exists():
            print(f"❌ Markdown directory not found: {self.markdown_dir}")
            return []
        
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
    
    def generate_blog_index(self, articles):
        """Generate the blog index HTML with all articles"""
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
        
        # Read current blog index template
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
    converter = BlogConverter()
    
    print("🔄 Converting Markdown files to HTML...")
    articles = converter.convert_all_markdown()
    
    if articles:
        print(f"\n📝 Updating blog index...")
        converter.generate_blog_index(articles)
        print(f"\n🎉 Successfully processed {len(articles)} articles!")
    else:
        print("\n📝 No articles to process.")

if __name__ == "__main__":
    main()
