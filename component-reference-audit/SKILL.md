---
name: component-reference-audit
description: 审计目录下组件/导出是否存在未被引用项，输出可核对的未引用文件、未引用导出、转导出层和可能误报。适用于用户询问“这个目录下有没有没被引用的组件”“有没有死组件 / 孤儿组件 / 未使用导出”“帮我盘一下组件引用情况”等场景。
---

# Component Reference Audit

用于做“组件引用审计”，不是自动删代码。

目标是给出一份**可验证、低误报**的引用核对结果，让后续清理有证据可依。

## 何时使用

当用户提出这些需求时使用：

- `@某个目录 下是否存在没有被引用的组件`
- `帮我看下有没有死组件`
- `这个模块里哪些导出没人在用`
- `盘一下组件引用情况`
- `找孤儿组件 / 未使用导出 / 没被 import 的文件`

## 结果边界

本 skill 默认回答的是“仓库内是否存在引用证据”，不是“可安全删除”。

必须区分这几类结果：

1. **未被引用文件**：整个组件文件在仓库内没有 import / JSX / 动态引用证据。
2. **未被引用导出**：文件本身可能被使用，但其中某个 named export 没人使用。
3. **纯转导出层**：例如 `components.tsx` / `index.ts` 只做 re-export；要单独判断它是否被引用。
4. **可能误报项**：动态 import、字符串拼接路径、运行时注册、配置驱动引用，不能轻易下结论。

如果证据不足，结论必须写成“未检出引用”，不要写成“可以删除”。

## 审计原则

- 优先用 `rg`，不要用慢速全文搜索方案。
- 先查“文件级引用”，再查“导出级引用”。
- 先给证据，再下结论。
- 默认把 `src/` 和 `tests/` 都视为有效引用来源；如果用户明确说“测试引用不算”，再单独说明。
- 必须过滤名称包含导致的假阳性，例如 `FirstCatPassRateTable` 不能证明 `PassRateTable` 被引用。
- 不要因为工具脚本里出现同名字符串，就认定组件被使用。
- 不自动删除、不顺手重构，除非用户明确要求。

## 建议流程

### 第 1 步：盘点目标目录

1. 列出目标目录下所有 `.ts` / `.tsx` 文件。
2. 标记以下候选：
   - `export default Xxx`
   - `export const Xxx`
   - `export { A, B } from ...`
   - 明显的组件文件、`index.ts(x)`、`components.tsx`
3. 先读入口文件和聚合文件，理解目录内部引用关系。

优先命令：

```bash
find <target-dir> -type f | sort
rg -n "export default|export const|export \{|export type|import " <target-dir>
```

### 第 2 步：做文件级引用检查

对每个候选文件，查这些证据：

- 是否被其他文件 `import`
- 是否被同目录或上层目录聚合 re-export
- 是否出现在动态 `import('...')`
- 是否只在自己文件里出现

常见检查方式：

```bash
rg -n "@/business-components/.../Foo|\./Foo|\.\./Foo|import\(.*Foo" src tests
```

如果是 `index.tsx` / `components.tsx` 这类聚合文件，要按“模块路径”查，不要只按文件名关键字查。

### 第 3 步：做导出级引用检查

对 default export / named export 分开检查。

#### `default export`

需要找：

- `import X from '...'`
- JSX `<X />`
- 极少数 `React.createElement(X)`

注意：

- 不能只搜组件名字符串；要避免被更长名字误命中。
- 搜到同名但不同来源的本地组件时，不算有效引用。

#### `named export`

需要找：

- `import { X } from '...'`
- 聚合 re-export 再被别处 import
- 同目录内部直接引用（如果确实跨文件）

如果某个 util 在定义文件内部被别的导出调用，不算“外部未引用”；但如果任务目标是“目录下未被引用的组件”，应把纯 util 和组件分开汇报，避免混在一起。

### 第 4 步：专门处理转导出层

像下面这类文件单独判断：

```ts
export { A, B, C } from '../shared'
```

规则：

- 如果这个聚合文件没人 import，它本身就是“未被引用的转导出层”。
- 但它 re-export 的底层组件，仍要继续检查真实引用，不要跟着一起判死。

### 第 5 步：检查误报来源

在下结论前，额外排查这些情况：

- `React.lazy(() => import('./X'))`
- 路由配置、菜单配置、注册表、映射表里的字符串路径
- 低代码/配置驱动组件注册
- 测试引用是否是唯一引用
- 文档、OpenSpec、Markdown 中的提及不算运行时引用，只能算旁证

如果发现只被文档提及，要明确写“仅文档/说明提及，无代码引用证据”。

## 推荐输出格式

按下面结构输出，优先给结论，再给证据：

```markdown
## 审计范围
- 目录：`...`
- 有效引用范围：`src/`、`tests/`
- 是否将测试视为引用：是 / 否

## 未被引用文件
- `path/to/File.tsx` — 未检出 import / JSX / 动态引用证据

## 未被引用导出
- `path/to/file.tsx:12` `SomeExport` — 文件被引用，但该导出未检出使用证据

## 未被引用的转导出层
- `path/to/components.tsx` — 仅做 re-export，未检出任何 import 入口

## 仍被引用的关键组件
- `path/to/A.tsx` — 证据：`src/pages/X/index.tsx:10`

## 可能误报 / 需人工复核
- `path/to/B.tsx` — 存在动态 import / 注册式引用线索
```

如果用户的问题是“有没有没被引用的组件”，最终回答要把“组件”和“工具函数”分开，不要混成一锅。

## 结论措辞

优先使用这些措辞：

- `未检出引用证据`
- `目前仅发现测试引用`
- `当前只是一层转导出，且未被任何文件 import`
- `存在同名误命中，已排除`
- `暂不能据此判断可安全删除`

避免直接写：

- `这个文件没用了，删掉吧`
- `肯定是死代码`
- `全都可以安全删除`

## 最小核验清单

交付前至少自检：

- [ ] 目标目录文件清单已枚举
- [ ] 入口/聚合文件已检查
- [ ] 文件级引用与导出级引用已分开判断
- [ ] 同名误命中已排除
- [ ] `src/` 与 `tests/` 的引用范围已说明
- [ ] 转导出层已单独判断
- [ ] 结论里没有把“未检出引用”偷换成“可安全删除”

## 一个高质量示例

如果审计 `src/business-components/cockpit/`，像这种结论是合格的：

- `src/business-components/cockpit/Director/DirectorWaitInfo.tsx`：未检出任何 import / JSX 引用
- `src/business-components/cockpit/Director/DWorkloadsTable.tsx`：未检出任何 import / JSX 引用
- `src/business-components/cockpit/DirectorPage/components.tsx`：仅做 re-export，且未被任何文件 import
- `src/business-components/cockpit/ChargePersonPage.tsx`：仍被 `src/pages/Home.jsx` 和 `src/pages/ChargePersonCockpitPage/index.tsx` 引用

这种输出既能回答问题，也不会越界做删除决策。
