# Session Sources

Load this reference when mining recent agent sessions.

## Known Locations

- Codex sessions: `/Users/liuyadong/.codex/sessions`
- Pi agent sessions: `/Users/liuyadong/.pi/agent/sessions`
- Claude project sessions: `/Users/liuyadong/.claude/projects`
- Claude alternate sessions/cache sources, when needed: `/Users/liuyadong/.claude/sessions`
- Archived Codex sessions: `/Users/liuyadong/.codex/archived_sessions`
- Agent run history, when present: project-local `agent/run-history.jsonl`

## Formats

Pi sessions usually contain JSONL rows like:

- `type: "session"` with `cwd`
- `type: "message"` with `message.role` and text content

Codex sessions usually contain JSONL rows like:

- `type: "session_meta"` with `payload.cwd`
- `type: "response_item"` with `payload.type: "message"` and `payload.role`

Claude project sessions usually live under project-key directories in `/Users/liuyadong/.claude/projects`, with `.jsonl` transcript files and sometimes `sessions-index.json`. Treat each project-key directory as the project/cwd signal, and parse only user/assistant/tool events needed for topic classification.

## Safe Extraction

- Keep only request text summaries, project/cwd, timestamps, and categories.
- Redact `Authorization`, `Bearer`, cookie headers, API keys, JWTs, and copied credentials before any output.
- Drop full AGENTS/system prompts from examples unless the task is specifically about instruction drift.
- Drop aborted-turn markers, `/exit`, and trivial acknowledgements from frequency counts.

## Classification Hints From Recent Sessions

- `Daddylab.Certification` dominates frontend, API, cockpit, workflow graph, and browser-debug work across Codex, Pi, and Claude sessions.
- `.pi` sessions repeatedly cover OpenSpec, subagents, chains, prompts, skills, gitignore hygiene, and sustained goal execution.
- `.claude/projects` should be included when looking for cross-agent repetition, especially where Claude commands, skills, hooks, or agents overlap with Codex/Pi assets.
- `Daddylab.CMC` sessions repeatedly cover item/drawer/service API integration and workflow fixes.
- Repeated risk signals include copied curl commands with sensitive headers, production endpoints, tracked temporary session files, and validation blocked by environment setup.
