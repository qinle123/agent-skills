# 2026-07-17 Chapter Selfcheck Design

设计并实现一个名为 `chapter-selfcheck` 的 model-invoked 技能。用于帮助用户自查特定章节的文本内容，特别是针对人物关系、辈分称呼、年龄逻辑、设定冲突以及前后连贯性。

## 1. 目标与背景 (Objectives)

本技能的触发词为类似“某章节走一遍自查”的说法。
当触发时，Agent 将使用 `novel-control-station` 审查流程的思想，以及项目自带的设定/风格文档，以分步结构化审计的方式对章节内容进行深度自查。

自查重点包括：
- 人物关系与辈分称呼
- 设定年龄大小与口头称呼的逻辑
- 确认无和项目设定冲突的地方
- 确认无前言不搭后语等逻辑断层

自查结果不需要写回项目文件，只需作为回答临时输出在聊天界面中。

## 2. 修改范围 (Scope of Changes)

1. **新建技能目录与主文件**：
   - 新建 `skills/chapter-selfcheck/SKILL.md`，用于定义该技能的触发条件和执行逻辑。
2. **注册新技能**：
   - 在 `skills.json` 中的 `entries` 列表中追加此技能。
3. **更新 README**：
   - 在 `README.md` 的 `✍️ 文本与学习辅助` 表格中添加此技能的说明。

## 3. 详细设计 (Detailed Design)

### 3.1 `skills/chapter-selfcheck/SKILL.md`
此文件为该技能的执行核心，内容设计如下：

```markdown
---
name: chapter-selfcheck
description: Use when the user asks to perform a self-check on a specific chapter (e.g., "某章节走一遍自查", "第X章自查", "第X章走一遍自查"). Audits character age logic, generational addressings/titles, settings conflicts, and textual cohesion using project files and novel-control-station guidelines.
---

# Chapter Self-Check (章节自查)

用于在编写完章节或修改章节后，针对人物关系、辈分称呼、年龄逻辑、设定冲突、以及文本连贯性进行多步结构化审计。

## 1. 查找并载入文件 (Context Loading)

1. **定位章节文件**：根据用户提供的章节描述（如“第八章”、“第8章”、“第08章”），在工作区（尤其是 `chapters/` 目录）中搜索匹配的文件，例如 `chapters/08-*.md` 或其他类似命名的 markdown 文件。
2. **定位设定与风格文件**：
   - 优先寻找标准 Novel-Control-Station 文件：`03-cast-bible.md`（人物设定）、`04-relationship-map.md`（人物关系）、`09-style-guide.md`（风格指南）、`02-worldbuilding.md`（世界观设定）。
   - 如果不存在上述文件，则在整个工作区内搜索文件名中包含 `style`、`cast`、`relationship`、`character`、`设定`、`风格` 等关键词的 markdown 文件，并将它们作为参考设定读入。
3. 如果找不到章节文件或任何设定文档，向用户明确报告，并列出搜索到的可能文件供用户选择。

## 2. 结构化审计步骤 (Multi-Pass Audit)

### 步骤 1：人物、辈分称呼与年龄逻辑专项审计 (Character, Address & Age Logic Audit)
* **任务**：提取本章中出现或被提及的所有人物。
* **核对**：
  - 从人物设定文档中查询这些人物的年龄、辈分、亲属/师门关系。
  - **称呼核对**：仔细研读角色之间的对话与旁白。核对彼此的称呼是否符合辈分和关系（例如：表哥/堂弟、师叔/师侄、叔侄、祖孙等称呼是否混淆）。
  - **年龄与称呼逻辑核对**：重点检查“设定的年龄大小”与“口头称呼”是否逻辑自洽。例如，不能出现“年龄设定为15岁的小辈直呼50岁的长辈为贤弟”，或者“设定为妹妹的角色在对话里突然叫哥哥为弟弟”等称呼错位。

### 步骤 2：设定与风格冲突审计 (Settings & Style Conflict Audit)
* **任务**：核对章节的剧情走向、人物表现是否违背了设定的基准。
* **核对**：
  - 检查章节中是否出现了与世界观设定或人物核心设定相冲突的情节或背景描述。
  - 对照风格文档，确认是否有禁用的 AI 腔调、废话短语，或与规定写作风格（例如：段落模式 `web-serial-natural`）冲突的地方。

### 步骤 3：语篇连贯性与逻辑审计 (Textual Cohesion & Logic Audit)
* **任务**：通读文本，排查纯粹的文学逻辑与叙事连贯性问题。
* **核对**：
  - 检查有无“前言不搭后语”、逻辑断层、剧情跳跃过大、或者前后事实矛盾等低级逻辑错误。

## 3. 输出自查报告 (Reporting)

自查完成后，将自查报告直接作为回答输出给用户（在聊天界面临时展示），不需要写入到项目文件中。报告应包含：

- **自查章节**：指示被检查的章节文件路径。
- **参考设定文件**：列出读取的设定和风格文件。
- **自查发现列表**：
  - **人物称呼与年龄逻辑问题**：列出具体哪一行（提供原文片段），说明为什么不合逻辑，并给出修改方案。
  - **设定与风格冲突**：列出与设定文档矛盾的地方及修改建议。
  - **语篇连贯性与逻辑问题**：指出前言不搭后语或突兀的剧情逻辑断层。
- **自查结论**：简要说明本章的整体合规度，是否建议直接修改或重写。
```

### 3.2 `skills.json` 追加项
在 `entries` 列表中追加：
```json
    { "path": "skills/chapter-selfcheck" }
```

### 3.3 `README.md` 修改项
在表格的 `✍️ 文本与学习辅助` 部分追加：
```markdown
| [chapter-selfcheck](skills/chapter-selfcheck/SKILL.md) | 章节多步自查。当说类似“某章节走一遍自查”时触发，针对人物称呼、辈分年龄逻辑、设定冲突和连贯性进行系统审计。 |
```

## 4. 扩展性说明 (Extensibility)

本技能的 4 步执行框架易于扩展。未来如果需要增加诸如“错别字与成语误用审计”、“情节张力/冲突程度审计”等，只需在 `SKILL.md` 中以 `步骤 X` 的形式追加规则即可。

## 5. 规范自查 (Spec Self-Review)

- 占位符检查：无 TBD 或 TODO。所有内容明确定义。
- 一致性检查：与用户“仅作为临时输出”的反馈一致，自查报告输出在聊天界面中。
- 范围检查：专注于本技能的添加和注册，不作无关改动。
