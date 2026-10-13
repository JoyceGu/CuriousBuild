# 部署到 Cloudflare Pages（源码私有，网站公开）

## 整体分工

| 谁 | 做什么 |
|---|---|
| **GitHub 私有仓库** | 存源码和文章原稿 |
| **GitHub Actions**（`notion-sync.yml`） | 每天同步 Notion、AI 翻译、重新生成博客页面，提交到 `main` |
| **Cloudflare Workers** | `main` 一有新提交就自动发布网站（免费） |

`python3 build_site.py` 只把网站需要的文件复制到 `dist/`，Cloudflare 只发布这个目录，
所以 Python 脚本、markdown 原稿、workflow 这些都不会出现在网站上。

> 私有仓库的 GitHub Actions 每月有 2000 分钟免费额度，每天同步一次只用几分钟，足够了。

## 第一步：创建 Cloudflare 项目（Workers）

1. 登录 [Cloudflare](https://dash.cloudflare.com/)，进入 **Workers & Pages** → **Create** → 从 GitHub 导入，选择 `JoyceGu/CuriousBuild`。
2. 设置：
   - **Project name**：`curiousbuild`
   - **Build command**：`python3 build_site.py`
   - **Deploy command** / **Preview command**：保持默认（`npx wrangler deploy` / `npx wrangler preview`），发布哪个目录由仓库里的 `wrangler.jsonc` 指定
   - **Enable Preview builds**：打开
3. 部署后在项目 **Settings** → **Domains & Routes** 里把 **workers.dev** 和 **Preview URLs** 设为 Enable。
   网址：`https://curiousbuild.aitoolscollection.workers.dev`

> 合并到 `main` 之前，`main` 上还没有 `build_site.py`，所以第一次正式部署会失败，这是正常的。
> 其他分支的预览链接在项目的 **Deployments** 页面。

如果 `curiousbuild` 这个名字被占用了，Cloudflare 会给一个别的网址。这时把
`blog/scripts/simple_md_converter.py` 里的 `SITE_URL` 改成实际网址（分享链接和 RSS 里会用到）。
想用自己的域名的话，在项目的 **Custom domains** 里添加，同样记得改 `SITE_URL`。

## 第二步：检查并合并

在预览网址上看一遍主页、博客、文章页、中英切换，没问题后把分支合并到 `main`。
Cloudflare 会自动发布正式网站。

## 第三步：把仓库改成私有

1. GitHub 仓库 → **Settings** → **Pages**：如果还开着 GitHub Pages，可以先关掉（改成私有后免费账号也会自动停用）。
2. **Settings** → **General** → 最下面 **Danger Zone** → **Change repository visibility** → **Private**。
3. Cloudflare 通过它的 GitHub App 访问仓库，改成私有后照常自动部署，不用重新设置。

## 注意

- 旧网址 `https://joycegu.github.io/CuriousBuild/` 改成私有后会失效，记得更新你在别处（简历、LinkedIn 等）留的链接。
- 之前用旧网址订阅 RSS 的读者需要换成新地址：`https://curiousbuild.aitoolscollection.workers.dev/blog/feed-zh.xml`（中文）或 `feed-en.xml`（英文）。
