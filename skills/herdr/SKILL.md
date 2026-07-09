---
name: herdr
description: >
  在 herdr 终端复用器中控制 pane、读取输出、等待状态变更。
  可以分屏跑命令、读报错、等构建完成、协调多个 agent — 全部通过 herdr CLI 完成。
  仅当在 herdr pane 内运行时启用（HERDR_ENV=1）。
allowed-tools:
  - Read
  - Write
  - Edit
  - RunCommand
  - AskUserQuestion
  - Bash
metadata:
  trigger: 需要在 herdr pane 内跑命令、读报错、等输出时使用
  source: https://raw.githubusercontent.com/ogulcancelik/herdr/master/SKILL.md
---

# herdr — agent skill

使用前先检查 `HERDR_ENV=1`。如果不是，说明没在 herdr pane 内运行，不要尝试控制 herdr。

你在 herdr 里运行。herdr 是一个终端级的 agent 多路复用器，每个 pane 都是一个真正的终端，
你可以用 CLI 控制所有 pane。

这意味着你可以：

- 看其他 pane 和 agent 在干什么
- 创建 tab 做子上下文
- 分屏跑命令
- 启动服务器、看日志、在隔壁 pane 跑测试
- 等特定输出出现后再继续
- 等另一个 agent 做完
- 启动新的 agent 实例

## 核心概念

- **workspace** — 项目上下文。每个 workspace 有 1+ 个 tab
- **tab** — workspace 内的子上下文。每个 tab 有 1+ 个 pane
- **pane** — tab 内的终端分屏。每个 pane 跑一个进程（shell、agent、server 等）
- **agent_status** — `idle` / `working` / `blocked` / `done` / `unknown`

ID 格式：workspace=`1`, tab=`1:1`, pane=`1-1`。
注意：ID 在关闭 tab/pane/workspace 后会压缩，不要当作持久 ID，每次用前重新读取。

## 常用命令

### 查看环境

```bash
herdr pane list           # 看所有 pane
herdr workspace list      # 看所有 workspace
herdr tab list --workspace 1  # 看某个 workspace 的 tab
```

### 读取 pane 输出（看报错！）

```bash
herdr pane read 1-1 --source recent --lines 80        # 最近输出
herdr pane read 1-1 --source visible --lines 50       # 可见屏幕
herdr pane read 1-1 --source recent-unwrapped --lines 80  # 原始日志（忽略折行）
```

### 分屏跑命令

```bash
# 右侧分屏，不抢焦点
NEW_PANE=$(herdr pane split 1-1 --direction right --no-focus \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "npm run build"
```

### 等输出出现（自修复核心）

```bash
# 等构建失败
herdr wait output 1-3 --match "error" --timeout 60000

# 正则匹配
herdr wait output 1-3 --match "FAIL|error|Error" --regex --timeout 60000

# 等 server 启动
herdr wait output 1-3 --match "ready on port" --timeout 30000
```

### 等 agent 状态

```bash
herdr wait agent-status 1-1 --status done --timeout 120000
herdr wait agent-status 1-1 --status blocked --timeout 60000
```

### 给 pane 发输入

```bash
herdr pane send-text 1-1 "hello"          # 发文本，不回车
herdr pane send-keys 1-1 Enter            # 按键
herdr pane run 1-1 "echo hello"           # 发文本+回车
```

### Tab 管理

```bash
herdr tab create --workspace 1 --label "logs"
herdr tab rename 1:2 "logs"
herdr tab focus 1:2
herdr tab close 1:2
```

### Workspace 管理

```bash
herdr workspace create --cwd /path/to/project --label "api"
herdr workspace focus 2
herdr workspace close 2
```

## 自修复工作流（推荐模式）

### 模式 1：跑构建 + 读报错 + 修复

```bash
# 1. 分屏
NEW_PANE=$(herdr pane split 1-1 --direction right --no-focus \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')

# 2. 跑构建
herdr pane run "$NEW_PANE" "npm run build"

# 3. 等结果
herdr wait output "$NEW_PANE" --match "error" --timeout 60000

# 4. 读详细错误
herdr pane read "$NEW_PANE" --source recent --lines 80
# -> 看到错误，修复代码

# 5. 重跑
herdr pane run "$NEW_PANE" "npm run build"
herdr wait output "$NEW_PANE" --match "error" --timeout 60000
# -> 没 error 了，完成
```

### 模式 2：跑测试 + 检查结果

```bash
herdr pane split 1-1 --direction down --no-focus
herdr pane run 1-3 "cargo test"
herdr wait output 1-3 --match "test result" --timeout 60000
herdr pane read 1-3 --source recent --lines 30
```

### 模式 3：起 server + 等就绪

```bash
NEW_PANE=$(herdr pane split 1-1 --direction right --no-focus \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
herdr pane run "$NEW_PANE" "npm run dev"
herdr wait output "$NEW_PANE" --match "ready" --timeout 30000
herdr pane read "$NEW_PANE" --source recent --lines 20
```

### 模式 4：查看另一个 agent 在干嘛

```bash
herdr pane list
herdr pane read 1-1 --source recent --lines 80
```

### 模式 5：等另一个 agent 做完再处理

```bash
herdr wait agent-status 1-1 --status done --timeout 120000
herdr pane read 1-1 --source recent --lines 100
```

## 注意事项

- `pane read` 输出纯文本（不是 JSON）
- `pane read --format ansi` 返回带 ANSI 渲染的快照
- `pane send-text` / `pane send-keys` / `pane run` 成功无输出
- `--no-focus` 让分屏不抢当前焦点
- 用 `pane read` 读已有输出，用 `wait output` 等未来输出
- 如果在 herdr 内运行，`HERDR_ENV` 环境变量为 `1`
