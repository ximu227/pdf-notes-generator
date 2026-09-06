# 设计系统

## 气质
「夜晚书桌上的暖光」—— 温暖、专业、可信赖、效率、清晰、克制。
现代化 + 教育温度，避免冰冷科技感；以信息密度和清晰排版取胜。

## 技术栈
- **Tailwind CSS**（CDN）：原子化样式，所有模板共用
- **marked.js**：Markdown 渲染（points / summary 内容）
- **KaTeX**：LaTeX 公式渲染

## Tailwind 配置（所有模板共用）

```javascript
tailwind.config = {
  theme: { extend: { colors: {
    primary: { DEFAULT:'#7C3AED', dark:'#6D28D9' },
    accent: { DEFAULT:'#F472B6' },
    ink:'#1C1B1F', muted:'#78716C', cardborder:'#E7E2D6'
  }}}
}
```

## 配色方案

| Token | 值 | 用途 |
|---|---|---|
| `--background` | `#FAF8F5` 暖米白 | 全局底色 |
| `--foreground` | `#1C1B1F` 墨黑 | 正文 |
| `--primary` | `#7C3AED` 薄暮紫 | 主按钮/重点/标题装饰/编号徽章 |
| `--primary-dark` | `#6D28D9` 深紫 | 表格表头渐变终点 |
| `--accent` | `#F472B6` 暖橙粉 | 强调/标签/要点前缀/总结边框 |
| `--secondary` | `#F4F0E8` 米灰 | 次级背景/卡片/表格奇数行 |
| `--muted` | `#78716C` 中性灰 | 辅助文字/日期填写线 |
| `--border` | `#E7E2D6` 暖灰边 | 卡片描边/横线纸 |
| `--success` | `#10B981` 薄荷绿 | 成功/正确 |
| `--warning` | `#F59E0B` 琥珀 | 警告/易错 |

品牌渐变：`linear-gradient(135deg, #7C3AED 0%, #F472B6 100%)`
- 用于：图标方块、编号徽章、装饰条、要点圆点、完成卡片

## 字体排版

```css
font-family: 'Times New Roman', 'Microsoft YaHei', serif;
```

**字体规则（强制）**：
- **汉字**：使用 `Microsoft YaHei`（微软雅黑）
- **英文和数字**：使用 `Times New Roman`
- **数学公式**：使用 KaTeX 默认字体（不受 body font-family 影响）
- **实现原理**：CSS 按 `font-family` 顺序匹配字符，英文字符和数字命中 Times New Roman，中文字符在 Times New Roman 中无对应字形，回退到 Microsoft YaHei

- 标题：600 粗体，行高 1.2
- 副标题：500 medium，letter-spacing 0.15em，全大写
- 正文：400 regular，行高 1.7
- 数字：Times New Roman 自带衬线风格，无需额外 tabular-nums
- 课程/日期填写：不要使用 font-mono，数字需用 Times New Roman

## 圆角与间距

- 页面容器：`rounded-2xl`（16px）
- 卡片：`rounded-2xl`（16px）
- 按钮/标签：`rounded-xl`（12px）~ `rounded-full`
- 编号徽章：`rounded-md`（6px）~ `rounded-full`
- 统一中度圆润，避免尖锐直角
- 内容区内边距：40px（康奈尔/表格/流程图），48px（重点高亮）

## Markdown 渲染变体

所有要点和总结内容通过 marked.js 渲染为 HTML，再叠加自定义类：

### `.md`（标准，康奈尔/总结用）
- 字号 14px，行高 1.75
- `strong`：紫色 `#7C3AED`，600 字重
- `em`：粉色 `#F472B6`，斜体
- `ul`：紫色 disc 标记，左缩进 20px
- `blockquote`：粉色左边框，斜体

### `.md.compact`（紧凑，表格/流程图用）
- 字号 12.5px，行高 1.65
- 其余同 `.md`

### `.md.hl`（高亮，重点高亮模板用）
- 字号 15px，行高 1.85
- `strong`：**渐变背景高亮** — `background:linear-gradient(to right,#FCE7F3,#EDE9FE)`，紫色文字，700 字重，padding 1px 6px，圆角 4px，inline-block
- `em`：粉色背景 `#FCE7F3`，粉色文字，600 字重斜体
- 这是重点高亮模板的核心视觉特征

## 流程图步骤色板（7 色循环）

```javascript
const STEP_COLORS = [
  { bg:'#FCE7F3', border:'#F472B6', text:'#9D174D' }, // 粉
  { bg:'#DBEAFE', border:'#3B82F6', text:'#1E40AF' }, // 蓝
  { bg:'#D1FAE5', border:'#10B981', text:'#065F46' }, // 绿
  { bg:'#FEF3C7', border:'#F59E0B', text:'#92400E' }, // 黄
  { bg:'#EDE9FE', border:'#7C3AED', text:'#5B21B6' }, // 紫
  { bg:'#CFFAFE', border:'#06B6D4', text:'#155E75' }, // 青
  { bg:'#FFE4E6', border:'#F43F5E', text:'#9F1239' }, // 红
];
```
第 i 步使用 `STEP_COLORS[i % 7]`，每个颜色包含背景色、边框色、文字色。

## 各模板背景

| 模板 | 页面背景 |
|---|---|
| 康奈尔 | 白色 + 横线纸纹理（repeating-linear-gradient，每 36px 一条 #E7E2D6 线） |
| 对比表格 | `#FAF8F5` 暖米白 |
| 流程图 | `#FAF8F5` 暖米白 |
| 重点高亮 | 渐变 `linear-gradient(135deg,#FAF8F5 0%,#F4F0E8 100%)` |

## 通用组件

### 表头图标方块
```
h-10 w-10 rounded-xl，品牌渐变背景，白色 SVG 图标
```
每个模板使用不同的 SVG 图标：
- 康奈尔：书本图标
- 对比表格：网格/分屏图标
- 流程图：连接/分支图标
- 重点高亮：书本/星星图标

### 渐变装饰条
```
h-1 w-24 rounded-full，品牌渐变背景
```
用于表格、流程图、重点高亮模板的标题下方。

### 总结区
- 康奈尔：粉色边框 `border-[#F472B6]/40` + 浅粉背景 `bg-[#F472B6]/5`，标签"总结 / SUMMARY"
- 对比表格：粉色边框 `border-[#F472B6]/30` + 浅粉背景，标签"一句话总结"
- 重点高亮：紫色边框 `border-[#7C3AED]/30` + 浅紫背景 `bg-[#7C3AED]/5`，标签"本节核心回顾"

## 设计禁忌

- ❌ 蓝紫渐变 + 圆角卡片的 AI 默认审美（用暖米白底 + 薄暮紫点缀）
- ❌ 大量 emoji 作为图标（使用 SVG 线性图标）
- ❌ 多色饱和度过高的卡通插图
- ❌ 浅灰底 + 蓝按钮的常规 SaaS 配色
- ❌ 笔记中出现"AI 生成"字样
- ❌ 重点高亮模板中使用普通紫色加粗（必须用渐变背景高亮 .md.hl）
- ❌ 使用 font-mono / ui-monospace 等覆盖数字字体（数字必须用 Times New Roman）
