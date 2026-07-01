---
name: multi-agent-execution
description: Structure multi-agent or sub-agent work when the user explicitly asks for it, when independent workstreams can run safely in parallel, or when verification/test/guard execution needs a delegated evidence matrix. Do not load for small serial tasks where decomposition would add overhead.
---

# Multi-Agent Execution

## Overview

把多代理协作当作一种执行手段，不当作默认流程。
目标是缩短总耗时，不是制造额外编排成本。

## When To Use

仅在满足以下条件时启用：

- 任务可以拆成多个边界清晰的子任务
- 子任务之间没有写冲突，或能明确划分写入范围
- 并行执行能明显缩短整体耗时
- 主代理仍能在本地推进关键路径

以下情况不要强行并行：

- 下一步动作被某个结果直接阻塞
- 多个子任务必须连续修改同一文件或同一逻辑面
- 任务本身很小，拆解成本高于收益
- 子代理很难在有限上下文里独立完成

## Workflow

1. 先识别依赖关系，区分并行节点与串行节点。
2. 主代理保留关键路径任务，本地先推进。
3. 将可并行的侧任务批量下发，不逐个串行派发。
4. 子代理返回后，由主代理统一校验、合并、验证、汇报。

## Task Template

每个子任务至少写清这 6 项：

- 目标：本轮只解决什么
- 边界：明确不处理什么
- 输入：允许读取的上下文、文件、文档
- 输出：补丁、结论、证据或测试结果
- 写入范围：允许修改哪些文件
- 验证：本轮最小检查是什么

## Hard Rules

- 同一轮内，默认一个文件只允许一个执行单元落盘
- 无前置依赖且无写冲突的任务才并行
- 分析、决策、最终汇总由主代理收口
- 子代理结论必须附证据，不能只给判断
- 子代理失败时，必须返回阻塞点、已尝试动作、下一步建议
- 合并后仍需执行与改动最相关的验证，不能因为并行而跳过

## Output Pattern

对外汇报时优先给这 4 类信息：

- 本轮完成了什么
- 哪些结果已被主代理确认
- 还有什么阻塞或风险
- 下一轮如何继续拆解
