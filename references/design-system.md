# 设计系统

## 气质
「夜晚书桌上的暖光」—— 温暖、专业、可信赖、效率、清晰、克制。
现代化 + 教育温度，避免冰冷科技感；以信息密度和清晰排版取胜。

## 配色方案

| Token | 值 | 用途 |
|---|---|---|
| `--background` | `#FAF8F5` 暖米白 | 全局底色 |
| `--foreground` | `#1C1B1F` 墨黑 | 正文 |
| `--primary` | `#7C3AED` 薄暮紫 | 主按钮/重点/标题装饰 |
| `--primary-foreground` | `#FFFFFF` | 主色上的文字 |
| `--accent` | `#F472B6` 暖橙粉 | 强调/标签/数字 |
| `--secondary` | `#F4F0E8` 米灰 | 次级背景/卡片 |
| `--muted` | `#78716C` 中性灰 | 辅助文字 |
| `--border` | `#E7E2D6` 暖灰边 | 卡片描边 |
| `--success` | `#10B981` 薄荷绿 | 成功/正确 |
| `--warning` | `#F59E0B` 琥珀 | 警告/易错 |

品牌渐变：`linear-gradient(135deg, #7C3AED 0%, #F472B6 100%)`

## 字体排版

```css
font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', 'Inter', sans-serif;
```

- 标题：600 粗体，行高 1.2
- 副标题：500 medium，letter-spacing 0.15em，全大写
- 正文：400 regular，行高 1.7
- 数字：tabular-nums，等宽

## 圆角与间距

- 卡片：12px ~ 16px 圆角
- 按钮/标签：8px 圆角
- 统一中度圆润，避免尖锐直角
- 内容区内边距：24px ~ 32px

## 加粗高亮样式

笔记中 `**...**` 渲染为：
- 颜色：`#7C3AED`（薄暮紫）
- 字重：600
- 背景：`rgba(124, 58, 237, 0.08)` 淡紫底
-  padding：1px 4px，border-radius：4px

## 设计禁忌

- ❌ 蓝紫渐变 + 圆角卡片的 AI 默认审美（用暖米白底 + 薄暮紫点缀）
- ❌ 大量 emoji 作为图标
- ❌ 多色饱和度过高的卡通插图
- ❌ 浅灰底 + 蓝按钮的常规 SaaS 配色
- ❌ 笔记中出现"AI 生成"字样
