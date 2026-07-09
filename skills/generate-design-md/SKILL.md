---
name: generate-design-md
description: 从现有前端系统、页面和组件中提炼并生成最小可用的 DESIGN.md，供后续 AI 开发新页面/组件时作为稳定视觉边界。适用于用户要求“生成 DESIGN.md”“提炼现有设计系统”“让 AI 参考现有 UI 风格继续开发”等场景。
---

# Generate DESIGN.md

## Overview

这个 skill 的目标不是凭空设计一套新视觉，而是把项目里已经存在、且足够稳定的视觉规则显式化，沉淀成一个可被 coding agent 持续消费的 `DESIGN.md`。

优先目标：

1. 从现有系统提取事实，而不是臆造 token
2. 先产出最小可用版本，再迭代精化
3. 同时写出机器可读 token 和人类可读 rationale
4. 让后续 AI 在“延续现有系统”时少跑偏

如果项目 UI 还没有收敛、页面风格明显混乱，先明确指出这一点，不要把混乱直接固化成 `DESIGN.md`。这种情况下，应该先收敛设计方向，再生成规范。

## When To Use

在这些场景使用：

- 用户要求基于现有项目生成 `DESIGN.md`
- 用户希望后续 AI 开发新页面/新组件时参考现有视觉系统
- 项目已有一套稳定 UI，但规则分散在代码、样式和组件中
- 用户想把现有 design tokens / 组件风格沉淀到仓库里

不要在这些场景直接触发：

- 只是一次性做一个新页面，没有长期复用需求
- 项目几乎没有现成 UI 可参考
- 用户真正要的是“重新设计一套新风格”而不是提炼现状

## Workflow

### 1. Inspect Before Writing

先检查仓库里是否已经存在设计规范或 token 来源。优先查找：

- `DESIGN.md`
- `tailwind.config.*`
- `theme.*`
- `tokens.*`
- `src/styles/*`
- `src/theme/*`
- 组件库目录（如 `components/`, `ui/`, `design-system/`）
- 设计说明文档、Storybook、Figma 导出说明、品牌文档

至少确认这些信息：

- 技术栈（React / Vue / Next / 原生 HTML/CSS 等）
- 样式来源（Tailwind / CSS Modules / SCSS / styled-components / token 文件）
- 哪些页面和组件最能代表现有系统
- 是否已有稳定的按钮、输入框、卡片、标签、导航等基础组件

如果项目中已经存在 `DESIGN.md`，默认先读它，再判断是补充、修订还是重建；不要直接覆盖。

### 2. Choose Representative Sources

不要扫描完所有页面就机械汇总。先挑 3 到 5 个“代表性样本”，优先级：

1. 设计最成熟、复用最多的页面
2. 基础组件最齐全的模块
3. 用户明确指出“这套风格是对的”的页面

优先挑这些元素作为样本来源：

- 主要布局页面
- `Button` / `Input` / `Card` / `Modal` / `Badge` / `Tabs`
- 导航、表单、列表、详情页中最稳定的实现

如果样本之间明显冲突：

- 明确记录冲突点
- 推断哪个是主流实现
- 必要时暂停并让用户确认哪套为准

不要偷偷平均化两套风格。

### 3. Extract Facts First

先提取“事实层”，再写“解释层”。

事实层至少包括：

- `colors`
- `typography`
- `rounded`
- `spacing`
- `components`

提取原则：

- 只收录高频、稳定、可命名的 token
- 同类值如果只有细微差异，优先收敛到最小必要集合
- 不要把每个页面上的一次性特殊值都写进 token
- 对于组件 token，优先写用户真正会复用的基础组件，而不是业务私有组件

推荐的最小字段：

```yaml
name: <design-system-name>
colors:
  primary: <color>
  secondary: <color>
  accent: <color>
  surface: <color>
  text: <color>
  muted: <color>
typography:
  h1: ...
  h2: ...
  body-md: ...
  label-sm: ...
rounded:
  sm: ...
  md: ...
  lg: ...
spacing:
  xs: ...
  sm: ...
  md: ...
  lg: ...
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
```

如果项目现有系统明显没有某类 token，不要硬补完整；缺什么就留空或省略，并在正文说明。

### 4. Infer Rationale Carefully

在 token 之后，再补 markdown 正文，解释“为什么”。

正文优先写这些 section：

1. `## Overview`
2. `## Colors`
3. `## Typography`
4. `## Layout`
5. `## Components`
6. `## Do's and Don'ts`

写法要求：

- 从现有系统推断，不要虚构品牌故事
- 用项目真实气质描述，例如“偏桌面工具感”“偏运营后台”“偏编辑器风格”“偏克制的企业产品”
- 明确强调色、边框、阴影、留白、层级的使用规则
- 写清楚哪些做法应避免，帮助后续 agent 不跑偏

`Do's and Don'ts` 至少回答：

- 哪些样式可以重复使用
- 哪些视觉元素只能少量使用
- 不该出现哪些常见跑偏模式

### 5. Produce A Minimal Draft First

默认先产出“最小可用版”而不是“大而全版”。

最小可用版标准：

- 能描述现有系统主色、文字层级、圆角、间距
- 能覆盖 2 到 4 个关键基础组件
- 能让 agent 继续生成新页面时大体不跑偏

如果用户没有要求，不要一开始就把全部组件、所有状态、所有页面变体都写进去。

### 6. Validate Against The Codebase

生成初稿后，必须回头对照现有代码检查：

- token 名称是否能映射到真实实现
- 颜色和字号是否真的被高频使用
- 组件定义是否符合现有基础组件样式
- 是否把一次性页面特效误写成系统规则
- 是否遗漏了最影响整体风格的公共约束

如果本地可用 `@google/design.md` CLI：

- 用 `npx @google/design.md lint DESIGN.md` 做结构校验

如果本地没有该 CLI：

- 至少人工检查 YAML front matter、token 引用和章节顺序
- 不要为了这件事擅自全局安装核心依赖

### 7. Review With The User When Ambiguous

遇到这些情况必须显式说明，而不是默默拍板：

- 主色体系有两套并行实现
- 旧页面和新页面风格冲突
- 组件库样式与业务页面样式不一致
- 无法判断某些值是系统规则还是历史遗留

这时先给用户一个简短选择题，例如：

- 以 `components/ui` 为准，还是以首页现有实现为准
- 以深色 dashboard 风格为准，还是以浅色营销页风格为准

不要一次抛很多问题；只问当前最影响规范方向的 1 到 2 个问题。

## Output Expectations

默认产出应包含：

1. 代表性样本来源列表
2. 提取出的核心 token 草稿
3. 完整 `DESIGN.md` 文件
4. 如存在冲突，附上关键假设与未决点
5. 如做过校验，附上 lint 或人工校验结果

默认优先参考同目录下的 `DESIGN.template.md` 作为最小输出骨架：

- 优先替换模板中的占位值，而不是从空白开始自由发挥
- 当项目没有某一类 token 时，可以删掉对应字段，不必硬补
- 如果项目已有更明确的 token 命名约定，应优先沿用项目命名

## Suggested Agent Output Shape

向用户汇报时，优先按这个结构：

- 这份 `DESIGN.md` 基于哪些页面/组件提炼
- 我提取了哪些 token，省略了哪些不稳定部分
- 哪些地方是事实提取，哪些地方是基于现状的推断
- 这份文件接下来应该如何在新页面/组件开发里使用

## Blacklist

- 不要在没有看现有代码和样式的情况下，凭空生成一份“看起来完整”的 `DESIGN.md`
- 不要把低频、一次性、活动页特效直接提升为系统 token
- 不要为了追求完整，把每个颜色、字号、圆角值都原样塞进去
- 不要偷偷调美化、重设计、改视觉方向；这个 skill 的任务是提炼现状，不是重做设计
- 不要把现有冲突风格机械平均化
- 不要在用户未确认时直接覆盖已有 `DESIGN.md`

## Quick Heuristics

**适合写进 DESIGN.md 的内容：**

- 高频出现的品牌/语义色
- 标题、正文、标签这类稳定字体层级
- 基础组件的默认态样式
- 常见圆角、间距、表面层级规则

**通常不该直接写进 DESIGN.md 的内容：**

- 某个营销活动页的一次性插画背景
- 只在一个页面临时出现的特殊字号
- 实验中的 hover 特效
- 还在迁移中的旧样式实现

## Example Prompt

当用户说下面这些话时，应该触发本 skill：

- “基于现有系统帮我生成一个 DESIGN.md”
- “扫描这个项目的前端代码，提炼设计规范给 AI 用”
- “我想让后续 AI 写页面时参考现有 UI 风格，先做 DESIGN.md”
- “从当前组件库生成最小可用的 DESIGN.md 草稿”
