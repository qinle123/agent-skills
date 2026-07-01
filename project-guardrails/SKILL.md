---
name: project-guardrails
description: Add or upgrade repo-local engineering guardrails for a project. Use when Codex should inspect a repository, choose the smallest local guard/check command, document the AGENTS.md contract, or adapt guardrails for web apps, Node packages, backend services, mixed repos, WeChat Mini Programs, or WeChat AI skills. Excludes CI unless explicitly requested.
---

# Project Guardrails

## Purpose

Build the smallest useful local guardrail loop for the current project, then document the contract in project `AGENTS.md`.

Prefer repo-native scripts, tools, and conventions. Do not turn this into a CI, platform governance, or full test strategy project unless the user explicitly asks.

## Core Workflow

### 1. Inspect Before Designing

Identify the project profile and existing checks first:

- Repo shape: app, package, backend, mini program, monorepo, generated code, specs.
- Tooling: `package.json`, `Makefile`, `justfile`, `pyproject.toml`, `go.mod`, `Cargo.toml`, existing scripts.
- Existing guardrails: lint, typecheck, tests, architecture checks, `guard`, `verify`, repair scripts.
- Agent contract: `AGENTS.md`, project docs, OpenSpec or similar planning boundaries.
- Runtime-specific files: for WeChat Mini Programs, inspect `app.json`, `project.config.json`, subpackages, components, and AI `skills/`.

If this is a WeChat Mini Program or WeChat AI skills project, read `references/wechat-miniprogram.md` before proposing or editing guardrails.

### 2. Choose The Smallest Effective Guardrail

Use one stable local entrypoint when possible, such as:

- `npm run guard`, `yarn guard`, `pnpm guard`
- `make guard`, `make verify`
- `just guard`, `just verify`
- `scripts/guard.*` wired into an existing script system

Start with the highest-value failure class for the repo:

1. Project structure and required config files.
2. Runtime-specific build or schema checks.
3. Lint/type/test checks already present in the repo.
4. Architecture or dependency-boundary checks.
5. Repair-context output for agent follow-up.
6. Changed-files mode only if the repo already has enough baseline coverage.

Do not introduce a heavy framework when a small script or existing command is enough.

### 3. Keep The Implementation Local

Place new files where the repo already keeps tooling, usually `scripts/`, `tools/`, `tests/`, or a project-local guard directory.

Avoid by default:

- CI changes.
- SaaS or remote service dependencies.
- Global installs.
- Production API calls.
- Broad rewrites of unrelated project conventions.

If a guard requires external tools, document the prerequisite and add a graceful skip or clear failure message.

### 4. Update AGENTS.md

After adding or changing guardrails, update project `AGENTS.md` with only the contract future agents need:

- Which command is the default local guard.
- When it must be run.
- Which project profile and runtime constraints matter.
- What counts as automated coverage vs manual acceptance.
- How to handle guard failures with minimal repairs.
- Whether CI is intentionally out of scope.

Preserve existing structure and managed blocks. Do not rewrite unrelated instructions.

### 5. Make Failures Repair-Friendly

Guard output should be useful to the next agent run. Prefer structured messages that include:

- Rule ID or check name.
- Failing file or config path.
- Why it failed.
- Minimal suggested fix.
- Whether the failure is new or pre-existing when that can be determined.

Avoid vague output such as only `invalid config` or `unexpected import`.

### 6. Verify According To The Active Agent Policy

Respect the current project/global verification rules. In Codex sessions where verification should be delegated, ask a `verifier` subagent to run tests, guard commands, or acceptance checks when allowed by the active tool policy.

If verification cannot be delegated or requires sandbox-external tools, state that clearly. Do not pretend unrun checks passed.

For low-risk documentation-only changes, static self-check is acceptable if you disclose that no runtime guard was executed.

## Project Profiles

Use these as selection hints, not rigid templates:

- `web-app`: lint/typecheck/unit tests/build, browser smoke checks when UI changed.
- `node-lib`: package tests, typecheck, exports/package boundary checks.
- `backend`: unit/integration tests, migrations/config checks, API contract checks.
- `wechat-miniprogram`: app config, pages/components/subpackages, DevTools build, package-size and platform constraints.
- `wechat-ai-skills`: mini program AI `skills/`, `app.json.agent.skills`, validate/execute/render snapshots, manual boundaries for auth/payments.
- `mixed`: choose one local entrypoint that orchestrates profile-specific checks without hiding failures.

## Output Expectations

Report:

- Project profile detected.
- Guardrail components added or changed.
- Default command future agents should use.
- `AGENTS.md` contract changes.
- Verification performed, delegated, skipped, or blocked.
- Remaining manual or CI-only risks.
