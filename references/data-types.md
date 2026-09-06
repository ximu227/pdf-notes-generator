# 笔记数据结构

## 通用说明

4 种模板分为两类数据结构：
- **康奈尔笔记 / 重点高亮**：使用通用 `NoteData`（sections 嵌套结构）
- **对比表格**：使用 `TableData`（行列表结构）
- **流程图**：使用 `FlowData`（步骤序列结构）

AI 生成笔记 JSON 时，根据所选模板输出对应的数据结构。

---

## NoteData（康奈尔 / 重点高亮 通用）

```typescript
interface NoteData {
  title: string;       // 笔记标题，如"第10讲 百分数 综合演练"
  subject: string;     // 学科：语文/数学/英语/物理/化学/生物/历史/地理/政治/综合
  date?: string;       // 日期（康奈尔模板表头用，如"2026/7/2"），可选
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

### 字段说明
- `cues` 仅康奈尔模板使用，重点高亮模板可忽略
- `date` 仅康奈尔模板表头显示，其他模板不用
- `points` 中支持 `**加粗**`、`*斜体*`、`> 引用`、`$公式$`、`$$块级公式$$`

---

## TableData（对比表格专用）

```typescript
interface TableData {
  title: string;       // 笔记标题，如"光合作用与呼吸作用对比"
  subject: string;     // 学科
  columns: string[];   // 表头列名数组（不含第一列"维度"），如 ["光合作用","呼吸作用"]
  rows: TableRow[];    // 数据行数组
  summary: string;     // 一句话总结
}

interface TableRow {
  dim: string;         // 维度名称，如"场所"、"条件"、"原料"
  cells: string[];     // 各列内容，与 columns 一一对应，支持 Markdown 和 LaTeX
}
```

### 生成规则
- `columns` 通常 2-3 列（对比 2-3 个概念），第一列固定为"维度"
- `rows` 建议 5-8 行，覆盖核心对比维度
- 每个 `cell` 内容简洁，1-2 句话，可含 `**加粗**` 和 `$公式$`
- 对比维度示例：定义、场所、条件、原料、产物、能量转化、公式、实质、应用等

---

## FlowData（流程图专用）

```typescript
interface FlowData {
  title: string;       // 笔记标题，如"解一元一次方程的完整步骤"
  subject: string;     // 学科
  steps: FlowStep[];   // 步骤数组，按顺序排列
  done: string;        // 完成后的总结/易错提醒，支持 Markdown 和 LaTeX
}

interface FlowStep {
  t: string;           // 步骤名称，如"去分母"、"去括号"
  d: string;           // 步骤详细说明，1-3 句话，支持 Markdown 和 LaTeX
}
```

### 生成规则
- `steps` 建议 4-8 步，每步有明确的先后顺序
- `t` 简短（2-6 字），`d` 详细说明操作要点和易错点
- `done` 总结全流程关键注意事项或最易出错的地方
- 步骤颜色由模板自动循环（7 色），无需在数据中指定

---

## TemplateType（模板类型）

```typescript
type TemplateType = 'cornell' | 'table' | 'flowchart' | 'highlight';
```

| 模板 ID | 中文名 | 数据结构 | 适用场景 |
|---|---|---|---|
| cornell | 康奈尔笔记 | NoteData | 通用复习笔记，左关键词右内容，横线纸风格 |
| table | 对比表格 | TableData | 多概念对比、异同分析 |
| flowchart | 流程图 | FlowData | 步骤流程、因果链、推导过程、解题步骤 |
| highlight | 重点高亮 | NoteData | 核心概念、易错点、记忆口诀卡片 |

## 模板选择策略

根据笔记内容自动选择最合适的模板：
- **默认**：`highlight`（重点高亮，通用性最强）
- 内容以并列概念对比为主 → `table`
- 内容以步骤/流程/推导为主 → `flowchart`
- 用户未指定且内容通用 → `cornell`
- 用户明确指定模板 → 按用户要求

如果用户要求"全部模板"，则 4 种都生成（注意：table 和 flowchart 需要将通用 NoteData 转换为对应数据结构）。

---

## 文件解析结果

```typescript
interface FileParseResult {
  content: string;     // 提取的文本内容
  fileName: string;    // 文件名
  pageCount: number;   // 页数
  type: 'pdf';
}
```
