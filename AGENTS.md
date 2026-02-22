# AGENTS.md — OpenClaw Multi-Agent Build: Complete Onboarding & Operations Guide

> **If you are an AI coding agent reading this for the first time: this file is your single source of truth.** Read it fully before doing anything. It tells you what we're building, where we are, how to figure out what to do next, and how to verify your work.

---

## What We're Building

OpenClaw is a **persistent, autonomous AI agent runtime** — not a chatbot. It runs 24/7 on a cloud VPS, accepts messages from WhatsApp/Telegram/Discord, executes tasks, manages its own memory, runs scheduled jobs, and gets smarter over time. Think of it as a full-time AI employee that never sleeps.

The architecture is 4 layers:

```
YOU (any device) → Channel Adapters (WhatsApp/Telegram/Discord)
                 → Gateway (Node.js, always-on VPS, port 18789)
                 → AI Brains & Tools (Claude/GPT/Ollama + shell/web/files)
```

The runtime is already partially running locally (`~/.openclaw/`). We are building it out to full production capability across 18 parts defined in the master guide.

## The Master Guide

`building_super_openclaw.md` (89KB) is the definitive reference. It contains 18 parts:

| Part | Title | Focus Area |
|------|-------|------------|
| 0 | Philosophy & Architecture Mental Model | Read-only reference (already done) |
| 1 | Cloud Infrastructure | OCI/Hetzner VPS provisioning |
| 2 | Server Hardening | SSH, firewall, fail2ban, unattended-upgrades |
| 3 | OpenClaw Installation & Security | npm install, systemd, token rotation |
| 4 | The Complete Configuration | openclaw.json validation & optimization |
| 5 | Workspace Files — Your Agent's Mind | SOUL.md, IDENTITY.md, memory system |
| 6 | Model Strategy & Intelligence Maximization | Model selection, fallbacks, cost/quality |
| 7 | Channel Setup | Telegram, Discord, WhatsApp configuration |
| 8 | Memory System & Retrieval | SQLite memory, workspace memory, retrieval |
| 9 | The Autonomy Engine | Heartbeat, cron, events, proactive behavior |
| 10 | Skills — Teaching Specialist Capabilities | Skill installation and configuration |
| 11 | Plugin Hooks — Instrumentation & Power | Hook system, event pipeline |
| 12 | Multi-Agent Architecture | Named agents, routing, subagents, trust boundaries |
| 13 | Remote Access with Tailscale | Secure remote access to gateway |
| 14 | Cost Control & Monitoring | Budget tracking, token usage, alerts |
| 15 | Maintenance Runbook | Updates, backups, recovery procedures |
| 16 | Money-Making Configurations | Revenue-generating agent setups |
| 17 | The Kill Switch & Incident Response | Emergency shutdown, compromise response |
| 18 | Things Nobody Talks About | Edge cases, gotchas, undocumented behavior |

## How the Build Is Organized

Three CLI coding agents work in parallel, each on its own git branch, each owning specific parts of the master guide. A human (Donovan) coordinates merges and resolves conflicts.

### Agent Assignments

| Agent | Branch | Parts | Strengths |
|-------|--------|-------|-----------|
| **Codex** (v0.47.0) | `codex/hardening` | 2, 3, 6, 14, 17, 18 | Sandboxed execution, `/plan` mode, code review, security-focused agent roles |
| **Kimi** (v1.12.0) | `kimi/skills` | 5, 8, 9, 10, 11, 12 | 15 MCP servers, 43 skills, choreographer, strongest tool ecosystem |
| **Kiro** (v1.26.2) | `kiro/infra` | 1, 4, 7, 13, 15, 16 | AWS CLI, infrastructure expertise, config analysis |

### Why This Split

- **Codex** gets security/hardening because it has sandboxed execution (can't accidentally break things), a `/plan` mode (propose before executing), and custom agent roles (reviewer, hardener, planner) that are purpose-built for security work.
- **Kimi** gets skills/hooks/autonomy because it has the richest tool ecosystem (15 MCP servers including choreographer for workflow orchestration, memory graph, puppeteer, playwright) and 43 built-in skills.
- **Kiro** gets infrastructure/config/channels because it has native AWS CLI integration, infrastructure expertise, and strong config analysis capabilities.

### If You're a 4th Agent

If you're a new agent joining this build, here's how to slot in:

1. Run the status check procedure below to see where things stand
2. Look at `BUILD-STATUS.md` for unclaimed or blocked tasks
3. Pick up tasks that match your strengths from any agent's backlog
4. Create your own branch: `git checkout -b [your-name]/[focus]`
5. Follow the same commit and coordination protocols below
6. Tell the human what you're taking on so they can update BUILD-STATUS.md

**Good tasks for a generalist agent:** Parts 15 (Maintenance Runbook), 16 (Money-Making), 18 (Edge Cases) — these are documentation-heavy and don't require specialized tools.

## How to Determine Current State

**Run this every time you start a session.** This is your situational awareness check.

### Quick Status (30 seconds)

```bash
cd ~/.openclaw

# 1. What branch am I on? What's the latest?
git branch -a
git log --all --oneline --graph -20

# 2. What's done vs pending?
grep "✅" BUILD-STATUS.md | wc -l    # completed
grep "⬜" BUILD-STATUS.md | head -20  # pending (ignore last line which is instructions)

# 3. Any uncommitted work?
git status
git diff --stat

# 4. What did other agents do recently?
cat workspace/memory/build-log-2026-02-22.md
```

### Deep Audit (2 minutes)

```bash
cd ~/.openclaw

# 1. Full branch comparison — who's ahead of main?
for b in codex/hardening kimi/skills kiro/infra; do
  echo "=== $b ===" 
  git log main..$b --oneline 2>/dev/null || echo "(no commits ahead of main)"
done

# 2. Are there merge conflicts waiting?
for b in codex/hardening kimi/skills kiro/infra; do
  git merge --no-commit --no-ff $b 2>&1 | head -3
  git merge --abort 2>/dev/null
done

# 3. Is OpenClaw actually running?
pgrep -f openclaw && echo "RUNNING" || echo "NOT RUNNING"
openclaw status 2>/dev/null || echo "openclaw CLI not available or not running"

# 4. Config state
cat openclaw.json | python3 -m json.tool > /dev/null 2>&1 && echo "openclaw.json: valid JSON" || echo "openclaw.json: INVALID"

# 5. What's the workspace state?
ls -la workspace/
cat workspace/.openclaw/workspace-state.json
```

### Interpreting Results

| You See | It Means | Do This |
|---------|----------|---------|
| All branches at same commit | No work started yet | Pick your assigned parts and begin |
| Branch ahead of main, BUILD-STATUS shows ✅ | Work done but not merged | Check if dependencies are met, tell human to merge |
| Uncommitted changes on a branch | Agent was interrupted mid-task | Review the changes, decide to commit or discard |
| Merge conflicts | Agents touched overlapping files | Flag to human — don't force-resolve yourself |
| BUILD-STATUS shows ⬜ but branch has commits | Agent forgot to update status | Update BUILD-STATUS.md, then continue |

## How to Do Work

### Before Starting Any Part

1. **Read the master guide section** for your part: `cat building_super_openclaw.md | sed -n '/^# PART N:/,/^# PART/p'` (replace N with part number)
2. **Read your execution guide** if one exists:
   - Codex agents: `codex_openclaw_execution_guide.md`
   - Kimi agents: `kimi_openclaw_execution_guide.md`
   - Other agents: Use the master guide directly
3. **Check dependencies** — see merge order below. Don't start Part 2 if Part 1 isn't done.
4. **Switch to your branch:** `git checkout [your-branch]`

### While Working

- **Commit often** with format: `[agent-name] Part N: short description`
- **Append to build log** (`workspace/memory/build-log-2026-02-22.md`) with timestamped entries
- **Don't modify files owned by other agents** (see file ownership below)

### After Completing a Part

1. Update `BUILD-STATUS.md`: change ⬜ to ✅, add notes
2. Append completion entry to build log
3. Commit: `[agent-name] Part N: complete — description of what was done`
4. Run the verification procedure for that part (see below)

## Dependency & Merge Order

Parts must be completed and merged in this order because later parts depend on earlier ones:

```
Phase 1 — Foundation (no dependencies):
  Parts 1, 4     → Cloud infra exists, config is validated
  Merge: kiro/infra → main

Phase 2 — Hardening (needs a server):
  Parts 2, 3     → Server is secured, OpenClaw is installed
  Merge: codex/hardening → main

Phase 3 — Agent Brain (needs running OpenClaw):
  Parts 5, 8, 9  → Workspace populated, memory working, autonomy configured
  Merge: kimi/skills → main

Phase 4 — Capabilities (needs working agent):
  Parts 6, 7, 10, 11, 12 → Models optimized, channels connected, skills loaded, hooks active, multi-agent running
  Merge: all branches → main (coordinate with human)

Phase 5 — Polish (needs everything above):
  Parts 13, 14, 15, 16, 17, 18 → Remote access, monitoring, maintenance, revenue, kill switch, edge cases
  Merge: remaining branches → main
```

**If you're blocked** because a prerequisite part isn't done: skip to your next non-blocked part, note the block in the build log, and move on.

## File Ownership

To prevent merge conflicts, each agent owns specific areas:

| Agent | Owns (can create/modify) | Read-only |
|-------|--------------------------|-----------|
| Codex | Server configs, systemd units, firewall rules, kill-switch scripts, security audit reports | Everything else |
| Kimi | `workspace/` files (SOUL, IDENTITY, MEMORY, etc.), skills/, hooks config sections in openclaw.json | Everything else |
| Kiro | Cloud provisioning scripts, openclaw.json (infra/channel/gateway sections), Tailscale config, maintenance docs | Everything else |

**Shared files** (all agents may update their own section only):
- `BUILD-STATUS.md` — update only your rows
- `workspace/memory/build-log-*.md` — append only, never delete others' entries
- This `AGENTS.md` — append to the "Build History" section at the bottom only

## Verification Procedures

After completing each part, run these checks. **A part is not done until verification passes.**

### Part 1 — Cloud Infrastructure
```bash
# Can you SSH to the server?
ssh -p 22 user@SERVER_IP "uname -a && free -h && df -h"
# Is it the right spec? (ARM, ≥4 cores, ≥24GB RAM for OCI; or ≥4GB for Hetzner)
```

### Part 2 — Server Hardening
```bash
ssh -p 2222 user@SERVER_IP  # SSH moved to non-standard port?
# fail2ban running?
sudo systemctl status fail2ban
# Unattended upgrades?
sudo systemctl status unattended-upgrades
# Root login disabled?
grep "PermitRootLogin" /etc/ssh/sshd_config  # should be "no"
# Password auth disabled?
grep "PasswordAuthentication" /etc/ssh/sshd_config  # should be "no"
# Firewall active?
sudo ufw status verbose  # or iptables -L
```

### Part 3 — OpenClaw Installation
```bash
# OpenClaw installed and running?
openclaw --version
openclaw status
systemctl status openclaw  # if systemd service exists
# Gateway responding?
curl -s http://127.0.0.1:18789/health || echo "Gateway not responding"
```

### Part 4 — Configuration
```bash
cd ~/.openclaw
# Valid JSON?
python3 -c "import json; json.load(open('openclaw.json'))" && echo "VALID" || echo "INVALID"
# Security audit
openclaw security audit 2>/dev/null || echo "security audit not available"
# No secrets in git?
git log --all -p | grep -i "token\|secret\|password\|apikey" | head -5
```

### Part 5 — Workspace Files
```bash
cd ~/.openclaw/workspace
# All required files exist and non-empty?
for f in SOUL.md IDENTITY.md USER.md AGENTS.md OBSERVER.md TOOLS.md HEARTBEAT.md; do
  [ -s "$f" ] && echo "✅ $f ($(wc -c < "$f") bytes)" || echo "❌ $f MISSING/EMPTY"
done
# BOOTSTRAP.md should be DELETED after bootstrap
[ ! -f BOOTSTRAP.md ] && echo "✅ BOOTSTRAP.md deleted" || echo "⚠️  BOOTSTRAP.md still exists"
# IDENTITY.md should be filled in
grep -q "^\- \*\*Name:\*\*$" IDENTITY.md && echo "⚠️  IDENTITY.md not filled in" || echo "✅ IDENTITY.md populated"
```

### Part 6 — Model Strategy
```bash
# Models configured?
cat ~/.openclaw/agents/main/agent/models.json | python3 -m json.tool | head -20
# Ollama running with local model?
ollama list 2>/dev/null || echo "Ollama not available"
```

### Part 7 — Channel Setup
```bash
# WhatsApp connected?
openclaw channels status 2>/dev/null || grep -q "whatsapp" ~/.openclaw/openclaw.json && echo "WhatsApp configured"
# Telegram bot configured?
grep -q "telegram" ~/.openclaw/openclaw.json && echo "Telegram configured" || echo "Telegram not configured"
```

### Parts 8-12 — Memory, Autonomy, Skills, Hooks, Multi-Agent
```bash
# Memory DB exists?
ls -la ~/.openclaw/memory/main.sqlite
# Cron jobs configured?
cat ~/.openclaw/cron/jobs.json
# Heartbeat state?
cat ~/.openclaw/workspace/memory/heartbeat-state.json
# Skills directory?
ls ~/.openclaw/workspace/skills/ 2>/dev/null || echo "No skills dir yet"
# Hooks enabled?
grep -A5 '"hooks"' ~/.openclaw/openclaw.json
# Named agents configured?
grep -A5 '"named"' ~/.openclaw/openclaw.json || echo "No named agents yet"
```

### Parts 13-18 — Tailscale, Monitoring, Maintenance, Revenue, Kill Switch, Edge Cases
```bash
# Tailscale connected?
tailscale status 2>/dev/null || echo "Tailscale not installed/connected"
# Kill switch script exists?
ls ~/.openclaw/kill-switch.sh 2>/dev/null || echo "No kill switch yet"
# Maintenance runbook exists?
ls ~/.openclaw/MAINTENANCE.md 2>/dev/null || echo "No maintenance runbook yet"
```

### Full Build Audit (run when you think everything is done)

```bash
cd ~/.openclaw
echo "=== BUILD AUDIT ==="
echo ""
echo "Parts completed: $(grep -c '✅' BUILD-STATUS.md)"
echo "Parts pending:   $(grep '⬜' BUILD-STATUS.md | grep -v 'Change' | wc -l)"
echo ""
echo "Git state:"
git log --all --oneline --graph -30
echo ""
echo "Branch status:"
for b in codex/hardening kimi/skills kiro/infra; do
  ahead=$(git log main..$b --oneline 2>/dev/null | wc -l)
  echo "  $b: $ahead commits ahead of main"
done
echo ""
echo "Uncommitted changes:"
git status --short
echo ""
echo "Config valid: $(python3 -c 'import json; json.load(open("openclaw.json"))' 2>&1 && echo YES || echo NO)"
echo ""
echo "Sensitive files in git:"
git ls-files | grep -iE 'auth|token|secret|\.env|credential|password' || echo "  None (good)"
echo ""
echo "OpenClaw status:"
openclaw status 2>/dev/null || echo "  Not running or CLI not available"
```

## Current Runtime State (as of bootstrap)

What's already working:
- OpenClaw v2026.2.21-2 installed locally
- Gateway configured on port 18789 (loopback)
- WhatsApp channel connected (self-chat mode, DM allowlist)
- Models configured: Claude Sonnet 4, Claude Opus 4, GPT-4.1, Gemini 2.5 Pro, local Qwen3 8B
- Memory SQLite DB exists (69KB)
- Heartbeat configured (every 30m)
- Hooks enabled (session-memory, boot-md, bootstrap-extra-files, command-logger)
- Subagents: maxConcurrent 8, maxSpawnDepth 2, maxChildrenPerAgent 5

What's NOT done yet:
- No cloud VPS (running locally only)
- No server hardening
- Workspace not bootstrapped (IDENTITY.md blank, BOOTSTRAP.md still exists)
- No cron jobs configured
- No skills installed
- No named agents (only defaults)
- No Tailscale
- No kill switch
- No maintenance runbook

## Execution Guides

Two agent-specific execution guides exist that map every master guide task to specific CLI commands and tools:

- `codex_openclaw_execution_guide.md` — For Codex CLI. Includes recommended profiles (`openclaw-build`, `openclaw-audit`, `openclaw-yolo`), agent roles (reviewer, planner, hardener, explorer), and exact commands per part.
- `kimi_openclaw_execution_guide.md` — For Kimi CLI. Maps tasks to specific MCP servers (choreographer, omega, filesystem, memory, sqlite, puppeteer, playwright, etc.) and skills (`/skill:security-engineering`, `/skill:architecture-design`, etc.).

If you're an agent without a dedicated execution guide, use the master guide (`building_super_openclaw.md`) directly. The parts are self-contained with exact commands and configs.

## Communication Protocol

- Agents don't communicate directly with each other
- Coordination happens through `BUILD-STATUS.md`, the build log, and git history
- The human (Donovan) resolves conflicts and decides merge timing
- If blocked, note it in the build log and skip to your next non-blocked task
- If you discover something that affects another agent's work, note it in the build log with `⚠️ CROSS-AGENT NOTE:` prefix

## Critical Rules

1. **Never commit secrets to git.** The `.gitignore` excludes `.env`, `openclaw.json`, auth files, credentials, and device identity. If you create new files with secrets, add them to `.gitignore` first.
2. **Don't modify `openclaw.json` without backing it up first:** `cp openclaw.json openclaw.json.bak`
3. **Use `trash` over `rm`** when deleting anything important.
4. **Test before committing.** Run the verification procedure for your part.
5. **Append to the build log, never overwrite it.**
6. **Stay on your branch.** Don't commit to `main` directly.

---

## Build History

_Agents: append entries here as you complete work. Format: `YYYY-MM-DD HH:MM — [Agent] Part N: what was done`_

2026-02-22 15:14 — [Kiro] Setup: Initialized git repo, created orchestration scaffold (BUILD-STATUS.md, AGENTS-COORDINATION.md, openclaw-build.sh, .gitignore), created 3 agent branches
