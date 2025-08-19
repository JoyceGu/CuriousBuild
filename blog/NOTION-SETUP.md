# 🚀 Notion Blog Integration Setup Guide

## 📋 Overview

This integration system allows you to write blog posts directly in Notion and automatically sync them to your website!

**Fully compatible with existing system** ✅ - Won't change any existing blog templates or styles

## 🎯 Workflow

```
Notion Database → Auto Sync → Markdown Files → Blog HTML → Website Update
```

## 📊 Step 1: Create Notion Database

### 1.1 Create New Database
1. Create a new page in Notion
2. Add a Database
3. Select "Table" view

### 1.2 Setup Database Fields

**Required Fields:**
- **Title** - Title type - Article title
- **Status** - Select type - Options: `Draft`, `Published`
- **Date** - Date type - Publication date

**Optional Fields:**
- **Tags** - Multi-select type - Article tags
- **Summary** - Text type - Article summary

### 1.3 Database Example

| Title | Status | Date | Tags | Summary |
|-------|--------|------|------|---------|
| My First Article | Published | 2024-01-18 | Personal, Life | This is my first blog post... |
| Data Science Learning | Draft | 2024-01-20 | Data Science, Learning | Sharing my data science journey... |

## 🔑 Step 2: Get Notion API Key

### 2.1 Create Integration
1. Visit [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Fill in the information:
   - Name: `Blog Sync`
   - Associated workspace: Select your workspace
   - Capabilities: Check `Read content`
4. Click "Submit"
5. Copy the **Internal Integration Token** (keep it secret!)

### 2.2 Connect Database
1. Go back to your Notion database page
2. Click the "..." menu in the top right
3. Select "Add connections"
4. Choose your newly created "Blog Sync" integration

### 2.3 Get Database ID
1. Open your database in the browser
2. Copy the database ID from the URL (32-character string)
   ```
   https://notion.so/your-workspace/DATABASE_ID?v=...
                                   ^^^^^^^^^^^
   ```

## 🖥️ Step 3: Local Setup

### 3.1 Set Environment Variables

**MacOS/Linux:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export NOTION_TOKEN="your_integration_token_here"
export NOTION_DATABASE_ID="your_database_id_here"

# Reload configuration
source ~/.zshrc
```

**Temporary Setup (current session only):**
```bash
export NOTION_TOKEN="your_integration_token_here"
export NOTION_DATABASE_ID="your_database_id_here"
```

### 3.2 Test Sync
```bash
cd blog
python3 sync_notion.py
```

If successful, you'll see:
```
🚀 Notion Blog Local Sync
==================================================
✅ Found Notion credentials
📚 Found X published articles
📄 Processing article: My First Article
✅ Sync successful: my-first-article.md
🎉 Sync complete! Processed X articles
✅ Blog build successful!
```

## ☁️ Step 4: GitHub Automation Setup

### 4.1 Setup GitHub Secrets
1. Visit your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add two secrets:
   - **Name:** `NOTION_TOKEN`, **Value:** Your Integration Token
   - **Name:** `NOTION_DATABASE_ID`, **Value:** Your Database ID

### 4.2 Auto Sync
GitHub Actions will:
- Automatically check Notion updates daily
- Sync published articles
- Auto build and deploy blog

## ✍️ Step 5: Writing Workflow

### 5.1 Writing in Notion
1. Create a new row in the database
2. Fill in title, tags, summary
3. **Set Status to `Draft`**
4. Write content in the page (supports all Notion formats)

### 5.2 Publishing Articles
1. After finishing content, change **Status to `Published`**
2. Set publication date
3. Wait for auto sync (daily) or trigger manually

### 5.3 Manual Sync
**Local Sync:**
```bash
cd blog
python3 sync_notion.py
```

**GitHub Manual Trigger:**
1. Visit GitHub repository
2. Click "Actions" → "Notion Blog Auto-Sync"
3. Click "Run workflow"

## 🎨 Supported Notion Formats

✅ **Text Formatting:** Bold, italic, inline code  
✅ **Headings:** H1, H2, H3  
✅ **Lists:** Ordered lists, unordered lists  
✅ **Quote Blocks:** > Quote text  
✅ **Code Blocks:** Syntax highlighting support  
✅ **Dividers:** ---  
✅ **Links:** Auto conversion  

## 🔧 Troubleshooting

### Common Issues

**Q: Sync fails with 401 error**
A: Check if Integration Token is correct, ensure database is connected

**Q: No articles found**
A: Make sure article Status is "Published", verify database ID is correct

**Q: Article format is wrong**
A: Check Notion database field names match (Title, Status, Date, Tags, Summary)

**Q: GitHub Actions fails**
A: Check if GitHub Secrets are properly set

### Debugging Steps
1. Test locally first: `python3 sync_notion.py`
2. Check generated markdown files: `blog/markdown/`
3. Manual build test: `python3 build.py`

## 💡 Usage Tips

### Best Practices
1. **Draft First**: Set to Draft first, then Published when ready
2. **Meaningful Titles**: Will auto-generate URLs
3. **Add Summaries**: Shows on blog homepage
4. **Use Tags Wisely**: Helps categorize articles
5. **Regular Checks**: Occasionally verify sync results

### Tag Suggestions
Use your previously defined tags:
- `Data Science`, `Learning`, `Analytics`
- `Tools`, `Productivity`, `Tech Tips`  
- `Books`, `Reading`, `Reviews`
- `Travel`, `Life`, `Personal`

## 🎉 Complete!

Now you can:
1. ✅ Write comfortably in Notion
2. ✅ One-click publish to blog
3. ✅ Auto sync to website
4. ✅ Keep existing blog styles unchanged

Enjoy your new writing workflow! 🌟

---

**Need Help?** 
- Check `blog/scripts/notion_sync.py` output messages
- View GitHub Actions run logs
- Ensure all environment variables are set correctly
