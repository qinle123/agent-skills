# /opsx:propose — 新建变更 + 全量 artifacts

## 用途
一步创建变更并生成所有 artifacts（proposal、design、tasks 等）。

## 输入
参数为变更名（kebab-case）或需求描述。

## 步骤

1. **无输入时询问**：用 clarify 问用户要构建什么

2. **创建工作区**
   ```
   openspec new change "<name>"
   ```

3. **获取 artifact 构建顺序**
   ```
   openspec status --change "<name>" --json
   ```
   解析 JSON 获取 `applyRequires`（需要哪些 artifacts）和 `artifacts`（完整列表）

4. **按依赖顺序循环创建 artifacts**

   对每个 `ready` 状态的 artifact：
   ```
   openspec instructions <artifact-id> --change "<name>" --json
   ```
   instructions JSON 包含：
   - `context`: 项目背景（约束你的行为，不要写入文件）
   - `rules`: artifact 特有规则（约束你的行为，不要写入文件）
   - `template`: 输出文件结构
   - `instruction`: artifact 类型的指导
   - `outputPath`: 写入路径
   - `dependencies`: 已完成的 artifact（需要先读取）

   读取依赖文件 → 用 template 结构创建 artifact → 应用 context/rules 约束

   创建完后重新 `openspec status --change "<name>" --json` 检查状态

5. **显示最终状态**
   ```
   openspec status --change "<name>"
   ```

## 输出示例
```
## 变更提案完成

**名称:** add-user-auth
**位置:** openspec/changes/add-user-auth/

**已创建 artifacts:**
- ✅ proposal.md — 变更动机与范围
- ✅ specs/ — 详细需求规格
- ✅ design.md — 技术方案
- ✅ tasks.md — 实现任务清单

**下一步:** 运行 `openspec:apply add-user-auth` 开始实现
```

## 围栏
- 必须创建 schema 定义的所有 artifacts
- `context` 和 `rules` 是给你的约束，不是文件内容 — 不要拷进 artifact
- 依赖文件要先读取再创建新 artifact

## Pitfalls

- **spec-driven schema 要求至少一个 delta** — 即使你的变更只是行为修复，不引入新能力，也必须在 proposal 的 Capabilities 中列出至少一个 capability，并在 specs/ 下对应创建 spec 文件。如果 proposal 写"无新 capability"，`openspec validate` 会报 `"Change must have at least one delta"` 错误（仅在 apply 前触发，但 propose 阶段就应该处理好）。补救方法：识别出一个合理的 capability 名称（如 `update-command`），把它加到 proposal 的 New Capabilities，并创建对应的 `specs/<name>/spec.md`，包含至少一个 #### Scenario 块。
