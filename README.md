# Agent Skills 🛠️

个人维护的一套 Claude / Antigravity / Codex 自定义 Skill 合集，用于提升 AI 编码与写作的专业度与确定性。

每个 Skill 均以独立目录形式存在，入口统一为该目录下的 `SKILL.md`（Frontmatter 包含 `name` 与 `description`）。

---

## 📚 Skill 清单与使用场景

### 🎨 设计 / 视觉
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [Novel-Control-Station-Skill](skills/Novel-Control-Station-Skill/SKILL.md) | 小说创作控制台。用于长篇小说写作、情节大纲策划、人物/世界设定维护、断点续写及长程 drafting/revision 流程管理。 |
| [frontend-design](skills/frontend-design/SKILL.md) | 高保真前端界面设计。当需要设计 distinctive、生产级的前端组件、静态页面或完整 Web UI 时使用，强调视觉美学，摆脱千篇一律的 AI 套路化设计。 |
| [codebase-design](skills/codebase-design/SKILL.md) | 深度模块与架构设计。在设计/重构模块接口、寻找模块解耦机会、优化代码可测性，以及为复杂业务建立统一共享词汇表时使用。 |
| [generate-design-md](skills/generate-design-md/SKILL.md) | 视觉规范提取。从已有页面或组件中自动提炼出核心设计系统规范，生成最小可用的 `DESIGN.md`，用于约束后续的新页面开发。 |
| [huashu-design](skills/huashu-design/SKILL.md) | 花叔原型与演示顾问。当需要用 HTML/CSS 快速实现动画 demo、高保真交互原型、幻灯片、设计方案对比探索，或需要专业视觉评审意见时触发。 |

### 🧪 测试与质量门禁
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [spec-to-tests](skills/spec-to-tests/SKILL.md) | 需求转测试。将 PRD 需求文档或 QA 用例转化为测试矩阵，规划覆盖率，生成最小有效的单元测试、组件测试或 E2E 自动化测试。 |
| [tdd](skills/tdd/SKILL.md) | 测试驱动开发。在实践 "Red-Green-Refactor" 开发循环或需要以测试先行的思路稳健实现新功能/修复复杂 Bug 时使用。 |
| [review](skills/review/SKILL.md) | 双轴变更审计。针对指定提交、分支或 Tag 之间的代码变更，同时比对"项目编码标准"与"PRD 规格说明"进行深度并行评审。 |

### 🏗️ 架构与系统调试
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | 系统化调试（铁律）。在遇到任何报错、测试失败或非预期行为时，**强制**在提出解决方案前先定位出根因（Root Cause），防止盲目试错。 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 疑难 Bug 诊断循环。专门用于复杂异常排查、长链路调用抛错以及性能衰退的诊断与追溯。 |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | 架构劣化扫描。扫描代码库查找隐式耦合与设计冗余，生成可视化 HTML 报告并引导进行模块的深度优化。 |
| [component-reference-audit](skills/component-reference-audit/SKILL.md) | 孤儿组件/导出审计。自动审计指定目录下组件或导出函数的实际被引用情况，识别不再被使用的僵尸代码。 |

### 🔥 方案质询 (Grill)
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [grilling](skills/grilling/SKILL.md) | 方案压力测试。在正式动手编码之前，对方案进行多维度的高强度连珠炮式提问，暴露潜在设计缺陷。 |
| [grill-me](skills/grill-me/SKILL.md) | 不留情面的访谈。以极客视角审视并打磨你的系统设计，帮助梳理盲区。 |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | 架构方案双推。在以质询的形式打磨设计的同时，自动产出对应的架构决策记录（ADR）与业务术语表。 |

### 🛡️ 工程护栏与会话管理
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [project-guardrails](skills/project-guardrails/SKILL.md) | 本地工程护栏。为项目添加自动化 Lint、构建、提交规范等前置校验契约，定义 `AGENTS.md` 以约束后续 AI 代理的修改行为。 |
| [health](skills/health/SKILL.md) | AI 维护性审计。审计 Claude/Codex/Pi 相关的代理指令、MCP、Hooks 覆盖率以及 AI 协作规范是否存在配置漂移或劣化。 |
| [handoff](skills/handoff/SKILL.md) | 会话交接归档。在当前会话即将超出 Context 限制或需要切换到新会话时，压缩并总结当前上下文，方便另一个 Agent 顺畅接手。 |

### 🛠️ Skill 与多 Agent 工程
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [using-superpowers](skills/using-superpowers/SKILL.md) | 技能引导。在开启新会话时运行，确立技能搜索与自动装载规则，保证技能工具被正确且积极地调配。 |
| [writing-great-skills](skills/writing-great-skills/SKILL.md) | Skill 编写指南。用于创建或改进自定义 Skill，提供使其行为具备确定性和可预测性的最佳实践规范。 |
| [skill-cleaner](skills/skill-cleaner/SKILL.md) | 技能体检。分析并重构过长或冗余的 Skill Description，进行 Token 压缩与预算优化。 |
| [agent-asset-harvest](skills/agent-asset-harvest/SKILL.md) | 代理资产挖掘。从历史会话中提取高频且可复用的 Prompt、自动化脚本和工作流，避免重复造轮子。 |
| [multi-agent-execution](skills/multi-agent-execution/SKILL.md) | 多代理并行编排。当有多个独立工作流可安全并行，或者有高风险验证任务需要委托给 Verifier 子 Agent 独立执行时使用。 |

### ✍️ 文本与学习辅助
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [chapter-selfcheck](skills/chapter-selfcheck/SKILL.md) | 章节多步自查。当说类似“某章节走一遍自查”时触发，针对人物称呼、辈分年龄逻辑、设定冲突和连贯性进行系统审计，报告仅在聊天界面临时输出。 |
| [humanizer-zh](skills/humanizer-zh/SKILL.md) | 中文去 AI 腔。用于修饰、审阅中文文本，检测并重写象征词泛滥、套路排比、浅薄分析等典型 AI 写作特征，使其读起来更加自然、人性化。 |
| [learn](skills/learn/SKILL.md) | 交互式学习教练。结合苏格拉底式启发提问与 Gemini 式学习卡片，根据上传的资料、代码库或文档生成定制大纲和练习阶梯，重在启发理解而非直接给出答案。 |

### ⌨️ 工具与编排
| Skill | 使用场景 / 核心作用 |
| :--- | :--- |
| [herdr](skills/herdr/SKILL.md) | 终端分屏编排。配合 herdr 命令行工具，进行类 tmux 的窗口分屏、多 Agent 命令同步执行与输出内容协同分析。 |
| [brainstorming](skills/brainstorming/SKILL.md) | 创意至设计门禁（**必用前置**）。在开始实现任何新功能、新组件或逻辑修改前，强制开启的交互式设计讨论门禁，需得到用户明确设计批准后方可开始写代码。 |

---

## 🛠️ 维护说明

1. **统一入口**：新增技能时，需在 `skills/` 目录下建立 `<skill-name>/SKILL.md` 并写好 frontmatter (`name` 与 `description`)。
2. **描述一致性**：`SKILL.md` 的 `description` 是该技能自动触发的事实来源，README 表格中的「使用场景」必须与之保持同步，不要随意偏离。
3. **组织结构**：所有技能目录平铺在 `skills/` 下，不嵌套层级。
