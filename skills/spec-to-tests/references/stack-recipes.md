# Stack Recipes

## Detection Order

先检测以下信息：

### Package Manager

- `pnpm-lock.yaml` -> `pnpm`
- `yarn.lock` -> `yarn`
- `package-lock.json` -> `npm`

目标仓库明确禁止某个包管理器时，以仓库规范为准。

### Existing Test Stack

- `playwright.config.*` 或 `@playwright/test`
- `cypress.config.*` 或 `cypress`
- `vitest.config.*` 或 `vitest`
- `jest.config.*` 或 `jest`
- `testing-library`
- `msw`、service mock、fixture helper、page object

### App Stack

- `next.config.*` -> Next.js
- `vite.config.*` -> Vite
- `.umirc.*`, `config/config.*` -> Umi
- `src/pages`, `src/app`, `app/` 等目录结构

## Canonical Matrix Commands

XMind 解析：

```bash
python3 scripts/parse_xmind.py cases.xmind --format markdown
python3 scripts/parse_xmind.py cases.xmind --format json
```

从 XMind 生成新版候选矩阵：

```bash
python3 scripts/build_case_matrix.py cases.xmind --format yaml
python3 scripts/build_case_matrix.py cases.xmind --format markdown
python3 scripts/build_case_matrix.py parsed-xmind.json --format json
```

需求矩阵与 XMind 候选矩阵对齐：

```bash
python3 scripts/reconcile_test_matrix.py requirement-matrix.yaml xmind-matrix.yaml --format markdown
python3 scripts/reconcile_test_matrix.py requirement-matrix.yaml xmind-matrix.yaml --format json
```

最终矩阵确认后生成脚手架：

```bash
python3 scripts/generate_test_scaffold.py final-matrix.yaml --project-root .
python3 scripts/generate_test_scaffold.py final-matrix.yaml --project-root . --write
python3 scripts/generate_test_scaffold.py final-matrix.yaml --project-root . --test-framework jest --ui-framework react --write
```

## Preferred Choices

### If the project already has Playwright

- 直接复用
- 不再引入 Cypress
- e2e 文件应绑定矩阵 `id`
- 失败证据优先使用 trace、screenshot、video

### If the project already has Cypress

- 默认复用 Cypress
- 用户明确要求 Playwright 时再切换

### If the project has unit/component stack but no e2e stack

- 对非关键链路，继续落到 Vitest/Jest/RTL
- 只有真实浏览器链路不可替代时，再新增 Playwright

### If the project has no unit/component stack

- 先根据项目现状补最小能力，不要同时引入 Jest 和 Vitest
- Umi、老 React、重型 Ant Design / ProComponents 项目，默认优先 `Jest + Testing Library`
- Vite、轻量 React 项目，默认优先 `Vitest + Testing Library`
- 只有存在明确兼容性问题时，才从一种栈切到另一种栈

### If the project has no browser automation stack

- 默认优先 Playwright
- 原因：trace、video、screenshot、浏览器管理和 CI 配置较统一

## Minimal Install Commands

根据包管理器选最小命令。执行前必须确认目标仓库允许安装依赖。

### Unit / Component With Jest + Testing Library

```bash
pnpm add -D jest ts-jest jest-environment-jsdom @types/jest @testing-library/react @testing-library/jest-dom @testing-library/user-event identity-obj-proxy jsdom
```

适用信号：

- 项目是 Umi 或非 Vite 主栈
- 组件测试依赖 jsdom、moduleNameMapper、CSS mock
- Vitest 下出现 React hook、实例或测试环境兼容问题

### Unit / Component With Vitest + Testing Library

```bash
pnpm add -D vitest jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

适用信号：

- 项目已存在 Vite / Vitest
- 单测与组件测更偏轻量化
- 没有明显框架兼容问题

### Browser Automation

pnpm:

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium
```

yarn:

```bash
yarn add -D @playwright/test
yarn playwright install chromium
```

npm:

```bash
npm install -D @playwright/test
npx playwright install chromium
```

如果项目已有浏览器二进制或只在本地 Chrome 跑，可按项目现状减少安装步骤。

## Minimal Playwright Setup

至少补齐：

- `playwright.config.*`
- `tests/e2e/`
- baseURL 读取环境变量
- failure 时保留 trace / screenshot / video
- 合理的 `timeout` 与 `expect.timeout`
- 登录态注入或会话复用方案

推荐默认：

- `baseURL` 从 `E2E_BASE_URL` 读取
- 本地与 CI 共用一套配置
- `headless` 由环境变量或 `CI` 控制

## Directory Layout

自动生成的测试默认按功能模块分目录，不要全部平铺。

推荐结构：

```text
tests/
  e2e/
    <feature-module>/
      <feature-module>.spec.ts
      <feature-module>.page.ts
      <feature-module>.fixture.ts
  component/
    <feature-module>/
      <feature-module>.test.tsx
  unit/
    <feature-module>/
      <feature-module>.test.ts
  api/
    <feature-module>/
      <feature-module>.test.ts
```

规则：

- 目录名优先使用业务模块名
- 一个模块内聚合该模块的 spec、page object、fixture、mock
- 只有项目已有更强约定时，才覆盖这个默认结构

## Project Documentation

如果新增了测试基础设施，补项目内文档，至少说明：

- 如何运行
- 真实环境与 mock 如何切换
- 登录态如何注入
- 当前覆盖范围
- 常见问题和排查方式
- 矩阵 `id` 如何追踪到测试文件
