# WeChat Mini Program Guardrails

Use this reference when the repo is a WeChat Mini Program, a Mini Program subpackage, or contains WeChat AI skills.

## Detection

Treat the project as WeChat-related when these appear:

- `app.json`
- `project.config.json`
- `sitemap.json`
- `miniprogramRoot`
- `pages/`, `components/`, `custom-tab-bar/`, `workers/`, `cloudfunctions/`
- `app.json.agent.skills`
- `skills/*/SKILL.md`
- `skills/*/components/*`

## Guardrail Layers

Prefer a layered local guard instead of only generic lint:

1. Static config checks
   - `app.json` is valid JSON and required entries exist.
   - `pages` paths resolve to page files.
   - `subPackages` / `subpackages` roots and pages resolve.
   - `usingComponents` paths resolve from page/component JSON files.
   - `project.config.json` preserves required `packOptions.include` / `ignore` rules.

2. Mini Program build checks
   - Use the repo's existing WeChat DevTools CLI command if present.
   - Treat DevTools build/upload/preview as environment-sensitive. It may require GUI login, local ports, or sandbox-external approval.
   - If the CLI cannot run in the current environment, record the exact blocked command and required manual check.

3. AI skills checks
   - Confirm `app.json.agent.skills[]` matches `skills/<name>/SKILL.md` directories.
   - Confirm AI skill component paths, props, and JSON declarations resolve.
   - Prefer the repo's validate/execute/render scripts when present.
   - Snapshot/render checks should inspect output artifacts and logs, not only exit codes.

4. Runtime behavior boundaries
   - Auth, payment, privacy authorization, native capability prompts, and real device behavior often require manual DevTools or device acceptance.
   - Do not mark these as fully automated unless the repo already has a proven harness for them.

## Common Commands To Look For

Search before inventing:

- `npm run guard`, `npm run verify`, `npm run lint`, `npm run test`
- `npm run miniprogram:*`, `npm run wechat:*`, `npm run wx:*`
- `node .codex/skills/*/scripts/validate.mjs`
- `node .codex/skills/*/scripts/execute.mjs`
- `node .codex/skills/*/scripts/render.mjs`
- WeChat DevTools CLI wrappers in `scripts/`, `tools/`, or package scripts.

## AGENTS.md Contract Additions

For Mini Program projects, document:

- The default local guard command.
- Whether WeChat DevTools CLI is required and how to handle sandbox restrictions.
- Which checks are static, build-time, render/snapshot, or manual.
- Which files are sensitive project boundaries, especially `app.json`, `project.config.json`, subpackage roots, and AI `skills/`.
- That production API calls, login flows, payment flows, and real user data require explicit user approval or a documented test environment.

## Repair-Friendly Output

For each failure, include:

- Check name, such as `wxa-config-pages`, `wxa-agent-skills`, or `wxa-render-snapshot`.
- Source file.
- Referenced target path if relevant.
- Minimal fix.
- Whether manual DevTools or device verification is still required.
