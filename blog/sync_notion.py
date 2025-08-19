#!/usr/bin/env python3
"""
本地Notion同步脚本
用于本地测试和手动同步Notion文章
"""

import os
import sys
from pathlib import Path

# 添加scripts目录到路径
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from notion_sync import NotionBlogSync

def setup_credentials():
    """设置Notion凭据"""
    print("🔑 Notion API 设置")
    print("=" * 40)
    
    # 检查现有环境变量
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if token and database_id:
        print("✅ 已找到Notion凭据")
        print(f"📊 数据库ID: {database_id[:8]}...")
        return True
    
    print("❌ 未找到Notion凭据")
    print("\n请按以下步骤设置:")
    print("1. 访问 https://www.notion.so/my-integrations")
    print("2. 创建新的integration")
    print("3. 复制 Internal Integration Token")
    print("4. 在您的Notion数据库中，点击右上角'...' > 'Add connections' > 选择您的integration")
    print("5. 复制数据库ID (URL中的32位字符串)")
    
    print("\n设置环境变量:")
    print("export NOTION_TOKEN='your_token_here'")
    print("export NOTION_DATABASE_ID='your_database_id_here'")
    
    return False

def main():
    print("🚀 Notion博客本地同步")
    print("=" * 50)
    
    if not setup_credentials():
        print("\n💡 设置完成后，重新运行此脚本")
        return
    
    try:
        sync = NotionBlogSync()
        sync.sync_posts()
        
        print("\n" + "=" * 50)
        print("✨ 同步完成!")
        print("🌐 启动本地服务器查看结果:")
        print("   cd .. && python3 -m http.server 8000")
        print("   然后访问: http://localhost:8000/blog/")
        
    except KeyboardInterrupt:
        print("\n👋 同步已取消")
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")

if __name__ == "__main__":
    main()
