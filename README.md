# CuriousBuild - Joyce的个人主页和博客项目

这是一个包含个人主页和博客的完整网站项目。主页展示了一棵金黄色的大树，树上挂满了互动式的果实，每个果实都链接到不同的网站。同时包含一个功能完整的博客系统，支持Markdown写作和Notion同步。

## 🌐 在线访问

- **主页**：https://joycegu.github.io/CuriousBuild/
- **博客**：https://joycegu.github.io/CuriousBuild/blog/

## 功能特点

### 🏠 个人主页
- 美观的响应式界面，适配不同屏幕尺寸
- 树上的交互式果实，悬停时有动画效果
- 点击果实可跳转到预设的链接
- 简洁优雅的设计风格

### 📝 博客系统
- 支持Markdown格式写作
- 自动从Markdown生成HTML文章
- Notion集成，支持从Notion数据库同步文章
- 响应式设计，移动端友好
- 自动生成文章列表和导航

## 文件结构

### 🏠 主页文件
- `index.html`: 主页HTML文件
- `styles.css`: 主页样式表文件
- `script.js`: JavaScript交互脚本
- `images/`: 图片资源目录
  - `image.png`: 背景图片

### 📝 博客文件
- `blog/`: 博客系统目录
  - `index.html`: 博客首页
  - `blog-styles.css`: 博客样式文件
  - `markdown/`: Markdown文章源文件
  - `posts/`: 生成的HTML文章
  - `scripts/`: 构建和同步脚本
  - `templates/`: 模板文件

## 使用方法

### 🌐 在线访问
1. **主页**：访问 https://joycegu.github.io/CuriousBuild/
2. **博客**：访问 https://joycegu.github.io/CuriousBuild/blog/

### 🚀 本地启动

#### 前置要求
- Python 3.x（用于运行本地服务器和构建脚本）

#### 启动步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/JoyceGu/CuriousBuild.git
   cd CuriousBuild
   ```

2. **启动本地服务器**
   
   在项目根目录运行：
   ```bash
   python3 -m http.server 8000
   ```
   
   或者使用 Python 2（如果只有 Python 2）：
   ```bash
   python -m SimpleHTTPServer 8000
   ```

3. **访问网站**
   
   打开浏览器访问：
   - **主页**：http://localhost:8000/
   - **博客**：http://localhost:8000/blog/

4. **停止服务器**
   
   在终端中按 `Ctrl + C` 停止服务器

#### 构建博客（可选）

如果修改了 Markdown 文件或需要重新生成博客：

```bash
cd blog
python3 build.py
```

然后重新启动服务器查看更新。

### 🖥️ 本地开发
1. 启动本地服务器（见上方步骤）
2. 打开浏览器访问 http://localhost:8000/
3. 将鼠标悬停在果实上可以看到动画效果和网站名称
4. 点击果实跳转到对应的网站

### ✍️ 博客写作
1. 在`blog/markdown/`目录下创建新的Markdown文件
2. 运行`python3 blog/build.py`构建博客
3. 或者使用Notion集成功能自动同步文章（见下方说明）

### 🔄 Notion 同步

#### 本地同步
1. 设置环境变量（见 `blog/NOTION-SETUP.md`）
2. 运行同步脚本：
   ```bash
   cd blog
   python3 scripts/notion_sync.py
   ```
3. 同步完成后会自动构建博客

#### GitHub Actions 自动同步
- 每天自动从 Notion 同步已发布的文章
- 自动构建并部署到 GitHub Pages
- 详见 `.github/SETUP.md`

## 自定义链接

要添加或修改果实链接，请编辑`script.js`文件中的`fruitLinks`数组。每个果实对象包含以下属性：
- `id`: 果实的唯一标识符
- `name`: 显示的网站名称
- `url`: 链接地址
- `position`: 果实在树上的位置 (x, y坐标)

示例:
```javascript
{
  id: "fruit1",
  name: "我的博客",
  url: "https://myblog.com",
  position: { x: 120, y: 250 }
}
``` 