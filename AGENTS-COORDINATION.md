# AGENTS-COORDINATION.md — Multi-Agent Build Protocol

## Overview

Three CLI agents are building OpenClaw in parallel. Each works on its own git branch, on isolated parts of the master guide (`building_super_openclaw.md`).

## Agents

| Agent | Branch | Parts | Execution Guide | Focus |
|-------|--------|-------|-----------------|-------|
| Codex | `codex/hardening` | 2, 3, 6, 14, 17, 18 | `codex_openclaw_execution_guide.md` | Security, hardening, cost, incident response |
| Kimi | `kimi/skills` | 5, 8, 9, 10, 11, 12 | `kimi_openclaw_execution_guide.md` | Skills, hooks, memory, autonomy, multi-agent |
| Kiro | `kiro/infra` | 1, 4, 7, 13, 15, 16 | `KIRO.md` (prompting & task guide) | Cloud infra, config, channels, maintenance |

## Rules

1. **Stay on your branch.** Don't modify files assigned to another agent.
2. **Read the master guide** (`building_super_openclaw.md`) for your assigned parts before starting.
3. **Read your execution guide** (see table above) for tool-specific instructions.
4. **Update BUILD-STATUS.md** after completing each part (⬜ → ✅ + notes).
5. **Append to build log** (`workspace/memory/build-log-YYYY-MM-DD.md` — use today's date) with timestamped entries.
6. **Commit often** with format: `[agent] Part N: short description`

## File Ownership

To avoid conflicts, each agent owns specific file areas:

| Agent | Owns | Can Read |
|-------|------|----------|
| Codex | Server configs, systemd units, firewall rules, kill-switch scripts, security audit reports | Everything |
| Kimi | `workspace/` files (SOUL, IDENTITY, etc.), `workspace/skills/`, hooks config in openclaw.json | Everything |
| Kiro | Cloud provisioning scripts, openclaw.json (infra sections), channel configs, Tailscale config, maintenance docs | Everything |

### openclaw.json Path-Level Ownership

`openclaw.json` is shared across agents. To prevent conflicts, each agent owns specific JSON paths:

| JSON Path | Owner | Description |
|-----------|-------|-------------|
| `gateway.*` | Kiro | Port, bind, auth, tailscale, nodes |
| `channels.*` | Kiro | WhatsApp, Telegram, Discord config |
| `agents.defaults.model`, `agents.defaults.models` | Codex | Model selection, fallbacks |
| `agents.defaults.workspace`, `agents.defaults.contextPruning`, `agents.defaults.compaction` | Kimi | Workspace and memory settings |
| `agents.defaults.heartbeat` | Kimi | Heartbeat interval |
| `agents.defaults.subagents` | Kimi | Subagent limits |
| `agents.named.*` | Kimi | Named agent definitions and routing |
| `tools.*` | Kiro | Tool profiles, exec config, web config |
| `hooks.*` | Kimi | Hook entries and configuration |
| `cron.*` | Kimi | Cron webhook token, session retention |
| `skills.*` | Kimi | Skill loading and install config |
| `plugins.*` | Kiro | Plugin entries |
| `messages.*`, `commands.*` | Kiro | Message and command policies |
| `diagnostics.*`, `update.*`, `env.*`, `meta.*` | Kiro | System-level config |

**Rule:** Before modifying `openclaw.json`, always `cp openclaw.json openclaw.json.bak`. If you need to edit a path owned by another agent, note it in the build log with `⚠️ CROSS-AGENT NOTE:` and wait for human approval.

**Shared files** (all agents may update their section only):
- `BUILD-STATUS.md` — update your own rows
- `workspace/memory/build-log-*.md` — append only, never delete others' entries
- `AGENTS.md` — append to Build History section only

## Dependency Graph & Merge Order

Parts must be completed and merged in this order. Every assigned part is accounted for.

```
Phase 1 — Server Foundation (no dependencies):
  Part 1  (Kiro)   Cloud infrastructure provisioned
  Part 2  (Codex)  Server hardened
  Part 3  (Codex)  OpenClaw installed & secured
  Merge: kiro/infra (Part 1) → main, then codex/hardening (Parts 2-3) → main

Phase 2 — Configuration (needs running OpenClaw):
  Part 4  (Kiro)   openclaw.json validated & optimized
  Part 5  (Kimi)   Workspace files populated (IDENTITY, SOUL, MEMORY)
  Merge: kiro/infra (Part 4) → main, then kimi/skills (Part 5) → main

Phase 3 — Intelligence & Channels (needs configured OpenClaw):
  Part 6  (Codex)  Model strategy optimized
  Part 7  (Kiro)   Channels connected (Telegram, Discord)
  Part 8  (Kimi)   Memory system configured
  Merge: all three branches → main (coordinate with human)

Phase 4 — Autonomy & Capabilities (needs working agent with memory):
  Part 9  (Kimi)   Autonomy engine (heartbeat, cron, events)
  Part 10 (Kimi)   Skills installed
  Part 11 (Kimi)   Plugin hooks configured
  Part 12 (Kimi)   Multi-agent architecture
  Merge: kimi/skills → main

Phase 5 — Polish & Hardening (needs everything above):
  Part 13 (Kiro)   Tailscale remote access
  Part 14 (Codex)  Cost control & monitoring
  Part 15 (Kiro)   Maintenance runbook
  Part 16 (Kiro)   Money-making configurations
  Part 17 (Codex)  Kill switch & incident response
  Part 18 (Codex)  Edge cases & gotchas (final audit)
  Merge: remaining branches → main
```

### Dependency Rules

- No part in Phase N may begin until all parts in Phase N-1 are merged to `main`
- Within a phase, parts may execute in parallel if they don't share file ownership
- Part 18 must be last — it's the final audit of everything

## Communication

Agents don't talk to each other directly. Coordination happens through:
1. **BUILD-STATUS.md** — see what others have done
2. **Build log** (`workspace/memory/build-log-YYYY-MM-DD.md`) — see timeline of changes
3. **Git log** — `git log --all --oneline --graph` to see all branch activity
4. **Human** — Donovan resolves conflicts and decides merge timing

## When You're Stuck

1. Check if another agent's work is a prerequisite (see dependency graph above)
2. Check BUILD-STATUS.md for their progress
3. If blocked, note it in the build log and move to your next non-blocked part
4. Ask the human if truly stuck

## Source of Truth

- `building_super_openclaw.md` is the canonical reference for all part definitions
- Execution guides must not contradict the master guide; if they do, master guide wins
- `KIRO.md` serves as Kiro's execution guide (prompting, planning, and task mapping)
