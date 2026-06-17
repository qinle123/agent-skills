---
name: zhihu-tui
description: Browse Zhihu (知乎) from the terminal — questions, answers, articles, pins, users, search, hot list, interactions
---

# zhihu-tui Skill

A TUI tool for interacting with Zhihu (知乎). Use it to fetch questions, answers, articles, pins (想法), user profiles, search content, browse hot list, and perform interactions like voting and following.

## Prerequisites

```bash
# Install (requires Python 3.10+)
uv tool install zhihu-tui
# Or: pipx install zhihu-tui
```

## Authentication

Most read commands work without login. Feed, favorites, following, and interactions require login.

```bash
zhihu status  # Check if logged in (exit code 0 = authenticated)
```

Authentication uses a 3-tier strategy:
1. Saved credential from `~/.zhihu-cli/credential.json`
2. Auto-extracts cookies from Chrome/Firefox/Edge/Brave
3. Manual login: `zhihu login --z-c0 <cookie_value>`

If the user mentions Zhihu operations requiring login and `zhihu status` fails, guide them to run `zhihu login --z-c0 <z_c0_cookie>`.

## Command Reference

### Questions

```bash
# Get question details with answers (accepts ID or full URL)
zhihu question 1908480548659225029
zhihu question https://www.zhihu.com/question/1908480548659225029
zhihu question 1908480548659225029 -n 5  # Top 5 answers
```

### Answers

```bash
# Get answer details with comments (accepts ID or full URL)
zhihu answer 1908294773132981653
zhihu answer https://www.zhihu.com/question/1908480548659225029/answer/1908294773132981653
```

### Articles

```bash
# Get article details with comments (accepts ID or full URL)
zhihu article 2010807391655052859
zhihu article https://zhuanlan.zhihu.com/p/2010807391655052859
```

### Pins (想法)

```bash
# Get pin details with comments (accepts ID or full URL)
zhihu pin 1999130577123636672
zhihu pin https://www.zhihu.com/pin/1999130577123636672
```

### Users

```bash
zhihu user zhi-hu-14-94-58                          # User profile
zhihu user-answers zhi-hu-14-94-58 -n 5             # User's answers
zhihu user-articles zhi-hu-14-94-58 -n 5            # User's articles
zhihu user-pins zhi-hu-14-94-58 -n 5                # User's pins
```

### Search

```bash
zhihu search "关键词"                    # General search (default)
zhihu search "关键词" --type people       # Search people
zhihu search "关键词" --type scholar      # Search papers
zhihu search "关键词" --type column       # Search columns
zhihu search "关键词" --type km_general   # Search Zhihu Select (盐选内容)
zhihu search "关键词" --type publication  # Search eBooks
zhihu search "关键词" --type ring         # Search circles
zhihu search "关键词" --type topic        # Search topics
zhihu search "关键词" --type zvideo       # Search videos
zhihu search "关键词" -n 5               # Limit results
```

### Discovery

```bash
zhihu hot          # Hot list (top 30)
zhihu hot -n 10    # Top 10
```

### Collections (require login)

```bash
zhihu favorites                      # My favorite folders
zhihu favorites -n 10                # Limit results
zhihu collections                    # My collections
zhihu collections <url_token>        # Someone else's collections
zhihu following                      # My following list
zhihu feed                           # Personalized feed
zhihu feed -n 5                      # Limit results
```

### Interactions (require login)

```bash
zhihu vote answer 1908294773132981653         # Vote up an answer
zhihu vote answer 1908294773132981653 --down  # Cancel vote on an answer
zhihu vote article 2010807391655052859        # Vote up an article
zhihu vote pin 1999130577123636672            # Vote up a pin
zhihu vote pin 1999130577123636672 --down     # Cancel vote on a pin
zhihu follow question 1908480548659225029     # Follow a question
zhihu follow user <url_token>                 # Follow a user
zhihu unfollow question 1908480548659225029   # Unfollow a question
zhihu unfollow user <url_token>               # Unfollow a user
```

### Account

```bash
zhihu status    # Quick login check
zhihu whoami    # Detailed profile info
zhihu login     # Login (use --z-c0 for cookie)
zhihu logout    # Clear credentials
```

## Structured Output

All commands support `--yaml` and `--json` for machine-readable output. **Prefer `--yaml`** for AI agent usage — it's more token-efficient.

```bash
zhihu question 1908480548659225029 --yaml
zhihu hot -n 5 --yaml
zhihu search "python" -n 5 --yaml
zhihu pin 1999130577123636672 --yaml
```

Non-TTY stdout (piped) defaults to YAML automatically.

Structured output uses a stable envelope: `{ok, schema_version, data/error}`.

## Common Patterns for AI Agents

```bash
# Check login status before actions
zhihu status && zhihu vote answer 1908294773132981653

# Summarize a question — fetch answers first (primary source for summarization)
zhihu question 1908480548659225029 -n 5 --yaml

# Find a user and get their recent answers
zhihu search "张三" --type people -n 1 --yaml
zhihu user-answers <url_token> -n 5 --yaml

# Get hot topics for context
zhihu hot -n 10 --yaml

# Read an article for summarization
zhihu article 2010807391655052859 --yaml

# Read a pin (想法) for context
zhihu pin 1999130577123636672 --yaml

# Always prefer -n to limit results and save context window
zhihu search "python" -n 5 --yaml
```

## Error Handling

- Commands exit with code 0 on success, non-zero on failure
- `zhihu status` exits 0 only when authenticated
- Structured error codes: `not_authenticated`, `invalid_input`, `network_error`, `upstream_error`, `not_found`, `rate_limited`, `api_error`, `internal_error`
- When asked to summarize a question, fetch answers first — they are the primary source. Only fall back to comments when answers are insufficient.