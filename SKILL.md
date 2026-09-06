---
name: pdf-notes-generator
description: 从 PDF 讲义/教材/试卷自动生成结构化课堂笔记图片。支持康奈尔笔记、对比表格、流程图、重点高亮 4 种模板，自动识别学科、填写挖空、渲染 LaTeX 公式，输出精美 PNG 笔记图。当用户上传 PDF 并要求生成笔记/讲义整理/课堂笔记/复习提纲，或提到"把这个 PDF 做成笔记"时使用。
---

# PDF 课堂笔记生成器

上传 PDF → 提取文本 → AI 生成结构化笔记 → 渲染为精美笔记图片（PNG）。

## 工作流程（5 步）

### 第 1 步：提取 PDF 文本

使用脚本提取 PDF 文本内容：
```bash
python3 <skill_dir>/scripts/extract_pdf.py <pdf_path> --output <output_txt>
```
- 如果提取到的文本为空或极少，提示用户该 PDF 可能是扫描版，建议提供文字版 PDF
- 记录页数和字符数，超过 2 万字的长文档可按章节分段处理

### 第 2 步：生成结构化笔记 JSON

读取 `references/prompts.md` 中的完整提示词，将 PDF 文本填入 `{fileText}`，用户额外要求填入 `{extraRequirements}`，然后**由你自己（AI）** 按照提示词要求输出严格的 JSON 笔记数据。

根据所选模板输出对应的数据结构（详见 `references/data-types.md`）：
- **康奈尔 / 重点高亮** → `NoteData`：`title` / `subject` / `date?` / `summary` / `sections[]`（含 `level`/`heading`/`cues`/`points`）
- **对比表格** → `TableData`：`title` / `subject` / `columns[]` / `rows[]`（含 `dim`/`cells[]`） / `summary`
- **流程图** → `FlowData`：`title` / `subject` / `steps[]`（含 `t`/`d`） / `done`

生成后按 `references/prompts.md` 末尾的质量检查清单逐项核验。

### 第 3 步：选择笔记模板

根据 `references/data-types.md` 中的模板选择策略决定模板：
- 默认 `highlight`（重点高亮）
- 并列概念对比为主 → `table`
- 步骤/流程/推导为主 → `flowchart`
- 用户明确指定 → 按用户要求
- 用户要求"全部"→ 4 种都生成

### 第 4 步：生成 HTML 笔记页面

读取 `references/templates.md`，按照所选模板的 HTML 结构生成完整的 HTML 文件。

技术栈（所有模板共用）：
- **Tailwind CSS**（CDN）：原子化样式
- **marked.js**（CDN）：Markdown 渲染，要点内容通过 `renderMD()` 输出
- **KaTeX**（CDN）：LaTeX 公式渲染

关键要求：
- 页面宽度 1080px，各模板背景遵循 `references/design-system.md`（康奈尔为横线纸，重点高亮为渐变）
- 配色/字体严格遵循 `references/design-system.md`
- 要点内容用 `<div class="md">`（或 `.md.compact` / `.md.hl`）包裹，通过 marked.js 渲染，不要手动转换 `**加粗**`
- `$...$` / `$$...$$` LaTeX 公式在 `renderMD()` 中通过 KaTeX 渲染
- 康奈尔模板表头含课程/日期填写栏，流程图使用 7 色循环步骤卡片，重点高亮的加粗为渐变背景高亮
- 将生成的 JSON 数据填入模板，注意各模板数据结构不同（NoteData / TableData / FlowData）

将 HTML 写入工作目录的临时文件，如 `note_cornell.html`。

### 第 5 步：渲染为 PNG 图片

```bash
python3 <skill_dir>/scripts/render_notes.py <html_path> <output_png> --width 1080
```
- 输出文件名：`{标题}_{模板名}.png`（标题中的特殊字符替换为下划线）
- 生成 4 种模板时，逐个渲染，文件名加模板名后缀
- 渲染完成后通过 `present_files` 交付图片给用户

## 资源索引

| 文件 | 用途 | 何时读取 |
|---|---|---|
| `references/prompts.md` | 完整提示词 + 质量检查清单 | 第 2 步生成笔记前 |
| `references/data-types.md` | NoteData/TableData/FlowData 结构 + 模板类型 + 选择策略 | 第 2、3 步 |
| `references/design-system.md` | 配色/字体/圆角/高亮样式 | 第 4 步生成 HTML 时 |
| `references/templates.md` | 4 种模板的 HTML/CSS 完整规范 | 第 4 步生成 HTML 时 |
| `scripts/extract_pdf.py` | PDF 文本提取 | 第 1 步 |
| `scripts/render_notes.py` | HTML → PNG 截图 | 第 5 步 |

## 注意事项

1. **挖空必须填写**：PDF 中的填空题/下划线挖空，必须根据学科知识补全答案并用加粗标记
2. **LaTeX 安全**：简单符号用 Unicode（× ÷ ± ≥ ≤ → ·），复杂结构才用 `\frac{}` `\sqrt{}` 等
3. **加粗密度**：每条要点 1-2 个加粗短语，不要整段加粗
4. **不要出现"AI 生成"字样**
5. **长 PDF 处理**：超过 2 万字时，可先生成大纲再分章节生成，或提示用户文件过长
6. **截图失败兜底**：如果 playwright 渲染失败，检查 HTML 是否有语法错误，或增加 `--wait` 时间
7. **学科识别**：必须从标准学科名中选择（语文/数学/英语/物理/化学/生物/历史/地理/政治/综合）
8. **客户端渲染等待**：HTML 使用 marked.js + KaTeX 客户端渲染，截图前需等待至少 1500ms，公式较多时增加 `--wait 2500`
9. **字体规范（强制）**：汉字使用 `Microsoft YaHei`（微软雅黑），英文和数字使用 `Times New Roman`，数学公式使用 KaTeX 默认字体。CSS 写法：`font-family:'Times New Roman','Microsoft YaHei',serif`（Times New Roman 在前匹配英文数字，中文回退到微软雅黑）。禁止使用 `font-mono`/`ui-monospace` 等覆盖数字字体。
