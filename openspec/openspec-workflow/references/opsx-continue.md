# /opsx:continue — 继续处理变更

## 用途
继续处理已有变更——创建下一个 artifact。

## 输入
可选：指定变更名。省略时从上下文推断或用 clarify 让用户选择。

## 步骤

1. **无名称时选择**
   ```
   openspec list --json
   ```
   展示最近修改的 3-4 个变更让用户选，标注最活跃的为推荐

2. **检查当前状态**
   ```
   openspec status --change "<name>" --json
   ```
   解析 JSON 了解当前状态：`schemaName`、`artifacts[].status`、`isComplete`

3. **根据状态行动**

   **全部完成**：祝贺，建议 `/opsx:apply` 或 `/opsx:archive`

   **有 artifact 可创建**（`status: "ready"`）：
   ```
   openspec instructions <artifact-id> --change "<name>" --json
   ```
   读取依赖文件 → 用 template 创建 artifact → 确认文件已写入

   **全部 blocked**：异常状态，展示并分析原因

4. **创建完成后展示进度**
   ```
   openspec status --change "<name>"
   ```

## Artifact 创建指南

**spec-driven schema 的标准顺序：**

| Artifact | 说明 |
|----------|------|
| proposal.md | 问用户变更详情。填写 Why、What Changes、Capabilities、Impact |
| specs/<capability>/spec.md | 每个 Capability 创建一个 spec 文件。使用 Requirement/Scenario 格式 |
| design.md | 技术决策、架构、实现方案 |
| tasks.md | 拆分为 checkbox 任务 |

## 围栏
- 每次只创建一个 artifact
- 必须按依赖顺序创建，不要跳过
- `context` 和 `rules` 是给你的约束，不写入文件
