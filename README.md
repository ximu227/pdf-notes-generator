# pdf-notes-generator

从 PDF 讲义/教材/试卷自动生成结构化课堂笔记图片的豆包技能。

支持 **康奈尔笔记、对比表格、流程图、重点高亮** 4 种模板，自动识别学科、填写挖空、渲染 LaTeX 公式，输出精美 PNG 笔记图。

## 功能特性

- 📄 自动提取 PDF 文本内容
- 🎯 AI 生成结构化笔记（标题 / 学科 / 小结 / 多级章节）
- 📝 4 种笔记模板：康奈尔、对比表格、流程图、重点高亮
- ✏️ 自动补全 PDF 中的填空题挖空
- 🧮 LaTeX 公式渲染（KaTeX）
- 🎨 暖米白 + 薄暮紫设计系统，输出 1080px 宽 PNG

## 安装方法

### 1. 克隆或下载本仓库

```bash
git clone https://github.com/ximu227/pdf-notes-generator.git
```

### 2. 放到豆包用户技能目录

将整个 `pdf-notes-generator` 文件夹复制到豆包的用户技能目录：

- **Linux / macOS**：`~/.super_doubao/super-doubao-runtime/workspace/.user_skills/`
- **Windows**：对应工作目录下的 `.user_skills/` 文件夹

### 3. 安装 Python 依赖

```bash
pip install pdfplumber playwright
playwright install chromium
```

### 4. 重启豆包会话

技能会被自动识别加载。上传 PDF 并说"把这个 PDF 做成笔记"即可触发。

## 目录结构

```
pdf-notes-generator/
├── SKILL.md                  # 技能入口（工作流程说明）
├── README.md                 # 本文件
├── scripts/
│   ├── extract_pdf.py        # PDF 文本提取脚本
│   └── render_notes.py       # HTML → PNG 渲染脚本
└── references/
    ├── prompts.md            # 笔记生成提示词 + 质量检查清单
    ├── data-types.md         # NoteData 数据结构 + 模板选择策略
    ├── templates.md          # 4 种模板的 HTML/CSS 规范
    └── design-system.md      # 配色 / 字体 / 设计系统
```

## 使用方式

在豆包中上传 PDF 文件，然后说类似以下的话：

- "把这个 PDF 做成课堂笔记"
- "帮我整理这份讲义，生成复习提纲"
- "用康奈尔笔记格式整理这份试卷"
- "全部模板都生成一份"

## 依赖

- Python 3.10+
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF 文本提取
- [Playwright](https://playwright.dev/) + Chromium — HTML 截图渲染

## License

MIT
