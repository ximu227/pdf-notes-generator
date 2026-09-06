# 笔记数据结构

## NoteData（AI 生成的笔记 JSON）

```typescript
interface NoteData {
  title: string;       // 笔记标题，如"第10讲 百分数 综合演练"
  subject: string;     // 学科：语文/数学/英语/物理/化学/生物/历史/地理/政治/综合
  summary: string;     // 本讲总结/课堂小结，1-3 句话
  sections: Section[]; // 笔记章节数组
}

interface Section {
  level: number;       // 层级：1=一级标题, 2=二级标题, 3=三级标题
  heading: string;     // 小标题，如"一、两线四角"、"对顶角"
  cues: string[];      // 关键词（康奈尔笔记专用），2-4 个，每个 2-6 字；仅 level 1 使用
  points: string[];    // 要点列表，3-6 条，每条支持 Markdown 和 LaTeX
}
```

## TemplateType（模板类型）

```typescript
type TemplateType = 'cornell' | 'table' | 'flowchart' | 'highlight';
```

| 模板 ID | 中文名 | 适用场景 |
|---|---|---|
| cornell | 康奈尔笔记 | 通用复习笔记，左关键词右内容 |
| table | 对比表格 | 多概念对比、异同分析 |
| flowchart | 流程图 | 步骤流程、因果链、推导过程 |
| highlight | 重点高亮 | 核心概念、易错点、记忆口诀卡片 |

## 模板选择策略

根据笔记内容自动选择最合适的模板：
- **默认**：`highlight`（重点高亮，通用性最强）
- 内容以并列概念对比为主 → `table`
- 内容以步骤/流程/推导为主 → `flowchart`
- 用户未指定且内容通用 → `cornell`
- 用户明确指定模板 → 按用户要求

如果用户要求"全部模板"，则 4 种都生成。

## 文件解析结果

```typescript
interface FileParseResult {
  content: string;     // 提取的文本内容
  fileName: string;    // 文件名
  pageCount: number;   // 页数
  type: 'pdf';
}
```
