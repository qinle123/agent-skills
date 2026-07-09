# /opsx:onboard — 引导式上手

## 用途
带新手走一遍完整的 OpenSpec 工作流。边教边干。

## 前置检查
```
openspec --version
```
如果未安装 → 提示安装后重来

## 阶段

### 1. 欢迎
介绍 OpenSpec 完整流程（探索 → 提案 → 规格 → 设计 → 任务 → 实现 → 归档），约 15-20 分钟

### 2. 任务选择
扫描代码库找小改进点：TODO/FIXME、缺 error handling、无测试函数、`any` 类型、debug artifact、缺校验
展示 3-4 个候选让用户选

### 3. 探索演示
对选定任务做 1-2 分钟探索，画 ASCII 图
介绍 `/opsx:explore` 命令

### 4. 创建变更
`openspec new change "<name>"` 并解释目录结构

### 5. Proposal
起草 proposal.md（Why、What Changes、Capabilities、Impact）
用户确认后保存

### 6. Specs
创建 delta spec，使用 Requirement/Scenario 格式（WHEN/THEN/AND）

### 7. Design
创建 design.md（Context、Goals/Non-Goals、Decisions）

### 8. Tasks
将工作拆分为 checkbox 任务

### 9. Apply
逐一实现任务，一边做一边讲解 spec/design 如何指导代码

### 10. Archive
归档变更，保存决策历史

### 11. 总结
回顾完整流程，提供命令参考表
