# 双语博客写作指南

网站右上角有 **中文 / EN** 切换按钮。会记住你上次的选择，第一次访问时按浏览器语言决定。

- **主页**：标题、提示文字、果实标签都会切换（中文名称在 `fruits-config.js` 的 `name_zh` / `shortName_zh` 里改）。
- **博客列表**：有中英两个版本的文章只显示当前语言那篇；只有一种语言的文章两边都显示，带一个小标签（`中文` / `EN`）。
- **文章页**：有译文时显示「Read in English →」/「阅读中文版 →」，点右上角切换按钮也会直接跳到另一版。AI 翻译的文章会标注出来。

## 推荐流程：用中文写，自动出英文版

1. **在 Notion 用中文写**，跟以前一样把 Status 改成 `Published`。
2. 每天的 GitHub Action 同步 Notion 后会运行 `blog/scripts/ai_translate.py`：
   - 给还没有英文版的中文文章生成**润色过的英文译文**（反过来也会给英文文章生成中文版）；
   - 原文没改就不会重复翻译（按内容 hash 判断），原文改了会自动更新译文；
   - 原文在 Notion 下线，译文也会一起删除；
   - 你自己写的译文永远不会被覆盖。
3. 如果某篇不想自动翻译，在 markdown 的 frontmatter 里加 `ai_translate: false`。

> 中文原文不会被改动，只有译文会被润色。

### 一次性设置（用 Claude 订阅，不需要 API key）

翻译走你的 Claude Pro / Max 订阅额度，不额外付费（会占用订阅的使用量）。

1. 在自己电脑上（装好并登录 Claude Code 后）运行：
   ```bash
   claude setup-token
   ```
   按提示登录，会输出一个长期有效的 token。
2. 打开 GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret，
   名字填 `CLAUDE_CODE_OAUTH_TOKEN`，值填刚才的 token。
3. 没有设置这个 secret 时，翻译步骤会自动跳过，其余功能照常。

> 以后如果有了 Anthropic API key，也可以改用 `ANTHROPIC_API_KEY` secret，两个都配置时优先用 API key。

本地手动翻译：登录过 Claude Code 的电脑上直接运行 `python3 blog/scripts/ai_translate.py`。

默认使用 `claude-sonnet-5-5` 模型，可以用环境变量 `BLOG_AI_MODEL` 换。只想中译英的话，把 workflow 里的 `BLOG_TRANSLATE_DIRECTION` 改成 `zh2en`。

## 手动配对中英两篇

如果中英两版都是你在 Notion 里自己写的，有两种方式让网站知道它们是一对：

- 在 Notion 数据库加一个 **Translation Key**（文本）列，两篇填同一个值；或者
- 在 `blog/translations.json` 里写上两篇的文件名（不含 `.md`）。

Notion 里还可以加一个 **Language**（单选：`zh` / `en`）列；不填时会根据内容自动识别。

## 邮件订阅

博客的「订阅」按钮接的是 [Buttondown](https://buttondown.com)（邮件订阅服务，免费档就能开始用）：

1. 注册 Buttondown 账号，记下你的用户名。
2. 把用户名填进 `blog/subscribe-config.js` 的 `buttondownUsername`，提交后订阅按钮就会出现。没填之前按钮是隐藏的，只显示 RSS。
3. 读者填邮箱后会收到 Buttondown 的确认邮件，确认后就进入你的订阅者列表（在 Buttondown 后台查看和导出）。
4. 想让新文章自动发邮件：在 Buttondown 里开启 RSS-to-email，订阅源填
   `https://curiousbuild.aitoolscollection.workers.dev/blog/feed-zh.xml`（中文）或 `feed-en.xml`（英文）。
   这两个订阅源里每篇文章只出现一次，订阅者不会因为中英两版收到重复邮件。
   这个功能包含在哪个价格档位，请以 Buttondown 价格页为准。

RSS 订阅源：`feed-zh.xml`（中文）、`feed-en.xml`（英文）、`feed.xml`（全部文章，兼容旧的订阅）。博客上的 RSS 链接会跟着当前语言切换。
