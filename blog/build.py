#!/usr/bin/env python3
"""
Blog build script - Convert markdown to HTML and update blog
Usage: python3 build.py
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from simple_md_converter import SimpleBlogConverter

def main():
    print("🚀 Building Joyce's Blog...")
    print("=" * 50)
    
    converter = SimpleBlogConverter()
    
    # Convert markdown files
    articles = converter.convert_all_markdown()
    
    if articles:
        # Update blog index
        converter.update_blog_index(articles)
        
        print("\n" + "=" * 50)
        print(f"✨ Blog build complete!")
        print(f"📝 Processed {len(articles)} articles")
        print(f"🌐 Visit: http://localhost:8000/blog/")
        
        # List processed articles
        print("\n📚 Articles:")
        for article in articles:
            print(f"   • {article['title']} ({article['date_formatted']})")
    else:
        print("\n" + "=" * 50)
        print("📝 No articles found to build.")
        print(f"💡 Add markdown files to: blog/markdown/")
        print("📖 See blog/templates/HOW-TO-CREATE-ARTICLES.md for help")

if __name__ == "__main__":
    main()
