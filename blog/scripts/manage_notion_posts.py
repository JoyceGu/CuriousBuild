#!/usr/bin/env python3
"""
Notion文章管理脚本
用于查看、更新或删除Notion数据库中的文章
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path

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

load_env_file()

class NotionPostManager:
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
    
    def query_all_posts(self):
        """查询所有文章"""
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        
        all_posts = []
        has_more = True
        start_cursor = None
        
        while has_more:
            payload = {"sorts": [{"property": "Date", "direction": "descending"}]}
            if start_cursor:
                payload['start_cursor'] = start_cursor
            
            try:
                response = requests.post(url, headers=self.headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    all_posts.extend(data['results'])
                    has_more = data.get('has_more', False)
                    start_cursor = data.get('next_cursor')
                else:
                    print(f"❌ 查询失败: {response.status_code}")
                    break
            except Exception as e:
                print(f"❌ 连接失败: {e}")
                break
        
        return all_posts
    
    def extract_page_properties(self, page):
        """提取页面属性"""
        properties = page.get('properties', {})
        
        title = "Untitled"
        title_prop = properties.get('Title') or properties.get('Name')
        if title_prop and title_prop.get('title'):
            title = title_prop['title'][0]['text']['content']
        
        status = "Draft"
        status_prop = properties.get('Status')
        if status_prop and status_prop.get('select'):
            status = status_prop['select']['name']
        
        date = datetime.now().strftime('%Y-%m-%d')
        date_prop = properties.get('Date')
        if date_prop and date_prop.get('date') and date_prop['date'].get('start'):
            date = date_prop['date']['start']
        
        return {
            'title': title,
            'status': status,
            'date': date,
            'page_id': page['id']
        }
    
    def list_posts(self):
        """列出所有文章"""
        posts = self.query_all_posts()
        
        print(f"\n📚 找到 {len(posts)} 篇文章:\n")
        print(f"{'序号':<6} {'标题':<50} {'状态':<12} {'日期':<12} {'ID'}")
        print("=" * 100)
        
        for idx, post in enumerate(posts, 1):
            props = self.extract_page_properties(post)
            print(f"{idx:<6} {props['title'][:48]:<50} {props['status']:<12} {props['date']:<12} {props['page_id'][:8]}...")
        
        return posts
    
    def update_page_status(self, page_id, new_status="Draft"):
        """更新页面状态"""
        url = f'https://api.notion.com/v1/pages/{page_id}'
        
        payload = {
            "properties": {
                "Status": {
                    "select": {
                        "name": new_status
                    }
                }
            }
        }
        
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ 更新失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 更新错误: {e}")
            return False
    
    def archive_page(self, page_id):
        """归档页面（Notion API不支持删除，只能归档）"""
        url = f'https://api.notion.com/v1/pages/{page_id}'
        
        payload = {
            "archived": True
        }
        
        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return True
            else:
                print(f"❌ 归档失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 归档错误: {e}")
            return False

def main():
    import sys
    
    print("📝 Notion文章管理工具")
    print("=" * 60)
    
    manager = NotionPostManager()
    
    if not manager.notion_token or not manager.database_id:
        print("\n💡 请先设置环境变量后重新运行")
        return
    
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python3 manage_notion_posts.py list                    # 列出所有文章")
        print("  python3 manage_notion_posts.py draft <page_id>         # 将文章标记为Draft")
        print("  python3 manage_notion_posts.py archive <page_id>       # 归档文章")
        print("  python3 manage_notion_posts.py draft-by-title <title>  # 根据标题将文章标记为Draft")
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        manager.list_posts()
    
    elif command == 'draft' and len(sys.argv) > 2:
        page_id = sys.argv[2]
        props = manager.extract_page_properties({'id': page_id, 'properties': {}})
        print(f"\n🔄 将文章标记为Draft: {page_id}")
        if manager.update_page_status(page_id, "Draft"):
            print("✅ 更新成功")
        else:
            print("❌ 更新失败")
    
    elif command == 'archive' and len(sys.argv) > 2:
        page_id = sys.argv[2]
        print(f"\n🗄️  归档文章: {page_id}")
        response = input("确认归档? (yes/no): ")
        if response.lower() == 'yes':
            if manager.archive_page(page_id):
                print("✅ 归档成功")
            else:
                print("❌ 归档失败")
        else:
            print("❌ 已取消")
    
    elif command == 'draft-by-title' and len(sys.argv) > 2:
        search_title = ' '.join(sys.argv[2:])
        posts = manager.query_all_posts()
        
        matching_posts = []
        for post in posts:
            props = manager.extract_page_properties(post)
            if search_title.lower() in props['title'].lower():
                matching_posts.append((post, props))
        
        if not matching_posts:
            print(f"\n❌ 没有找到标题包含 '{search_title}' 的文章")
            return
        
        print(f"\n🔍 找到 {len(matching_posts)} 篇匹配的文章:")
        for idx, (post, props) in enumerate(matching_posts, 1):
            print(f"  {idx}. {props['title']} ({props['status']}) - {props['page_id'][:8]}...")
        
        if len(matching_posts) == 1:
            post, props = matching_posts[0]
            print(f"\n🔄 将 '{props['title']}' 标记为Draft")
            if manager.update_page_status(props['page_id'], "Draft"):
                print("✅ 更新成功")
            else:
                print("❌ 更新失败")
        else:
            print("\n💡 找到多篇文章，请使用 'draft <page_id>' 命令指定具体文章")

if __name__ == "__main__":
    main()

