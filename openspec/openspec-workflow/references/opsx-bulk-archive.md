# /opsx:bulk-archive — 批量归档

## 用途
一次归档多个变更。智能处理 spec 冲突。

## 步骤

1. **获取活跃变更**
   ```
   openspec list --json
   ```
   无活跃变更则提示并停止

2. **让用户选择**
   用 clarify 让用户多选要归档的变更

3. **批量验证**
   对每个变更收集：
   - artifact 状态（`openspec status --json`）
   - task 完成度（tasks.md checkbox）
   - delta specs（检查 `specs/` 目录）

4. **检测 spec 冲突**
   构建 `capability -> [变更列表]` 映射
   当多个变更同时修改同一个 capability 时为冲突

5. **智能解决冲突**
   对每个冲突：
   - 读取每个变更的 delta spec
   - 搜索代码库，检查哪些需求已实现
   - 仅同步已实现的变更
   - 都实现则按时间顺序应用

6. **展示汇总表并确认**
7. **逐一执行归档**

## 输出示例
```
## Bulk Archive Complete

Archived 3 changes:
- schema-management-cli -> archive/2026-06-09-schema-management-cli/
- project-config -> archive/2026-06-09-project-config/
- add-oauth -> archive/2026-06-09-add-oauth/
```
