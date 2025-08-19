---
title: How to Set Up Notion and Blog Sync
date: 2025-08-18
tags: Personal
summary: Overview This integration system allows you to write blog posts directly in Notion and automatically sync them to your website! Fully compatible with ...
filename: how-to-set-up-notion-and-blog-sync
---

# Overview

This integration system allows you to write blog posts directly in Notion and automatically sync them to your website!

**Fully compatible with existing system** ✓ - Won't change any existing blog templates or styles

## Workflow

Notion Database → Auto Sync → Markdown Files → Blog HTML → Website Update

## Step 1: Create Notion Database

### 1.1 Create New Database

1. Create a new page in Notion
1. Add a Database
1. Select "Table" view
### 1.2 Setup Database Fields

**Required Fields:**

- **Title** - Title type - Article title
- **Status** - Select type - Options: 'Draft', 'Published'
- **Date** - Date type - Publication date
**Optional Fields:**

- **Tags** - Multi-select type - Article tags
- **Summary** - Text type - Article summary
### 1.3 Database Example

## Step 2: Get Notion API Key

### 2.1 Create Integration

1. Visit [Notion Integrations](https://www.notion.so/my-integrations)
1. Click "New integration"
1. Fill in the information:

1. Click "Submit"
1. Copy the **Internal Integration Token** (keep it secret!)
### 2.2 Connect Database

1. Go back to your Notion database page
1. Click the "..." menu in the top right
1. Select "Add connections"
1. Choose your newly created "Blog Sync" integration
### 2.3 Get Database ID

1. Open your database in the browser
1. Copy the database ID from the URL (32-character string)[https://notion.so/your-workspace/DATABASE_ID?v=](https://notion.so/your-workspace/DATABASE_ID?v=)...
                                ^^^^^^^^^^^
## Step 3: Local Setup

### 3.1 Set Environment Variables

**MacOS/Linux:**

# Add to ~/.zshrc or ~/.bash_profile

export NOTION_TOKEN="your_integration_token_here"
export NOTION_DATABASE_ID="your_database_id_here"

# Reload configuration

source ~/.zshrc

**Temporary Setup (current session only):**

export NOTION_TOKEN="your_integration_token_here"
export NOTION_DATABASE_ID="your_database_id_here"

### 3.2 Test Sync

cd blog
python3 sync_notion.py

If successful, you'll see:

# 🚀 Notion Blog Local Sync

✅ Found Notion credentials
📚 Found X published articles
📄 Processing article: My First Article
✅ Sync successful: [my-first-article.md](http://my-first-article.md/)
🎉 Sync complete! Processed X articles
✅ Blog build successful!

## Step 4: GitHub Automation Setup

### 4.1 Setup GitHub Secrets

1. Visit your GitHub repository
1. Click "Settings" → "Secrets and variables" → "Actions"
1. Click "New repository secret"
1. Add two secrets:

### 4.2 Auto Sync

GitHub Actions will:

- Automatically check Notion updates daily
- Sync published articles
- Auto build and deploy blog
## Step 5: Writing Workflow

### 5.1 Writing in Notion

1. Create a new row in the database
1. Fill in title, tags, summary
1. **Set Status to 'Draft'**
1. Write content in the page (supports all Notion formats)
### 5.2 Publishing Articles

1. After finishing content, change **Status to 'Published'**
1. Set publication date
1. Wait for auto sync (daily) or trigger manually
### 5.3 Manual Sync

**Local Sync:**

cd blog
python3 sync_notion.py

**GitHub Manual Trigger:**

1. Visit GitHub repository
1. Click "Actions" → "Notion Blog Auto-Sync"
1. Click "Run workflow"
## Supported Notion Formats

✓ **Text Formatting:** Bold, italic, inline code  
✓ **Headings:** H1, H2, H3  
✓ **Lists:** Ordered lists, unordered lists  
✓ **Quote Blocks:** > Quote text  
✓ **Code Blocks:** Syntax highlighting support  
✓ **Dividers:** ---  
✓ **Links:** Auto conversion

## Troubleshooting

### Common Issues

**Q: Sync fails with 401 error**
A: Check if Integration Token is correct, ensure database is connected

**Q: No articles found**
A: Make sure article Status is "Published", verify database ID is correct

**Q: Article format is wrong**
A: Check Notion database field names match (Title, Status, Date, Tags, Summary)

**Q: GitHub Actions fails**
A: Check if GitHub Secrets are properly set
