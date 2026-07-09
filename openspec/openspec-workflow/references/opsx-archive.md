# /opsx:archive — 归档变更

## 用途
将已完成变更归档。

## 输入
可选：指定变更名。

## 步骤

1. **选择变更**
   ```
   openspec list --json
   ```
   只展示活跃变更（未归档的）

2. **检查 artifact 完成度**
   ```
   openspec status --change "<name>" --json
   ```
   如有未完成的 artifact，警告并确认是否继续

3. **检查 task 完成度**
   读取 `tasks.md`，统计 `- [ ]` vs `- [x]`
   如有未完成 task，警告并确认

4. **检查 delta specs 同步状态**
   检查 `openspec/changes/<name>/specs/` 目录
   如果有 delta specs，对比主规格文件，展示变更摘要
   询问是否同步：推荐同步后再归档

5. **执行归档**
   ```
   mkdir -p openspec/changes/archive
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

## 输出示例
```
## Archive Complete

**Change:** add-user-auth
**Schema:** spec-driven
**Archived to:** openspec/changes/archive/2026-06-09-add-user-auth/
**Specs:** ✓ Synced to main specs

All artifacts complete. All tasks complete.
```

## Pitfalls

### User-verified testing tasks
When the user says "我已手动测试" (I've manually tested), you can mark all verification/QA tasks (`- [ ] 4.1 手动走通...`) as complete directly — the user has confirmed the feature works. Do NOT require the user to re-demonstrate. Just update `tasks.md` with `- [ ]` → `- [x]`.

### Bulk archival
When the user asks to archive "所有" (all) completed changes:

1. Check `openspec list --json` — only in-progress changes appear (archived ones are gone)
2. For each change with `completedTasks == totalTasks`:
   - Mark any remaining verification tasks as done (user confirmed testing)
   - `mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>`
3. Changes still in-progress (incomplete tasks) stay active — ask the user what to do
4. Confirm with a second `openspec list --json` — should return empty or only remaining WIP changes
