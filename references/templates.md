# 4 种笔记模板 HTML/CSS 完整规范

## 通用技术栈（所有模板共用）

每个模板生成**独立的完整 HTML 文件**，必须在 `<head>` 中引入以下 CDN：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js"></script>
<script>
tailwind.config = {
  theme: { extend: { colors: {
    primary: { DEFAULT:'#7C3AED', dark:'#6D28D9' },
    accent: { DEFAULT:'#F472B6' },
    ink:'#1C1B1F', muted:'#78716C', cardborder:'#E7E2D6'
  }}}
}
</script>
<style>
  body { font-family:'Times New Roman','Microsoft YaHei',serif; background:#FAF8F5; color:#1C1B1F; margin:0; }
  .note-page { width:100%; min-height:600px; box-sizing:border-box; }
  .md { font-size:14px; line-height:1.75; }
  .md p { margin:6px 0; }
  .md.compact { font-size:12.5px; line-height:1.65; }
  .md.hl { font-size:15px; line-height:1.85; }
  .md strong { font-weight:600; color:#7C3AED; }
  .md em { font-style:italic; color:#F472B6; }
  .md.hl strong { font-weight:700; background:linear-gradient(to right,#FCE7F3,#EDE9FE); color:#7C3AED; padding:1px 6px; border-radius:4px; margin:0 2px; display:inline-block; }
  .md.hl em { font-style:italic; font-weight:600; color:#F472B6; background:#FCE7F3; padding:0 4px; border-radius:4px; margin:0 2px; }
  .md ul { list-style:disc; margin:6px 0; padding-left:20px; color:rgba(124,58,237,.4); }
  .md ul li { color:#1C1B1F; line-height:1.7; margin:2px 0; }
  .md ol { list-style:decimal; margin:6px 0; padding-left:22px; }
  .md ol li { line-height:1.7; margin:2px 0; }
  .md blockquote { border-left:2px solid rgba(244,114,182,.6); padding-left:12px; margin:6px 0; color:rgba(28,27,31,.8); font-style:italic; }
  .md code { background:rgba(120,113,108,.15); border-radius:4px; padding:1px 4px; font-size:12.5px; font-family:'Times New Roman','Microsoft YaHei',serif; color:#1C1B1F; }
  .md .katex-display { margin:8px 0; overflow-x:auto; }
</style>
</head>
```

## 通用渲染脚本（所有模板共用，放在 `</body>` 前）

```javascript
function renderMD(text) {
  if (!text) return '';
  // 先提取并渲染 LaTeX（避免 marked 把 < > 转义为 &lt; &gt;）
  const mathBlocks = [];
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (m, tex) => {
    try {
      mathBlocks.push('<div>' + katex.renderToString(tex, {throwOnError:false, displayMode:true}) + '</div>');
      return `@@MATH${mathBlocks.length-1}@@`;
    } catch(e){ return m; }
  });
  text = text.replace(/\$([^\$\n]+?)\$/g, (m, tex) => {
    try {
      mathBlocks.push(katex.renderToString(tex, {throwOnError:false}));
      return `@@MATH${mathBlocks.length-1}@@`;
    } catch(e){ return m; }
  });
  // 再解析 Markdown
  let html = marked.parse(text);
  // 还原 LaTeX 渲染结果
  html = html.replace(/@@MATH(\d+)@@/g, (m, i) => mathBlocks[parseInt(i)]);
  return html;
}
function stripMd(s){
  return s.replace(/\*\*([^*]+)\*\*/g,'$1').replace(/`([^`]+)`/g,'$1')
    .replace(/\$([^$]+)\$/g,'$1').replace(/\s+/g,' ').trim();
}
```

渲染要点时，将 points 数组的每条通过 `renderMD(point)` 输出；标题中的 markdown 符号用 `stripMd(heading)` 去除。

---

## 1. 康奈尔笔记 (cornell)

### 布局
```
┌─────────────────────────────────────────────┐
│ [横线纸背景]                                  │
│  📖图标  第9讲 相交线与平行线      课程: 数学  │
│                              日期: 2026/7/2  │
│  ─────────────────────────────────────────  │
│ ┌──────────┬──────────────────────────────┐ │
│ │关键词/CUES│  ① 一、两线四角               │ │
│ │ 对顶角    │  · 对顶角：两条直线相交...    │ │
│ │ 邻补角    │  · 对顶角性质：对顶角相等...  │ │
│ │ 垂直      │  · 邻补角：有公共顶点...      │ │
│ ├──────────┼──────────────────────────────┤ │
│ │关键词/CUES│  ② 二、平行线的判定与性质     │ │
│ │ ...      │  · ...                       │ │
│ └──────────┴──────────────────────────────┘ │
│ ┌─────────────────────────────────────────┐ │
│ │ 📝 总结 / SUMMARY                        │ │
│ │ summary 内容                             │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### HTML 结构（body 部分）

```html
<body>
<div class="max-w-4xl mx-auto px-4 py-8">
  <div class="note-page rounded-2xl shadow-sm overflow-hidden bg-white"
       style="background-image:repeating-linear-gradient(transparent,transparent 35px,#E7E2D6 35px,#E7E2D6 36px); padding:40px;">

    <!-- 表头 -->
    <div class="flex items-end justify-between pb-3 mb-4 border-b-2 border-[#7C3AED] gap-4">
      <div class="flex items-center gap-3 min-w-0">
        <div class="h-10 w-10 rounded-xl flex items-center justify-center text-white shrink-0"
             style="background:linear-gradient(135deg,#7C3AED,#F472B6)">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        </div>
        <h1 class="text-3xl font-bold text-ink break-words leading-tight">{title}</h1>
      </div>
      <div class="text-right text-xs text-muted space-y-0.5 shrink-0">
        <div>课程：<span class="ml-1 text-ink border-b border-dotted border-muted inline-block min-w-[100px]">{subject}</span></div>
        <div>日期：<span class="ml-1 text-ink border-b border-dotted border-muted inline-block min-w-[100px]">{date}</span></div>
      </div>
    </div>

    <!-- 两栏 -->
    <div class="flex flex-col md:flex-row gap-0 border-2 border-[#7C3AED]/30 rounded-2xl overflow-hidden bg-white/60">
      <!-- 左侧关键词 -->
      <div class="w-full md:w-[28%] md:min-w-[200px] border-b-2 md:border-b-0 md:border-r-2 border-[#7C3AED]/30 p-4">
        <div class="flex items-center justify-center gap-1.5 text-[11px] font-bold tracking-widest uppercase text-[#7C3AED] mb-3 py-1 bg-[#7C3AED]/10 rounded">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>
          关键词 / CUES
        </div>
        <div class="space-y-4">
          {#each sections}
          <div>
            <div class="text-sm font-semibold text-ink mb-1.5 border-l-2 border-[#F472B6] pl-1.5 break-words">{index}. {stripMd(heading)}</div>
            <ul class="space-y-1 ml-2 list-none p-0">
              {#each cues}<li class="text-[13px] text-ink leading-relaxed flex items-baseline gap-1.5"><span class="text-[#F472B6] font-bold">·</span><span class="flex-1">{cue}</span></li>{/each}
            </ul>
          </div>
          {/each}
        </div>
      </div>
      <!-- 右侧详细笔记 -->
      <div class="flex-1 min-w-0 p-5">
        <div class="text-[11px] font-bold tracking-widest uppercase text-[#7C3AED] mb-3 text-center py-1 bg-[#7C3AED]/10 rounded">详细笔记</div>
        <div class="space-y-4">
          {#each sections}
          <div>
            <h2 class="text-lg font-semibold text-ink mb-2 flex items-center gap-2">
              <span class="h-5 w-5 rounded-md text-white text-[10px] flex items-center justify-center font-bold shrink-0" style="background:linear-gradient(135deg,#7C3AED,#F472B6)">{index}</span>
              {stripMd(heading)}
            </h2>
            <div class="space-y-1.5 ml-7">
              {#each points}<div class="text-[14px] text-ink leading-relaxed flex items-baseline gap-1.5"><span class="text-[#F472B6] font-bold">·</span><div class="flex-1 min-w-0 md">{renderMD(point)}</div></div>{/each}
            </div>
          </div>
          {/each}
        </div>
      </div>
    </div>

    <!-- 总结 -->
    <div class="mt-4 border-2 border-[#F472B6]/40 rounded-2xl p-4 bg-[#F472B6]/5">
      <div class="flex items-center gap-2 mb-2">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F472B6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 .98 0 1 0 1 1v1c0 1-1 2-2 2s-.98.03-.98 1.031V20c0 1 0 1 .98 1z"/></svg>
        <span class="text-[11px] font-bold tracking-widest uppercase text-[#F472B6]">总结 / SUMMARY</span>
      </div>
      <div class="md text-[14px] leading-relaxed text-ink">{renderMD(summary)}</div>
    </div>

  </div>
</div>
</body>
```

### 关键样式说明
- 背景：横线纸效果 `repeating-linear-gradient(transparent,transparent 35px,#E7E2D6 35px,#E7E2D6 36px)`
- 表头：渐变图标方块 + 大标题 + 右侧课程/日期（虚线下划线填写样式）
- 两栏容器：`border-2 border-[#7C3AED]/30 rounded-2xl`，左栏 28% 宽
- 章节编号：渐变圆角小方块 `h-5 w-5 rounded-md`
- 要点前缀：`·` 用 `#F472B6` 粉色
- 总结区：粉色边框 + 浅粉背景 + 引号图标

---

## 2. 对比表格 (table)

### 布局
```
┌─────────────────────────────────────────┐
│ 🔲图标                                   │
│ 光合作用与呼吸作用对比                    │
│ ▓▓▓ 渐变装饰条                           │
│ ┌─────────────────────────────────────┐ │
│ │ 维度  │ 光合作用    │ 呼吸作用      │ │ ← 渐变表头
│ ├─────────────────────────────────────┤ │
│ │ ①场所 │ ● 叶绿体中  │ ● 线粒体中    │ │
│ │ ②条件 │ ● 需要光    │ ● 有光无光    │ │
│ │ ...   │             │               │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ 📖 一句话总结                        │ │
│ │ summary 内容                        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 数据结构
表格模板使用 `TableData`：
- `title`：笔记标题
- `subject`：学科
- `columns`：表头列名数组（如 `["光合作用","呼吸作用"]`），第一列固定为"维度"
- `rows`：行数组，每行 `{ dim: "维度名", cells: ["列1内容","列2内容",...] }`
- `summary`：一句话总结

### HTML 结构（body 部分）

```html
<body>
<div class="max-w-4xl mx-auto px-4 py-8">
  <div class="note-page rounded-2xl shadow-sm bg-[#FAF8F5]" style="padding:40px;">

    <div class="flex items-center gap-3 mb-1">
      <div class="h-10 w-10 rounded-xl flex items-center justify-center text-white"
           style="background:linear-gradient(135deg,#7C3AED,#F472B6)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg>
      </div>
    </div>
    <h1 class="text-3xl font-bold text-ink leading-tight mb-1">{title}</h1>
    <div class="h-1 w-24 rounded-full mb-6" style="background:linear-gradient(to right,#7C3AED,#F472B6)"></div>

    <div class="rounded-2xl border-2 border-cardborder overflow-hidden bg-white shadow-sm">
      <table class="w-full border-collapse">
        <thead>
          <tr class="text-white" style="background:linear-gradient(to right,#7C3AED,#6D28D9)">
            <th class="px-4 py-3 text-left text-sm font-bold border-r border-white/20 w-[140px]">维度</th>
            {#each columns}<th class="px-4 py-3 text-left text-sm font-semibold border-r border-white/20">{column}</th>{/each}
          </tr>
        </thead>
        <tbody>
          {#each rows}
          <tr class="{index%2===0?'bg-[#FAF8F5]':'bg-[#F4F0E8]'}">
            <td class="px-4 py-3 text-sm font-semibold text-[#7C3AED] border-r border-cardborder align-top">
              <div class="flex items-start gap-1.5">
                <span class="h-5 w-5 rounded bg-[#7C3AED] text-white text-[10px] flex items-center justify-center font-bold shrink-0 mt-0.5">{index}</span>
                {dim}
              </div>
            </td>
            {#each cells}<td class="px-4 py-3 text-sm text-ink border-r border-cardborder align-top leading-relaxed">
              <div class="flex items-start gap-1.5"><span class="text-[#F472B6] mt-1 shrink-0">●</span><div class="flex-1 md compact">{renderMD(cell)}</div></div>
            </td>{/each}
          </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="mt-6 rounded-xl border-2 border-[#F472B6]/30 bg-[#F472B6]/5 p-4">
      <div class="flex items-center gap-2 mb-1.5">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F472B6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        <span class="text-xs font-bold tracking-widest uppercase text-[#F472B6]">一句话总结</span>
      </div>
      <div class="md text-sm leading-relaxed text-ink">{renderMD(summary)}</div>
    </div>

  </div>
</div>
</body>
```

### 关键样式说明
- 表头：图标 + 大标题 + 24px 宽渐变装饰条
- 表头行：渐变背景 `linear-gradient(to right,#7C3AED,#6D28D9)`，白字
- 维度列：紫色文字 + 紫色编号圆角方块
- 内容单元格：粉色 `●` 圆点前缀，使用 `.md.compact` 紧凑渲染
- 行交替：偶数行 `#FAF8F5`，奇数行 `#F4F0E8`

---

## 3. 流程图笔记 (flowchart)

### 布局
```
┌─────────────────────────────────────────┐
│ 🔀图标                                   │
│ 解一元一次方程的完整步骤                  │
│ ▓▓▓ 渐变装饰条                           │
│                                           │
│   ① ──┐                                  │
│   粉色圆 │  [粉色卡片] 去分母             │
│         │    · 方程两边同乘最小公倍数...  │
│         ↓  (虚线箭头)                     │
│   ② ──┐                                  │
│   蓝色圆 │  [蓝色卡片] 去括号             │
│         │    · 利用乘法分配律...          │
│         ↓                                │
│   ...                                    │
│   ✓ ──┐                                  │
│ 渐变圆  │  [渐变卡片] 完成 / Done         │
│         │    done 内容                    │
└─────────────────────────────────────────┘
```

### 数据结构
流程图模板使用 `FlowData`：
- `title`：笔记标题
- `subject`：学科
- `steps`：步骤数组，每个 `{ t: "步骤名", d: "详细说明" }`
- `done`：完成后的总结/易错提醒

### 步骤颜色循环（7 色）
```javascript
const STEP_COLORS=[
  {bg:'#FCE7F3',border:'#F472B6',text:'#9D174D'},
  {bg:'#DBEAFE',border:'#3B82F6',text:'#1E40AF'},
  {bg:'#D1FAE5',border:'#10B981',text:'#065F46'},
  {bg:'#FEF3C7',border:'#F59E0B',text:'#92400E'},
  {bg:'#EDE9FE',border:'#7C3AED',text:'#5B21B6'},
  {bg:'#CFFAFE',border:'#06B6D4',text:'#155E75'},
  {bg:'#FFE4E6',border:'#F43F5E',text:'#9F1239'}
];
```
第 i 步使用 `STEP_COLORS[i % 7]`。

### HTML 结构（body 部分）

```html
<body>
<div class="max-w-4xl mx-auto px-4 py-8">
  <div class="note-page rounded-2xl shadow-sm bg-[#FAF8F5]" style="padding:40px;">

    <div class="flex items-center gap-3 mb-1">
      <div class="h-10 w-10 rounded-xl flex items-center justify-center text-white"
           style="background:linear-gradient(135deg,#7C3AED,#F472B6)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>
      </div>
    </div>
    <h1 class="text-3xl font-bold text-ink leading-tight mb-1">{title}</h1>
    <div class="h-1 w-24 rounded-full mb-8" style="background:linear-gradient(to right,#7C3AED,#F472B6)"></div>

    <div class="relative">
      {#each steps}
      <div class="relative">
        <div class="flex items-stretch gap-4">
          <div class="flex flex-col items-center pt-2">
            <div class="h-12 w-12 rounded-full flex items-center justify-center text-white text-base font-bold shadow-md" style="background-color:{color.border}">{index}</div>
          </div>
          <div class="flex-1 min-w-0 rounded-2xl border-2 p-4 shadow-sm" style="background-color:{color.bg};border-color:{color.border}">
            <h3 class="text-lg font-bold mb-2" style="color:{color.text}">{t}</h3>
            <div class="space-y-1.5">
              <div class="text-sm text-ink leading-relaxed flex items-start gap-2">
                <span class="shrink-0 mt-2 h-1.5 w-1.5 rounded-full" style="background-color:{color.border}"></span>
                <div class="flex-1 md compact">{renderMD(d)}</div>
              </div>
            </div>
          </div>
        </div>
        {#if notLast}
        <div class="flex justify-start ml-[22px] my-1">
          <svg width="8" height="32" viewBox="0 0 8 32">
            <line x1="4" y1="0" x2="4" y2="24" stroke="{color.border}" stroke-width="2" stroke-dasharray="3 3"/>
            <polygon points="2,24 6,24 4,32" fill="{color.border}"/>
          </svg>
        </div>
        {/if}
      </div>
      {/each}

      <div class="flex items-stretch gap-4 mt-2">
        <div class="flex flex-col items-center pt-2">
          <div class="h-12 w-12 rounded-full flex items-center justify-center text-white shadow-md" style="background:linear-gradient(135deg,#7C3AED,#F472B6)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
        </div>
        <div class="flex-1 rounded-2xl border-2 border-[#7C3AED] p-4" style="background:linear-gradient(to right,rgba(124,58,237,.1),rgba(244,114,182,.1))">
          <h3 class="text-lg font-bold text-[#7C3AED] mb-1">完成 / Done</h3>
          <div class="md text-sm text-ink">{renderMD(done)}</div>
        </div>
      </div>
    </div>

  </div>
</div>
</body>
```

### 关键样式说明
- 垂直时间线布局：左侧圆形编号 + 右侧卡片
- 编号圆：`h-12 w-12 rounded-full`，使用步骤对应颜色
- 卡片：对应浅色背景 + 同色边框 `border-2`，圆角 `rounded-2xl`
- 步骤间连接：`ml-[22px]` 对齐圆心，虚线 + 箭头 SVG
- 完成卡片：渐变背景 + 紫色边框 + 对勾图标

---

## 4. 重点高亮 (highlight)

### 布局
```
┌─────────────────────────────────────────┐
│ [渐变背景 #FAF8F5→#F4F0E8]               │
│  ✨图标  数学                             │
│  百分数核心知识点                        │
│  ▓▓▓ 渐变装饰条                           │
│                                           │
│  ① 一、百分数的意义                       │
│     ● **百分数**表示一个数是另一个数...   │ ← 渐变高亮加粗
│     ● 百分数通常用 **%** 表示...          │
│     ● 百分数只表示两个量的**倍比关系**... │
│                                           │
│  ② 二、百分数与小数、分数的互化           │
│     ● ...                                 │
│                                           │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ 本节核心回顾                       │ │
│ │ summary 内容                        │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### HTML 结构（body 部分）

```html
<body>
<div class="max-w-4xl mx-auto px-4 py-8">
  <div class="note-page rounded-2xl shadow-sm" style="background:linear-gradient(135deg,#FAF8F5 0%,#F4F0E8 100%); padding:48px;">

    <div class="flex items-center gap-3 mb-2">
      <div class="h-10 w-10 rounded-xl flex items-center justify-center text-white"
           style="background:linear-gradient(135deg,#7C3AED,#F472B6)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
      </div>
      <div class="text-xs text-muted tracking-widest uppercase">{subject}</div>
    </div>
    <h1 class="text-4xl font-bold text-ink leading-tight mb-1">{title}</h1>
    <div class="h-1 w-24 rounded-full mb-8" style="background:linear-gradient(to right,#7C3AED,#F472B6)"></div>

    <div class="space-y-6">
      {#each sections}
      <div>
        <div class="flex items-center gap-2 mb-3">
          <span class="h-6 w-6 rounded-md bg-[#7C3AED] text-white text-xs flex items-center justify-center font-bold">{index}</span>
          <h2 class="text-xl font-semibold text-ink">{stripMd(heading)}</h2>
        </div>
        <div class="space-y-2 pl-8">
          {#each points}
          <div class="flex items-start gap-2.5 group">
            <div class="flex-shrink-0 mt-2 h-2 w-2 rounded-full" style="background:linear-gradient(135deg,#7C3AED,#F472B6)"></div>
            <div class="flex-1 pl-3 -ml-1 md hl">{renderMD(point)}</div>
          </div>
          {/each}
        </div>
      </div>
      {/each}
    </div>

    <div class="mt-8 rounded-2xl border-2 border-[#7C3AED]/30 bg-[#7C3AED]/5 p-5">
      <div class="flex items-center gap-2 mb-2">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
        <span class="text-xs font-bold tracking-widest uppercase text-[#7C3AED]">本节核心回顾</span>
      </div>
      <div class="md text-[15px] leading-relaxed text-ink">{renderMD(summary)}</div>
    </div>

  </div>
</div>
</body>
```

### 关键样式说明
- 页面背景：渐变 `linear-gradient(135deg,#FAF8F5 0%,#F4F0E8 100%)`
- 表头：图标 + 学科标签（小字大写）+ 超大标题 `text-4xl` + 渐变装饰条
- 章节编号：紫色圆角方块 `h-6 w-6 rounded-md`
- 要点前缀：渐变小圆点 `h-2 w-2 rounded-full`
- 要点内容使用 `.md.hl` 变体：**加粗**渲染为渐变背景高亮（粉→紫），字号 15px 行高 1.85
- 总结区：紫色边框 + 浅紫背景 + 对勾图标，标签"本节核心回顾"

---

## 输出图片规格
- 宽度：1080px（render_notes.py 的 `--width` 参数）
- 高度：自适应内容（全页截图 `full_page=True`）
- 格式：PNG
- 文件名：`{title}_{模板名}.png`（标题中的特殊字符替换为下划线）

## 渲染等待
由于使用了 marked.js 和 KaTeX 客户端渲染，`render_notes.py` 默认等待 1500ms 确保公式渲染完成。如公式较多可增加 `--wait 2500`。
