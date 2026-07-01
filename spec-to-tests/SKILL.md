---
name: spec-to-tests
description: 将需求文档和可选 XMind/QA 测试用例转化为可追溯测试矩阵，先做需求规则提取、XMind 覆盖校准和测试分层，再生成最小有效的 unit / component / API / e2e 自动化测试。适用于 AI 根据需求生成测试、XMind 晚到后的覆盖对齐、测试矩阵审查、测试脚手架规划。不要为一次性 QA 问题、测试结果分析或调试已有测试触发。
compatibility: 需要 python3, pyyaml 可选
---

# Spec To Tests

## Purpose

这个 skill 的核心是把“需求事实”和“测试覆盖”分离，再通过测试矩阵连接实现与自动化测试。

权威顺序：

1. 需求文档 / OpenSpec / 设计说明：业务规则权威来源
2. 接口文档 / mock / 现有代码：技术契约和边界来源
3. XMind / QA checklist：测试视角的覆盖校准来源

XMind 不是需求权威。只有 XMind 时，只能生成候选测试矩阵，必须把业务断言标记为 `needs-confirmation`，不得声称覆盖完整。

## Read Before Acting

开始前按需阅读：

- `references/stack-recipes.md`
- `references/common-lessons.md`
- `scripts/parse_xmind.py`：输入包含 `.xmind` 时
- `scripts/build_case_matrix.py`：需要从 XMind/JSON 生成候选矩阵时
- `scripts/reconcile_test_matrix.py`：需要把需求矩阵与 XMind 矩阵做覆盖差异时
- `scripts/generate_test_scaffold.py`：用户确认最终矩阵后，需要生成测试目录和文件骨架时

如果目标仓库有 `AGENTS.md`、项目 guard、verifier、OpenSpec 或同类流程规范，必须服从目标仓库规范；本 skill 只定义测试设计方法，不覆盖仓库级验证约束。

## Canonical Matrix Schema

所有矩阵必须使用以下字段。不要使用旧字段别名。

```yaml
- id: "TM-001"
  source: "requirement" # requirement | xmind | requirement+xmind | inferred
  requirementRef: "需求文档 2.1"
  xmindRef: ""
  scenario: "新建认证申请成功"
  precondition: "用户已登录，具备创建权限"
  action: "填写必填信息并提交"
  expected: "状态变为待审核，列表展示新记录，详情出现审批记录"
  priority: "P0" # P0 | P1 | P2 | P3
  recommendedLevel: "e2e" # unit | component | API | e2e | manual
  dataRequirement: "real-env" # none | mock | fixture | real-env | seeded
  assertionAuthority: "confirmed" # confirmed | inferred | needs-confirmation
  reason: "跨页面提交和列表回显，需要真实浏览器链路验证"
  plannedFile: "tests/e2e/certification-create/certification-create.spec.ts"
  automationStatus: "planned" # planned | automated | manual | blocked
  openQuestions: []
```

字段规则：

- `id` 必须稳定，需求阶段生成后后续沿用。
- `source=requirement` 表示来自需求；`source=xmind` 表示只有测试用例来源；两者对齐后改为 `requirement+xmind`。
- `assertionAuthority=confirmed` 只用于需求、接口文档或用户确认过的断言。
- `assertionAuthority=inferred` 表示 AI 从上下文推断，不能当成最终验收标准。
- `assertionAuthority=needs-confirmation` 表示缺少需求权威或存在冲突。
- `recommendedLevel=manual` 用于自动化价值低、依赖人工判断、环境不可控或数据成本过高的用例。
- `plannedFile` 必须按项目现有目录约定生成；没有现有约定时按模块分目录。

## Workflow

### 1. Input Audit

先盘点输入，不要直接写测试。

检查：

- 是否有需求文档、OpenSpec 或验收标准
- 是否有 XMind、QA checklist 或测试用例文档
- 是否有接口文档、mock、测试数据说明
- 是否有设计稿、页面路径、权限/角色说明
- 是否已有 unit/component/API/e2e 测试和 helper

输入模式：

| 模式 | 输入 | 允许动作 |
|---|---|---|
| Spec-first | 只有需求文档 | 生成需求规则清单和初版矩阵，可规划测试 |
| Spec + XMind | 需求文档 + XMind | 做一致性审查，合并最终矩阵 |
| XMind-only | 只有 XMind | 生成候选矩阵，所有业务断言标记 `needs-confirmation` |

### 2. Extract Requirement Rules

有需求文档时，先提取需求规则，再生成矩阵。

至少提取：

- 业务目标
- 主路径
- 状态流转
- 权限差异
- 字段校验
- 数据写入和副作用
- 异常路径
- 可观察断言
- 未说明但影响测试的问题

输出“需求规则清单”后再生成 `source=requirement` 的初版矩阵。

### 3. XMind Intake

如果输入包含 `.xmind`：

- 必须优先执行 `python3 scripts/parse_xmind.py <file> --format markdown` 或 `--format json`
- 需要候选矩阵时，执行 `python3 scripts/build_case_matrix.py <file> --format yaml`
- 不要把原始 XMind 内容大量塞进上下文
- 脚本输出只作为候选矩阵来源，不是最终测试用例

XMind 收敛规则：

- 按“一个业务目标 / 一条业务链路 / 一组同类字段规则”合并叶子节点。
- 字段名、列表列名、详情静态展示项默认并入父级断言。
- 独立风险、独立交互、独立状态流转、独立校验规则才保留为单独用例。
- 只有 XMind 时，`source=xmind` 且 `assertionAuthority=needs-confirmation`。

### 4. Reconcile Requirement And XMind

当同时存在需求矩阵和 XMind 候选矩阵时，必须先做 coverage diff，再生成或修改测试代码。

可以执行：

```bash
python3 scripts/reconcile_test_matrix.py requirement-matrix.yaml xmind-matrix.yaml --format markdown
```

必须输出：

- 需求已被 XMind 覆盖的场景
- XMind 新增但需求未出现的场景
- 需求中有但 XMind 漏测的场景
- 可能重复或可合并的用例
- 可能冲突或需要人工确认的断言
- 建议更新后的最终矩阵

冲突处理：

- 需求和 XMind 冲突时，以需求为准，XMind 行标记 `needs-confirmation`。
- XMind 补充了需求未写明但合理的边界时，保留为 `source=xmind`，并放入 `openQuestions`。
- 用户确认后，才能把 `assertionAuthority` 改为 `confirmed`。

### 5. Choose The Smallest Effective Test Level

默认优先级：

1. unit
2. component
3. API
4. e2e
5. manual

写成 unit：

- 纯函数、映射、枚举、参数构造、权限判断、状态计算

写成 component：

- 表单显隐/禁用/必填
- 弹窗、Drawer、局部提交
- 表格列渲染、筛选控件、局部交互

写成 API：

- 请求 payload、响应 mapping、错误码、权限接口契约
- 不依赖真实浏览器即可验证的服务层行为

写成 e2e：

- 真实页面、真实路由、真实浏览器交互
- 跨组件、跨页面、跨接口联动
- 创建后列表/详情/导出/审批流联动
- 上传、下载、hover、焦点、弹窗、地址跳转

写成 manual：

- 自动化收益低于维护成本
- 依赖第三方人工判断或不稳定外部系统
- 只能在生产/准生产敏感环境验证

复合用例必须拆分：稳定字段逻辑下沉到 unit/component/API，只保留薄的关键链路做 e2e smoke。

### 6. Matrix Checkpoint

这是硬性节奏约束：

1. 先生成已经收敛过的覆盖矩阵
2. 展示 coverage diff 和 open questions
3. 明确提示用户检阅矩阵
4. 等用户确认最终矩阵
5. 再生成测试代码或测试脚手架

未确认最终矩阵前，不得生成测试代码、测试脚手架或批量落盘测试文件。

### 7. Inspect The Project Before Scaffolding

生成测试前先检查：

- 包管理器和 lock 文件
- 现有测试框架
- UI 技术栈
- 现有测试目录、helper、fixture、mock、登录注入方案
- 现有 guard / verifier / CI 入口

规则：

- 已有 Playwright 就沿用 Playwright。
- 已有 Cypress 就沿用 Cypress，除非用户明确要求切换。
- 已有 Vitest/Jest/RTL 时，非浏览器链路优先落在现有栈。
- 不为单次测试生成引入第二套重复框架。
- 如果仓库已有 harness guard，新增测试接入已有入口，不另起平行命令体系。

安装与配置策略见 `references/stack-recipes.md`。

### 8. Generate Tests After Confirmation

用户确认最终矩阵后：

- 先 dry-run 脚手架：

```bash
python3 scripts/generate_test_scaffold.py final-matrix.yaml --project-root .
```

- 用户确认路径合理后，再显式 `--write`。
- 生成的测试必须绑定矩阵 `id`。
- 每个测试文件内按业务意图组织，不按 XMind 叶子节点机械生成。
- 优先复用现有 helper、fixture、page object、mock。
- 没有稳定选择器时，优先在业务代码中补最小 `data-testid`，不要依赖脆弱 DOM 顺序。

### 9. Validate In Narrow Loops

验证必须服从目标仓库规范。

原则：

- 先跑最小相关测试文件或单个 case。
- 中高风险改动按目标仓库要求使用 verifier 或 guard。
- 不绕过 lint/test/guard/harness。
- 失败后先归因，再修复。

失败归因分类：

- 需求或 XMind 冲突
- 测试断言错误
- 选择器/等待问题
- 测试数据问题
- 请求参数或接口契约问题
- 真实业务缺陷
- 环境或权限问题

### 10. Capture Reusable Lessons

完成后只把通用、跨项目可复用的经验沉淀到：

- `references/common-lessons.md`

不要记录项目私有 URL、账号、token、时间戳、临时 ID 或敏感信息。

## Output Expectations

默认产出：

1. 输入盘点和缺口
2. 需求规则清单
3. 初版测试矩阵
4. XMind 候选矩阵（如有）
5. coverage diff（如有需求 + XMind）
6. 用户确认后的最终矩阵
7. 测试脚手架 dry-run 结果
8. 用户确认后的测试代码
9. 验证命令、结果和未覆盖风险
10. 通用经验沉淀说明

## Blacklist

- 不要在最终矩阵确认前生成测试代码或批量落盘。
- 不要把 XMind 当作需求权威。
- 不要在只有 XMind 时把断言标记为 `confirmed`。
- 不要机械把每个 XMind 叶子节点变成独立测试。
- 不要把字段显隐、必填、枚举映射、参数转换默认升格为 e2e。
- 不要因为用户说“都写成 Playwright”就跳过分层纠偏。
- 不要在项目已有测试栈时引入平行框架。
- 不要为了跑通测试顺手修改无关业务逻辑或 guard。

## Quick Heuristics

应该写成 e2e：

- 新增记录后，在列表、详情、审批流中都能看到
- 禁用后按钮状态、列表状态和二次确认完整联动
- 跨页面完成创建、编辑、权限校验和导出

不该默认写成 e2e：

- `is_leaf = true` 时显示某字段且必填
- 评分最大值是 100
- 编辑参数里字段名改为 `category_id`

这些更适合 unit、component 或 API。只有它们必须通过真实浏览器联动才能暴露风险时，才升到 e2e。
