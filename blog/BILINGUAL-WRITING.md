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

> 中文原文不会被自动改写。原文是你的声音，改动要你自己确认，所以润色放在发布前、由你审阅（见下一节）。

### 一次性设置

1. 在 [Claude Console](https://console.anthropic.com/) 创建 API key。
2. 打开 GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret，
   名字填 `ANTHROPIC_API_KEY`。
3. 没有设置这个 secret 时，翻译步骤会自动跳过，其余功能照常。

默认使用 `claude-opus-5-5` 模型，可以用环境变量 `BLOG_AI_MODEL` 换。只想中译英的话，把 workflow 里的 `BLOG_TRANSLATE_DIRECTION` 改成 `zh2en`。

## 发布前润色中文（可选）

想让中文稿也润色一下，又想自己把关：

```bash
pip install anthropic
export ANTHROPIC_API_KEY=你的key
python3 blog/scripts/ai_translate.py polish 我的草稿.md
```

会在 `blog/drafts/`（不会提交到 git）里生成三个文件：

- `我的草稿.polished.zh.md`：轻度润色后的中文（改错字、标点、病句和段落衔接，保留你的语气和表情）
- `我的草稿.en.md`：根据润色稿翻译的英文
- `我的草稿.notes.md`：主要改了哪些地方，方便你逐条确认

满意后把润色稿贴回 Notion 发布即可；英文版可以交给每天的自动翻译，也可以把 `.en.md` 也贴进 Notion 自己发。

不想用命令行的话，也可以直接在 Notion AI 或 Claude 里贴上文章，用类似这样的提示词：
「请轻度润色这篇中文博客：修正错别字、标点和不通顺的句子，保留我的口吻、表情和中英混用的习惯，不要增删内容。然后把润色后的版本翻译成自然地道的英文。」

## 手动配对中英两篇

如果中英两版都是你在 Notion 里自己写的，有两种方式让网站知道它们是一对：

- 在 Notion 数据库加一个 **Translation Key**（文本）列，两篇填同一个值；或者
- 在 `blog/translations.json` 里写上两篇的文件名（不含 `.md`）。

Notion 里还可以加一个 **Language**（单选：`zh` / `en`）列；不填时会根据内容自动识别。
