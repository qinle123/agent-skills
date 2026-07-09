---
name: openspec-workflow
description: "OpenSpec change lifecycle commands (propose, apply, verify, archive, explore)"
---

# OpenSpec Workflow — Hermes Skill Package

## 懒加载说明

> **本技能只在以下情况加载：**
> 1. 你主动提及 `spec`、`openspec`、`opsx`、`变更` 等关键词
> 2. 你明确要求使用 openspec 命令干活
>
> 其他情况下我不会自动加载，避免浪费 token。

## 概述

OpenSpec 是一个规格驱动(spec-driven)的开发工作流工具。核心流程：

```
探索 → 创建变更 → 提案 → 规格 → 设计 → 任务 → 实现 → 归档
```

通过 `openspec` CLI 操作。

变更（change）存放在项目根目录的 `openspec/changes/<change-name>/` 下。

## 命令一览

每个命令的详细步骤见对应的参考文件：

| 命令 | 用途 | 参考文件 |
|------|------|---------|
| `openspec:new` <name> | 新建变更，一步步创建 artifacts | references/opsx-new.md |
| `openspec:propose` <name> | 新建变更 + 一次性生成所有 artifacts | references/opsx-propose.md |
| `openspec:ff` <name> | 快进模式：一口气生成全部 artifacts | references/opsx-ff.md |
| `openspec:continue` <name> | 继续处理变更（创建下一个 artifact） | references/opsx-continue.md |
| `openspec:apply` <name> | 实现变更中的任务 | references/opsx-apply.md |
| `openspec:verify` <name> | 验证实现是否匹配 artifacts | references/opsx-verify.md |
| `openspec:explore` <topic> | 探索模式：想清楚再做，不写代码 | references/opsx-explore.md |
| `openspec:archive` <name> | 归档已完成变更 | references/opsx-archive.md |
| `openspec:bulk-archive` | 批量归档多个变更 | references/opsx-bulk-archive.md |
| `openspec:sync` <name> | 同步 delta specs 到主规格文件 | references/opsx-sync.md |
| `openspec:onboard` | 引导式新人上手，走完整流程 | references/opsx-onboard.md |

## 前置条件

- `openspec` CLI 已安装
- 项目根目录下有 `openspec/` 目录（CLI 自动创建）
- `openspec` 命令需要在项目根目录执行

## 通用流程

### 快速开始（推荐）

```
openspec:propose <change-name>
openspec:apply <change-name>
openspec:archive <change-name>
```

### 分步式

```
openspec:new <change-name>
openspec:continue <change-name>   (循环直到 artifacts 完成)
openspec:apply <change-name>
openspec:verify <change-name>
openspec:archive <change-name>
```

### 探索先行

```
openspec:explore <topic>
(想清楚后)
openspec:propose <change-name>
...
```

## 载入子命令

加载具体命令的完整步骤说明：

```markdown
skill_view('openspec-workflow', file_path='references/opsx-apply.md')
skill_view('openspec-workflow', file_path='references/opsx-propose.md')
# ... etc
```
