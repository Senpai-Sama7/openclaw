# AGENTS-COORDINATION.md — Multi-Agent Build Protocol

## Overview

Three CLI agents are building OpenClaw in parallel. Each works on its own git branch, on isolated parts of the master guide (`building_super_openclaw.md`).

## Agents

| Agent | Branch | Parts | Focus |
|-------|--------|-------|-------|
| Codex | `codex/hardening` | 2, 3, 6, 14, 17, 18 | Security, hardening, cost, incident response |
| Kimi | `kimi/skills` | 5, 8, 9, 10, 11, 12 | Skills, hooks, memory, autonomy, multi-agent |
| Kiro | `kiro/infra` | 1, 4, 7, 13, 15, 16 | Cloud infra, config, channels, maintenance |

## Rules

1. **Stay on your branch.** Don't modify files assigned to another agent.
2. **Read the master guide** (`building_super_openclaw.md`) for your assigned parts before starting.
3. **Read your execution guide** (`codex_openclaw_execution_guide.md` or `kimi_openclaw_execution_guide.md`) for tool-specific instructions.
4. **Update BUILD-STATUS.md** after completing each part (⬜ → ✅ + notes).
5. **Append to build log** (`workspace/memory/build-log-2026-02-22.md`) with timestamped entries.
6. **Commit often** with format: `[agent] Part N: short description`

## File Ownership

To avoid conflicts, each agent owns specific file areas:

| Agent | Owns | Can Read |
|-------|------|----------|
| Codex | Server configs, systemd units, firewall rules, kill-switch scripts | Everything |
| Kimi | `workspace/` files (SOUL, IDENTITY, etc.), skills/, hooks config in openclaw.json | Everything |
| Kiro | Cloud provisioning scripts, openclaw.json (infra sections), channel configs, Tailscale | Everything |

**Shared files** (all agents may update their section only):
- `BUILD-STATUS.md` — update your own rows
- `workspace/memory/build-log-*.md` — append only

## Merge Order

When parts are complete, merge to `main` in dependency order:

```
Phase 1 (no dependencies):
  kiro/infra   → main   (Parts 1, 4 — infra must exist first)

Phase 2 (needs infra):
  codex/hardening → main (Parts 2, 3 — needs server to harden)

Phase 3 (needs running OpenClaw):
  kimi/skills  → main   (Parts 5, 8-12 — needs installed OpenClaw)

Phase 4 (finishing touches):
  All agents   → main   (Parts 13-18 — polish, monitoring, edge cases)
```

## Communication

Agents don't talk to each other directly. Coordination happens through:
1. **BUILD-STATUS.md** — see what others have done
2. **Build log** — see timeline of changes
3. **Git log** — `git log --all --oneline --graph` to see all branch activity
4. **Human** — Donovan resolves conflicts and decides merge timing

## When You're Stuck

1. Check if another agent's work is a prerequisite (see merge order above)
2. Check BUILD-STATUS.md for their progress
3. If blocked, note it in the build log and move to your next non-blocked part
4. Ask the human if truly stuck
