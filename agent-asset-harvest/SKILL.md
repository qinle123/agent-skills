---
name: agent-asset-harvest
description: Mine recent agent sessions and configuration files into reusable agent assets. Use when asked to review sessions, identify repeated workflows or requests, deduplicate prompts/skills/agents/chains, create or update Skills, Sub-Agents, prompts, or automation checklists, audit agent configuration drift, or convert periodic maintenance tasks into durable operating assets.
---

# Agent Asset Harvest

## Overview

Use this skill to convert repeated agent work into durable assets without leaking session secrets. It classifies repeated work into Skill, Sub-Agent, Prompt, Chain, or Automation candidates, then creates the smallest useful asset set.

## Workflow

1. Scope the corpus.
   - Read current repo docs first.
   - Use `references/session-sources.md` for known session locations and formats.
   - Include both active and archived sessions only when the request asks for historical patterns.

2. Extract safely.
   - Collect user requests, cwd/project, timestamps, and high-level topics.
   - Redact tokens, cookies, authorization headers, API keys, JWTs, and full copied logs.
   - Ignore heartbeat messages, aborted-turn markers, and one-word continuations unless they reveal a workflow problem.

3. Classify repeated patterns.
   - Workflow repeated across tasks -> create or update a Skill.
   - Distinct role with clear responsibility -> create or update a Sub-Agent.
   - Repeated user command phrasing -> create or update a Prompt.
   - Ordered multi-agent execution -> create or update a Chain.
   - Time-based or recurrence-based maintenance -> create or update an Automation checklist/spec.

4. Choose conservative asset boundaries.
   - Prefer one focused asset over a broad catch-all.
   - Update existing assets when they already cover the pattern.
   - Create a new Skill only when another agent would benefit from procedural instructions that are not already in global rules.
   - Create a Sub-Agent only when the role has a stable responsibility, output contract, and permission profile.

5. Validate.
   - For Skills, run the skill validator through the verifier.
   - For TOML/JSON/YAML assets, ask the verifier to parse or lint them with the smallest available command.
   - Report source evidence as counts and sanitized examples, not raw session dumps.

## Asset Decision Rules

- Skill: repeated process with steps, failure modes, and references.
- Sub-Agent: recurring specialist role such as session mining, verification, implementation, review, research, or visual QA.
- Automation: recurring maintenance such as weekly session mining, monthly agent config hygiene, or post-frontend-change regression triage.
- Prompt: short repeatable entrypoint that invokes an existing skill/chain without adding new procedure.
- Chain: fixed ordered or parallel multi-agent workflow.

## Output Contract

When reporting a harvest, include:

- Sources scanned: paths, date range, and counts.
- Repeated patterns: category, approximate count, representative sanitized examples.
- Assets created or updated: path and purpose.
- Deferred candidates: why they were not created now.
- Verification: verifier evidence or an explicit gap.

## Do Not

- Do not paste raw session logs into new assets.
- Do not store secrets, cookies, bearer tokens, or private third-party identifiers.
- Do not create an asset for a one-off task.
- Do not delete existing assets during a harvest unless the user explicitly confirms the dangerous operation.
- Do not turn a vague pattern into an automation without an owner, trigger, and output.
