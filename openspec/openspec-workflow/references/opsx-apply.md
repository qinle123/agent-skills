# /opsx:apply — 实现变更任务

## 用途
逐一实现变更中的任务（tasks.md 的 checkbox）。

## 输入
可选：指定变更名。省略时从上下文推断或用 clarify。

## 步骤

1. **选择变更**
   用 `openspec list --json` 列出可选项，让用户选

2. **检查状态**
   ```
   openspec status --change "<name>" --json
   ```
   了解 schemaName 和 artifact 状态

3. **获取 implement 指令**
   ```
   openspec instructions apply --change "<name>" --json
   ```
   返回：
   - `contextFiles`: 需要读取的文件列表
   - 进度（total / complete / remaining）
   - 当前状态指令

   **状态处理：**
   - `state: "blocked"`（缺少 artifact）→ 建议 `openspec:continue`
   - `state: "all_done"` → 祝贺，建议归档
   - 其他 → 继续实现

4. **读取上下文文件**
   读取 `contextFiles` 列出的所有文件。

5. **展示当前进度**
   - Schema 名称
   - 进度: N/M tasks
   - 剩余任务概览

6. **循环实现任务**
   每个任务：
   - 展示正在处理哪个任务
   - 做代码变更（保持最小化）
   - 在 tasks.md 中标记完成：`- [ ]` → `- [x]`
   - 继续下一个

## 输出示例
```
## Implementing: add-user-auth (schema: spec-driven)

Working on task 3/7: Add password hashing utility
✓ Task complete

Working on task 4/7: Create login endpoint
✓ Task complete

## Implementation Complete

**Change:** add-user-auth
**Progress:** 7/7 tasks complete ✓

All tasks complete! Archive with `openspec:archive add-user-auth`
```

## 围栏
- 一直执行直到完成或受阻
- 每次读取 contextFiles 中的文件
- 任务模糊时暂停询问
- 代码变更保持最小范围
- 完成即打勾
- **用户声明已手动测试时** 直接标记验证类任务完成并推进归档，不要重复测试或质疑用户
