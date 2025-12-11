#!/usr/bin/env python3
"""
Notion数据库重复文章清理脚本
用于识别和清理重复的文章
"""

import os
import requests
import json
import re
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

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

class NotionDuplicateCleaner:
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
        """查询所有文章（包括Published和Draft状态）"""
        url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
        
        # 查询所有文章，不筛选状态
        payload = {
            "sorts": [
                {
                    "property": "Date",
                    "direction": "descending"
                }
            ]
        }
        
        all_posts = []
        has_more = True
        start_cursor = None
        
        while has_more:
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
                    print(f"❌ 查询Notion失败: {response.status_code}")
                    print(f"错误信息: {response.text}")
                    break
            except Exception as e:
                print(f"❌ 连接Notion失败: {e}")
                break
        
        print(f"📚 找到 {len(all_posts)} 篇文章（所有状态）")
        return all_posts
    
    def get_page_content(self, page_id):
        """获取页面内容"""
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()['results']
            else:
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
            result.append(text)
        
        return ''.join(result)
    
    def convert_notion_to_text(self, blocks):
        """将Notion块转换为纯文本（用于比较）"""
        text_content = []
        
        for block in blocks:
            block_type = block.get('type')
            block_data = block.get(block_type, {})
            
            if block_type == 'paragraph':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                if text.strip():
                    text_content.append(text)
            
            elif block_type in ['heading_1', 'heading_2', 'heading_3']:
                text = self.extract_rich_text(block_data.get('rich_text', []))
                if text.strip():
                    text_content.append(text)
            
            elif block_type in ['bulleted_list_item', 'numbered_list_item']:
                text = self.extract_rich_text(block_data.get('rich_text', []))
                if text.strip():
                    text_content.append(text)
            
            elif block_type == 'quote':
                text = self.extract_rich_text(block_data.get('rich_text', []))
                if text.strip():
                    text_content.append(text)
        
        # 合并所有文本，移除多余空格
        full_text = ' '.join(text_content)
        # 移除所有标点符号和空格，只保留字母数字，用于比较
        clean_text = re.sub(r'[^\w]', '', full_text.lower())
        return clean_text
    
    def extract_page_properties(self, page):
        """提取页面属性"""
        properties = page.get('properties', {})
        
        # 标题
        title = "Untitled"
        title_prop = properties.get('Title') or properties.get('Name')
        if title_prop and title_prop.get('title'):
            title = title_prop['title'][0]['text']['content']
        
        # 状态
        status = "Draft"
        status_prop = properties.get('Status')
        if status_prop and status_prop.get('select'):
            status = status_prop['select']['name']
        
        # 日期
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
    
    def calculate_similarity(self, text1, text2):
        """计算两个文本的相似度"""
        if not text1 or not text2:
            return 0.0
        
        # 使用SequenceMatcher计算相似度
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_duplicates(self):
        """查找重复的文章"""
        print("🔍 开始查找重复文章...")
        
        all_posts = self.query_all_posts()
        
        if len(all_posts) < 2:
            print("📝 文章数量不足，无法查找重复")
            return []
        
        # 提取所有文章的信息
        posts_info = []
        for post in all_posts:
            try:
                properties = self.extract_page_properties(post)
                if properties['title'] == "Untitled":
                    continue
                
                # 获取内容
                blocks = self.get_page_content(post['id'])
                content_text = self.convert_notion_to_text(blocks)
                
                posts_info.append({
                    'page_id': post['id'],
                    'title': properties['title'],
                    'status': properties['status'],
                    'date': properties['date'],
                    'content': content_text,
                    'raw_post': post
                })
                
                print(f"  📄 {properties['title']} ({properties['status']})")
            except Exception as e:
                print(f"  ⚠️  处理文章时出错: {e}")
                continue
        
        # 查找重复
        duplicates = []
        checked = set()
        
        for i, post1 in enumerate(posts_info):
            if post1['page_id'] in checked:
                continue
            
            similar_posts = [post1]
            
            for j, post2 in enumerate(posts_info[i+1:], start=i+1):
                if post2['page_id'] in checked:
                    continue
                
                # 计算相似度
                similarity = self.calculate_similarity(post1['content'], post2['content'])
                
                # 如果内容相似度超过70%，或者内容长度相似且相似度超过60%，认为是重复
                # 同时检查标题是否相似（处理改标题的情况）
                title_similarity = self.calculate_similarity(
                    re.sub(r'[^\w]', '', post1['title'].lower()),
                    re.sub(r'[^\w]', '', post2['title'].lower())
                )
                
                is_duplicate = False
                if similarity > 0.7:
                    is_duplicate = True
                elif similarity > 0.6 and abs(len(post1['content']) - len(post2['content'])) < max(len(post1['content']), len(post2['content'])) * 0.2:
                    # 内容长度相似且相似度超过60%
                    is_duplicate = True
                elif title_similarity > 0.5 and similarity > 0.5:
                    # 标题相似且内容有一定相似度
                    is_duplicate = True
                
                if is_duplicate:
                    print(f"    🔍 发现相似: '{post1['title']}' vs '{post2['title']}' (相似度: {similarity:.2%}, 标题相似度: {title_similarity:.2%})")
                    similar_posts.append(post2)
                    checked.add(post2['page_id'])
            
            if len(similar_posts) > 1:
                duplicates.append(similar_posts)
                checked.add(post1['page_id'])
        
        return duplicates
    
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
                print(f"  ❌ 更新失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"  ❌ 更新错误: {e}")
            return False
    
    def cleanup_duplicates(self, auto_clean=False):
        """清理重复文章"""
        duplicates = self.find_duplicates()
        
        if not duplicates:
            print("\n✅ 没有找到重复文章！")
            return
        
        print(f"\n🔍 找到 {len(duplicates)} 组重复文章:")
        print("=" * 60)
        
        for idx, group in enumerate(duplicates, 1):
            print(f"\n📦 重复组 {idx} ({len(group)} 篇文章):")
            
            # 按日期和状态排序，保留最新的Published版本
            group_sorted = sorted(group, key=lambda x: (
                x['status'] != 'Published',  # Published优先
                x['date']  # 日期越新越好
            ), reverse=True)
            
            keep_post = group_sorted[0]
            duplicate_posts = group_sorted[1:]
            
            print(f"  ✅ 保留: {keep_post['title']} ({keep_post['status']}, {keep_post['date']})")
            
            for dup in duplicate_posts:
                print(f"  🗑️  标记为Draft: {dup['title']} ({dup['status']}, {dup['date']})")
            
            if auto_clean:
                print("\n  🔄 正在更新状态...")
                for dup in duplicate_posts:
                    if self.update_page_status(dup['page_id'], "Draft"):
                        print(f"  ✅ 已将 '{dup['title']}' 标记为Draft")
                    else:
                        print(f"  ❌ 更新 '{dup['title']}' 失败")
            else:
                print("\n  💡 提示: 运行脚本时添加 --auto 参数将自动更新状态")
        
        print("\n" + "=" * 60)
        print(f"📊 总结: 找到 {len(duplicates)} 组重复，共 {sum(len(g) - 1 for g in duplicates)} 篇需要处理")

def main():
    import sys
    
    print("🧹 Notion数据库重复文章清理工具")
    print("=" * 60)
    
    cleaner = NotionDuplicateCleaner()
    
    if not cleaner.notion_token or not cleaner.database_id:
        print("\n💡 请先设置环境变量后重新运行")
        return
    
    auto_clean = '--auto' in sys.argv or '-a' in sys.argv
    
    if auto_clean:
        print("⚠️  自动清理模式已启用，将自动将重复文章标记为Draft")
        response = input("确认继续? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ 已取消")
            return
    
    cleaner.cleanup_duplicates(auto_clean=auto_clean)
    
    if auto_clean:
        print("\n✨ 清理完成！")
        print("💡 建议运行同步脚本重新同步: cd blog && python3 sync_notion.py")

if __name__ == "__main__":
    main()

