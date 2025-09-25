# GitHub Actions 设置指南

## 修复权限问题

### 1. 设置 GitHub Secrets

在您的 GitHub 仓库中设置以下 Secrets：

1. 访问 `https://github.com/JoyceGu/CuriousBuild/settings/secrets/actions`
2. 添加以下 Secrets：

**NOTION_TOKEN**
```
your_notion_integration_token_here
```

**NOTION_DATABASE_ID**
```
your_notion_database_id_here
```

### 2. 启用 GitHub Pages

1. 访问 `https://github.com/JoyceGu/CuriousBuild/settings/pages`
2. 在 "Source" 下选择 "GitHub Actions"
3. 保存设置

### 3. 权限设置

确保 GitHub Actions 有正确的权限：

1. 访问 `https://github.com/JoyceGu/CuriousBuild/settings/actions`
2. 在 "Workflow permissions" 下选择 "Read and write permissions"
3. 勾选 "Allow GitHub Actions to create and approve pull requests"
4. 保存设置

### 4. 手动触发测试

1. 访问 `https://github.com/JoyceGu/CuriousBuild/actions`
2. 点击 "Notion Blog Auto-Sync" 工作流
3. 点击 "Run workflow" 按钮进行测试

## 问题解决

如果遇到权限错误：
- 检查 Secrets 是否正确设置
- 确认 GitHub Pages 源设置为 "GitHub Actions"
- 验证工作流权限设置为 "Read and write permissions"

## 自动同步

工作流将：
- 每天北京时间 10:00 自动运行
- 从 Notion 同步已发布的文章
- 自动构建并部署到 GitHub Pages
- 只有在检测到更改时才会提交和部署


