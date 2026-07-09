# /opsx:verify — 验证实现

## 用途
验证代码实现是否匹配变更中的 artifacts（specs、tasks、design）。

## 输入
可选：指定变更名。

## 步骤

1. **选择变更**
   ```
   openspec list --json
   ```

2. **检查 schema**
   ```
   openspec status --change "<name>" --json
   ```

3. **加载 artifacts**
   ```
   openspec instructions apply --change "<name>" --json
   ```
   读取 `contextFiles` 中的所有 artifact

4. **三维验证**

   **完整性**：检查 tasks.md checkbox 完成情况 + spec 覆盖范围
   **正确性**：需求实现映射 + 场景覆盖
   **一致性**：设计决策遵从度 + 代码风格模式

5. **输出验证报告**

```
## Verification Report: add-user-auth

| 维度       | 状态               |
|-----------|--------------------|
| 完整性     | 5/6 tasks, 3 reqs |
| 正确性     | 2/3 reqs covered  |
| 一致性     | Followed          |

**CRITICAL (必须修复):**
- 未完成任务: "Add input validation"

**WARNING (建议修复):**
- 场景未覆盖: "Empty password rejected"

**SUGGESTION (锦上添花):**
- 代码风格: consider using early return pattern
```
