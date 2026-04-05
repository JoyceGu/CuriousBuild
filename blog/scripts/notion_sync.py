#!/usr/bin/env python3
"""
Notion to Blog sync script
Syncs published articles from Notion database to blog markdown files
"""

import os
import requests
import json
import re
from datetime import datetime
from pathlib import Path

from simple_md_converter import SimpleBlogConverter

def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables from .env file
load_env_file()

class NotionBlogSync:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not self.notion_token or not self.database_id:
            print("❌ 请设置环境变量:")
            print("   export NOTION_TOKEN='your_notion_token'")
            print("   export NOTION_DATABASE_ID='your_database_id'")
            return
            
        self.headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        self.blog_dir = Path(__file__).parent.parent
        self.markdown_dir = self.blog_dir / "markdown"
        self.markdown_dir.mkdir(exist_ok=True)
        
        print(f"📁 博客目录: {self.blog_dir}")
        print(f"📝 Markdown目录: {self.markdown_dir}")
    
    def query_published_posts(self):
        """查询所有已发布的文章"""
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        payload = {
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Published"
                }
            },
            "sorts": [
                {
                    "property": "Date",
                    "direction": "descending"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                results = response.json()['results']
                print(f"📚 找到 {len(results)} 篇已发布文章")
                return results
            else:
                print(f"❌ 查询Notion失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return []
        except Exception as e:
            print(f"❌ 连接Notion失败: {e}")
            return []

    def query_all_posts(self):
        """查询数据库中的全部条目（任意 Status），用于清理已改为 Draft 的本地文件"""
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        payload = {
            "sorts": [
                {"property": "Date", "direction": "descending"}
            ],
            "page_size": 100
        }
        results = []
        start_cursor = None
        try:
            while True:
                body = dict(payload)
                if start_cursor:
                    body["start_cursor"] = start_cursor
                response = requests.post(url, headers=self.headers, json=body)
                if response.status_code != 200:
                    print(f"❌ 查询Notion(全部)失败: {response.status_code}")
                    print(f"错误信息: {response.text}")
                    return results
                data = response.json()
                results.extend(data.get("results", []))
                if not data.get("has_more"):
                    break
                start_cursor = data.get("next_cursor")
            print(f"📚 数据库共 {len(results)} 条（含 Draft 等）")
            return results
        except Exception as e:
            print(f"❌ 连接Notion失败: {e}")
            return []

    def get_page_status_name(self, page):
        props = page.get("properties", {})
        st = props.get("Status")
        if st and st.get("select") and st["select"].get("name"):
            return st["select"]["name"]
        return None

    def get_page_content(self, page_id):
        """获取页面内容"""
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()['results']
            else:
                print(f"❌ 获取页面内容失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ 获取页面内容错误: {e}")
            return []
    
    def extract_rich_text(self, rich_text_array):
        """提取富文本内容"""
        if not rich_text_array:
            return ""
            
        result = []
        for text_obj in rich_text_array:
            text = text_obj.get('text', {}).get('content', '')
            annotations = text_obj.get('annotations', {})
            
            # 应用格式
            if annotations.get('bold'):
                text = f'**{text}**'
            if annotations.get('italic'):
                text = f'*{text}*'
            if annotations.get('code'):
                text = f'`{text}`'
            
            # 处理链接
            link = text_obj.get('text', {}).get('link')
            if link:
                url = link.get('url', '')
                text = f'[{text}]({url})'
            
            result.append(text)
        
        return ''.join(result)
    
    def convert_notion_to_markdown(self, blocks):
        """将Notion块转换为Markdown"""
        markdown_content = []
        
        for block in blocks:
            block_type = block.get('type')
            block_data = block.get(block_type, {})
            
            if block_type == 'paragraph':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                if text.strip():
                    markdown_content.append(text)
                    markdown_content.append('')
            
            elif block_type == 'heading_1':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'# {text}')
                markdown_content.append('')
            
            elif block_type == 'heading_2':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'## {text}')
                markdown_content.append('')
            
            elif block_type == 'heading_3':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'### {text}')
                markdown_content.append('')
            
            elif block_type == 'bulleted_list_item':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'- {text}')
            
            elif block_type == 'numbered_list_item':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'1. {text}')
            
            elif block_type == 'quote':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'> {text}')
                markdown_content.append('')
            
            elif block_type == 'code':
                language = block_data.get('language', '')
                text = self.extract_rich_text(block_data.get('rich_text', []))
                markdown_content.append(f'```{language}')
                markdown_content.append(text)
                markdown_content.append('```')
                markdown_content.append('')
            
            elif block_type == 'divider':
                markdown_content.append('---')
                markdown_content.append('')
        
        return '\n'.join(markdown_content)
    
    def extract_page_properties(self, page):
        """提取页面属性"""
        properties = page.get('properties', {})
        
        # 标题
        title = "Untitled"
        title_prop = properties.get('Title') or properties.get('Name')
        if title_prop and title_prop.get('title'):
            title = title_prop['title'][0]['text']['content']
        
        # 日期
        date = datetime.now().strftime('%Y-%m-%d')
        date_prop = properties.get('Date')
        if date_prop and date_prop.get('date') and date_prop['date'].get('start'):
            date = date_prop['date']['start']
        
        # 标签 - 尝试多种可能的字段名
        tags = []
        # 尝试常见的标签字段名
        possible_tag_fields = ['Tags', 'Tag', 'tags', 'tag', 'Labels', 'Category', 'Categories']
        
        for field_name in possible_tag_fields:
            tags_prop = properties.get(field_name)
            if tags_prop:
                if tags_prop.get('multi_select'):
                    tags = [tag['name'] for tag in tags_prop['multi_select']]
                    break
                elif tags_prop.get('select') and tags_prop['select']:
                    tags = [tags_prop['select']['name']]
                    break
                elif tags_prop.get('status') and tags_prop['status']:
                    tags = [tags_prop['status']['name']]
                    break
        
        # 摘要
        summary = ""
        summary_prop = properties.get('Summary')
        if summary_prop and summary_prop.get('rich_text') and summary_prop['rich_text']:
            summary = summary_prop['rich_text'][0]['text']['content']
        
        
        return {
            'title': title,
            'date': date,
            'tags': tags,
            'summary': summary
        }
    
    def create_filename(self, title):
        """创建URL友好的文件名"""
        # 移除特殊字符，转换为小写
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        # 将空格和多个连字符替换为单个连字符
        filename = re.sub(r'[-\s]+', '-', filename)
        # 移除首尾连字符
        filename = filename.strip('-')
        return f"{filename}.md"
    
    def _delete_blog_post_files(self, md_path, meta):
        """删除一篇本地文章对应的 markdown 与 posts 下 HTML"""
        posts_dir = self.blog_dir / "posts"
        md_path.unlink(missing_ok=True)
        stem = meta.get('filename')
        if stem:
            html_name = stem if str(stem).endswith('.html') else f'{stem}.html'
        else:
            conv = SimpleBlogConverter()
            html_name = conv.create_filename(meta.get('title', 'untitled'))
        html_path = posts_dir / html_name
        html_path.unlink(missing_ok=True)

    def remove_unpublished_local_files(self, published_ids, all_pages):
        """
        删除本地仍保留、但 Notion 中已不是 Published 的文章。
        优先用 frontmatter 中的 notion_page_id；旧文件则按标题与数据库唯一匹配。
        """
        converter = SimpleBlogConverter()
        by_title = {}
        for page in all_pages:
            props = self.extract_page_properties(page)
            t = props['title']
            if not t or t == 'Untitled':
                continue
            by_title.setdefault(t, []).append(page)

        removed = 0
        for md_path in list(self.markdown_dir.glob('*.md')):
            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                meta, _ = converter.parse_frontmatter(content)
            except OSError:
                continue

            notion_pid = meta.get('notion_page_id')
            if notion_pid:
                if notion_pid in published_ids:
                    continue
                self._delete_blog_post_files(md_path, meta)
                removed += 1
                print(f"🗑  已移除（Notion 非 Published）: {md_path.name}")
                continue

            title = meta.get('title')
            if not title:
                continue
            same = by_title.get(title, [])
            if len(same) != 1:
                continue
            st = self.get_page_status_name(same[0])
            if st == 'Published':
                continue
            self._delete_blog_post_files(md_path, meta)
            removed += 1
            label = st if st else '未设置 Status'
            print(f"🗑  已移除（数据库中为 {label}）: {md_path.name}")

        if removed:
            print(f"📭 共移除 {removed} 篇本地文章（与 Draft 等状态对齐）")
        return removed

    def sync_posts(self):
        """同步所有文章"""
        if not self.notion_token or not self.database_id:
            return
            
        print("🔄 开始从Notion同步文章...")
        posts = self.query_published_posts()
        published_ids = {p['id'] for p in posts}
        all_pages = self.query_all_posts()

        if not posts:
            print("📝 当前没有 Status=Published 的文章")
        
        synced_count = 0
        
        for post in posts:
            try:
                # 提取属性
                properties = self.extract_page_properties(post)
                
                if not properties['title'] or properties['title'] == "Untitled":
                    print(f"⚠️  跳过无标题文章")
                    continue
                
                print(f"📄 处理文章: {properties['title']}")
                
                # 获取内容
                blocks = self.get_page_content(post['id'])
                content = self.convert_notion_to_markdown(blocks)
                
                # 创建文件名
                filename = self.create_filename(properties['title'])
                
                # 如果没有摘要，从内容中生成
                if not properties['summary'] and content:
                    # 提取纯文本用于摘要
                    clean_content = re.sub(r'[#*`>\[\]()]', '', content)
                    clean_content = ' '.join(clean_content.split())
                    properties['summary'] = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content
                
                # 生成前置信息（notion_page_id 用于下次同步时删除已下线文章）
                tags_str = ', '.join(properties['tags']) if properties['tags'] else 'Personal'
                page_id = post['id']
                frontmatter = f"""---
title: {properties['title']}
date: {properties['date']}
tags: {tags_str}
summary: {properties['summary']}
filename: {filename.replace('.md', '')}
notion_page_id: {page_id}
---

"""
                
                # 组合完整内容
                full_content = frontmatter + content
                
                # 写入文件
                file_path = self.markdown_dir / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                
                print(f"✅ 同步成功: {filename}")
                synced_count += 1
                
            except Exception as e:
                print(f"❌ 同步文章失败: {e}")
                continue

        self.remove_unpublished_local_files(published_ids, all_pages)
        
        print(f"\n🎉 同步完成! 共写入 {synced_count} 篇 Published 文章")
        
        print("🔨 正在构建博客...")
        self.build_blog()
    
    def build_blog(self):
        """构建博客"""
        try:
            import subprocess
            import sys
            
            os.chdir(self.blog_dir)
            result = subprocess.run([sys.executable, 'build.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 博客构建成功!")
                print("🌐 访问: http://localhost:8000/blog/")
            else:
                print(f"❌ 博客构建失败: {result.stderr}")
                
        except Exception as e:
            print(f"❌ 构建博客时出错: {e}")

def main():
    print("🚀 Notion博客同步工具")
    print("=" * 50)
    
    sync = NotionBlogSync()
    sync.sync_posts()

if __name__ == "__main__":
    main()
