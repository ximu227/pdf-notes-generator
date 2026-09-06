# 4 种笔记模板 HTML/CSS 实现规范

所有模板共用：页面宽度 1080px，暖米白背景 `#FAF8F5`，内边距 40px。
标题区：顶部品牌渐变装饰条 + 标题 + 学科标签。

---

## 1. 康奈尔笔记 (cornell)

### 布局
```
┌─────────────────────────────────────────┐
│  [渐变条]  标题              [学科标签]  │
├──────────┬──────────────────────────────┤
│ 关键词    │  一级标题                     │
│ 关键词    │  · 要点1（**加粗**高亮）      │
│ 关键词    │  · 要点2                      │
│          │  · 要点3                      │
├──────────┴──────────────────────────────┤
│  📝 课堂小结                              │
│  summary 内容                            │
└─────────────────────────────────────────┘
```

### HTML 结构
```html
<div class="note cornell">
  <header class="note-header">
    <div class="header-bar"></div>
    <h1>{{title}}</h1>
    <span class="subject-tag">{{subject}}</span>
  </header>
  {{#each sections}}
  <section class="cornell-block">
    <div class="cue-column">
      {{#each cues}}<span class="cue-tag">{{this}}</span>{{/each}}
    </div>
    <div class="content-column">
      <h2 class="section-heading level-{{level}}">{{heading}}</h2>
      <ul class="points">
        {{#each points}}<li class="point">{{this}}</li>{{/each}}
      </ul>
    </div>
  </section>
  {{/each}}
  <footer class="note-summary">
    <div class="summary-label">📝 课堂小结</div>
    <p>{{summary}}</p>
  </footer>
</div>
```

### CSS 要点
- `.cue-column`：宽度 28%，背景 `#F4F0E8`，圆角 12px，padding 20px
- `.cue-tag`：inline-block，背景白色，薄暮紫文字，圆角 6px，padding 4px 10px，margin 4px
- `.content-column`：宽度 72%，padding 0 0 0 24px
- `.section-heading`：薄暮紫，左边框 4px  solid #7C3AED，padding-left 12px
- `.point`：行高 1.8，margin-bottom 10px，列表样式用 "·"
- `.note-summary`：背景 `rgba(124,58,237,0.06)`，边框左 4px #7C3AED，圆角 12px，padding 20px

---

## 2. 对比表格 (table)

### 布局
```
┌─────────────────────────────────────────┐
│  [渐变条]  标题              [学科标签]  │
├─────────────────────────────────────────┤
│  一级标题（表名）                         │
│  ┌─────────┬─────────┬─────────┐        │
│  │ 列头1    │ 列头2    │ 列头3    │        │
│  ├─────────┼─────────┼─────────┤        │
│  │ 行标题   │ 内容     │ 内容     │        │
│  │ 行标题   │ 内容     │ 内容     │        │
│  └─────────┴─────────┴─────────┘        │
├─────────────────────────────────────────┤
│  📝 课堂小结                              │
└─────────────────────────────────────────┘
```

### 数据映射规则
- 每个 level 1 → 一张独立表格，heading 为表名
- level 1 下的 level 2 → 表头列（第一列固定为"对比项"）
- level 2 下的 level 3 → 行标题
- level 3 的 points → 对应单元格内容（取第一条，多条用 <br> 连接）
- 如果没有 level 2/3 嵌套，则将 level 1 的 points 转为两列："要点" + "说明"

### HTML 结构
```html
<div class="note table">
  <header class="note-header">...</header>
  {{#each sections(level=1)}}
  <div class="table-block">
    <h2 class="table-title">{{heading}}</h2>
    <table class="compare-table">
      <thead><tr><th>对比项</th>{{#each children(level=2)}}<th>{{heading}}</th>{{/each}}</tr></thead>
      <tbody>
        {{#each rows}}
        <tr><td class="row-header">{{rowName}}</td>{{#each cells}}<td>{{content}}</td>{{/each}}</tr>
        {{/each}}
      </tbody>
    </table>
  </div>
  {{/each}}
  <footer class="note-summary">...</footer>
</div>
```

### CSS 要点
- `table.compare-table`：width 100%，border-collapse: collapse，圆角 12px，overflow hidden
- `thead th`：背景 `#7C3AED`，白色文字，padding 12px 16px，font-weight 600
- `tbody td`：padding 12px 16px，border-bottom 1px solid #E7E2D6
- `tbody tr:nth-child(even)`：背景 `#F4F0E8`
- `.row-header`：font-weight 600，颜色 `#7C3AED`，背景 `rgba(124,58,237,0.04)`

---

## 3. 流程图笔记 (flowchart)

### 布局
```
┌─────────────────────────────────────────┐
│  [渐变条]  标题              [学科标签]  │
├─────────────────────────────────────────┤
│  一级标题（流程名）                        │
│  ┌──────┐   →   ┌──────┐   →   ┌──────┐ │
│  │ 步骤1 │       │ 步骤2 │       │ 步骤3 │ │
│  └──────┘       └──────┘       └──────┘ │
│                    ↓                     │
│             ┌────────────┐               │
│             │  决策/分支   │               │
│             └────────────┘               │
├─────────────────────────────────────────┤
│  📝 课堂小结                              │
└─────────────────────────────────────────┘
```

### 数据映射规则
- 每个 level 1 → 一条流程线，heading 为流程名
- level 1 下的 level 2 → 流程步骤卡片，按顺序横向排列，用 → 连接
- level 2 下的 points → 步骤卡片内的详细说明
- 如果 level 2 下有 level 3，则 level 3 作为分支/子步骤，用 ↓ 连接到下方

### HTML 结构
```html
<div class="note flowchart">
  <header class="note-header">...</header>
  {{#each sections(level=1)}}
  <div class="flow-block">
    <h2 class="flow-title">{{heading}}</h2>
    <div class="flow-chain">
      {{#each children(level=2)}}
      <div class="flow-step">
        <div class="step-title">{{heading}}</div>
        <ul class="step-points">{{#each points}}<li>{{this}}</li>{{/each}}</ul>
      </div>
      {{#if notLast}}<div class="flow-arrow">→</div>{{/if}}
      {{/each}}
    </div>
  </div>
  {{/each}}
  <footer class="note-summary">...</footer>
</div>
```

### CSS 要点
- `.flow-chain`：display flex，align-items flex-start，justify-content center，flex-wrap wrap，gap 0
- `.flow-step`：背景白色，border 2px solid #7C3AED，border-radius 12px，padding 16px，min-width 160px，max-width 220px，box-shadow 0 2px 8px rgba(124,58,237,0.1)
- `.step-title`：font-weight 600，color #7C3AED，text-align center，margin-bottom 8px，font-size 15px
- `.step-points`：font-size 13px，color #555，line-height 1.6，padding-left 16px
- `.flow-arrow`：font-size 24px，color #F472B6，align-self center，padding 0 8px，font-weight bold
- 步骤过多时自动换行，换行后的箭头用 ↓ 表示纵向连接

---

## 4. 重点高亮 (highlight)

### 布局
```
┌─────────────────────────────────────────┐
│  [渐变条]  标题              [学科标签]  │
├─────────────────────────────────────────┤
│  ┃ 一级标题（卡片）                       │
│  ┃  · 要点1（**加粗**高亮）               │
│  ┃  · 要点2                               │
│  ┃  · 要点3                               │
│  ┠────────────────────────────────────── │
│  ┃ 一级标题（卡片）                       │
│  ┃  · 要点1                               │
│  ...                                     │
├─────────────────────────────────────────┤
│  📝 课堂小结                              │
└─────────────────────────────────────────┘
```

### HTML 结构
```html
<div class="note highlight">
  <header class="note-header">...</header>
  {{#each sections(level=1)}}
  <div class="highlight-card">
    <div class="card-accent"></div>
    <div class="card-body">
      <h2 class="card-title">{{heading}}</h2>
      <div class="card-cues">{{#each cues}}<span class="cue-chip">{{this}}</span>{{/each}}</div>
      <ul class="card-points">
        {{#each points}}<li class="point">{{this}}</li>{{/each}}
      </ul>
      {{#each children(level=2)}}
      <div class="sub-section">
        <h3 class="sub-heading">{{heading}}</h3>
        <ul class="sub-points">{{#each points}}<li>{{this}}</li>{{/each}}</ul>
      </div>
      {{/each}}
    </div>
  </div>
  {{/each}}
  <footer class="note-summary">...</footer>
</div>
```

### CSS 要点
- `.highlight-card`：背景白色，border-radius 14px，margin-bottom 20px，overflow hidden，box-shadow 0 2px 12px rgba(0,0,0,0.04)，display flex
- `.card-accent`：width 6px，background 渐变 `linear-gradient(180deg, #7C3AED, #F472B6)`，flex-shrink 0
- `.card-body`：padding 24px，flex 1
- `.card-title`：font-size 20px，font-weight 600，color #1C1B1F，margin-bottom 8px
- `.cue-chip`：inline-block，background `rgba(244,114,182,0.12)`，color #F472B6，border-radius 20px，padding 2px 12px，font-size 12px，margin-right 6px
- `.card-points .point`：line-height 1.8，margin-bottom 8px
- `.sub-heading`：font-size 16px，color #7C3AED，margin-top 16px，margin-bottom 8px，font-weight 600

---

## 通用组件

### note-header（所有模板共用）
```html
<header class="note-header">
  <div class="header-bar" style="height:4px;background:linear-gradient(90deg,#7C3AED,#F472B6);border-radius:2px;margin-bottom:20px;"></div>
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <h1 style="font-size:28px;font-weight:700;color:#1C1B1F;margin:0;">{{title}}</h1>
    <span class="subject-tag" style="background:#7C3AED;color:#fff;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:500;">{{subject}}</span>
  </div>
</header>
```

### note-summary（所有模板共用）
```html
<footer class="note-summary" style="background:rgba(124,58,237,0.06);border-left:4px solid #7C3AED;border-radius:0 12px 12px 0;padding:20px 24px;margin-top:24px;">
  <div style="font-weight:600;color:#7C3AED;margin-bottom:8px;font-size:15px;">📝 课堂小结</div>
  <p style="margin:0;color:#444;line-height:1.7;">{{summary}}</p>
</footer>
```

### 加粗高亮（**text** 转换）
将 `**内容**` 替换为：
```html
<strong style="color:#7C3AED;background:rgba(124,58,237,0.08);padding:1px 5px;border-radius:4px;font-weight:600;">内容</strong>
```

### LaTeX 渲染
HTML 中通过 MathJax 或 KaTeX CDN 渲染 `$...$` 和 `$$...$$`。在 `<head>` 中引入：
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});"></script>
```
截图前等待 KaTeX 渲染完成（`window.katex` 存在且 `.katex` 元素数量 > 0）。

## 输出图片规格
- 宽度：1080px
- 高度：自适应内容（全页截图）
- 格式：PNG
- 背景：暖米白 `#FAF8F5`
- 文件名：`{title}_{模板名}.png`
