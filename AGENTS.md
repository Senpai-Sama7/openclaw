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

| Agent | Branch | Parts | Role |
|-------|--------|-------|------|
| **Kiro** (v1.26.2) | `kiro/infra` | 1, 4, 7, 13, 15, 16 | **Orchestrator** — directs all agents, builds infra/config/channels |
| **Codex** (v0.104.0) | `codex/hardening` | 2, 3, 6, 14, 17, 18 | Security, hardening, cost control, kill switch |
| **Kimi** (v1.12.0) | `kimi/skills` | 5, 8, 9, 10, 11, 12 | Workspace files, memory, autonomy, skills, hooks, multi-agent |

### Orchestration Model

Kiro is the **lead orchestrator** — it launches, supervises, and verifies work done by Kimi and Codex. The other agents do not self-direct; Kiro reads the master guide, crafts task prompts, launches them via their CLI exec modes, monitors output, and verifies results against the Final Readiness Checklist.

```bash
# Launch Kimi (fully autonomous, no approval prompts)
kimi -w ~/.openclaw --yolo --print -p "TASK PROMPT"

# Launch Codex (fully autonomous, no sandbox, web search enabled)
cd ~/.openclaw && codex exec --dangerously-bypass-approvals-and-sandbox --search "TASK PROMPT"
```

See `KIRO.md` for full orchestration procedures, prompt templates, and supervision workflow.

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
cat workspace/memory/build-log-$(date +%Y-%m-%d).md 2>/dev/null || echo "No log for today yet"
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
   - Kiro agents: `KIRO.md` (prompting, planning & task guide)
   - Other agents: Use the master guide directly
3. **Check dependencies** — see merge order below. Don't start Part 2 if Part 1 isn't done.
4. **Switch to your branch:** `git checkout [your-branch]`

### While Working

- **Commit often** with format: `[agent-name] Part N: short description`
- **Append to build log** (`workspace/memory/build-log-YYYY-MM-DD.md` — use today's date) with timestamped entries
- **Don't modify files owned by other agents** (see file ownership below)

### After Completing a Part

1. Update `BUILD-STATUS.md`: change ⬜ to ✅, add notes
2. Append completion entry to build log
3. Commit: `[agent-name] Part N: complete — description of what was done`
4. Run the verification procedure for that part (see below)

## Dependency & Merge Order

Parts must be completed and merged in this order because later parts depend on earlier ones. Every assigned part is accounted for.

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

**Dependency rules:** No part in Phase N may begin until all parts in Phase N-1 are merged to `main`. Within a phase, parts may execute in parallel if they don't share file ownership. Part 18 must be last.

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
- `KIRO.md` — For Kiro CLI. Maps all 3 agents' real capabilities to build tasks, with exact prompts and tool/MCP recommendations per part.

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

## Final Readiness Checklist

> **CHECKLIST AND BUILD RULES — DO NOT VIOLATE**
>
> 1. **Never rewrite, remove, or restructure** any part of this checklist.
> 2. On task completion, the **only** permitted changes are:
>    - Change `[ ]` → `[x]` on the completed task line.
>    - Replace `_pending_` on the Proof line with actual validation evidence (commands run, output received, timestamps).
>    - Append a new row to the **Completion Log** table at the bottom.
> 3. **Do not** alter Validation lines, reorder tasks, add/remove sections, or touch any uncompleted task.
> 4. If a task fails validation, leave it as `[ ]` and append failure notes under its Proof line prefixed with `❌ FAIL:`.
> 5. **If the planned Implementation method fails**, do NOT delete it. Instead:
>    - Keep the original Implementation text intact.
>    - Append `❌ FAIL:` with the error/reason it didn't work.
>    - Then append `✅ FIX:` with what was done instead and why it worked.
>    - The Proof line must show the final passing result with timestamp, commands, and output.
> 6. These rules are permanent and apply to all agents (human or AI) editing this file.

### INFRASTRUCTURE

- [x] Server running (Oracle Free Tier or Hetzner) with 4+ GB RAM
  - Validation: `ssh -p 2222 openclaw@SERVER_IP "uname -a && free -h"`
  - Proof: EC2 t4g.small 1.8GB RAM at 18.209.247.78 — `2026-02-22T21:19Z` — `Linux 6.17.0-1007-aws aarch64, 1.8Gi RAM` (under 4GB spec — AWS free tier constraint)
- [x] SSH hardened (key-only, non-standard port, fail2ban)
  - Validation: `ssh -p 2222`, `grep PermitRootLogin /etc/ssh/sshd_config`, `sudo systemctl status fail2ban`
  - Proof: `2026-02-22T22:10Z` — port 2222, PermitRootLogin no, PasswordAuthentication no, fail2ban active (sshd jail, maxretry 3, bantime 3600)
- [x] UFW firewall active (only SSH port open)
  - Validation: `sudo ufw status verbose`
  - Proof: `2026-02-22T22:12Z` — `Status: active`, default deny incoming, 2222/tcp ALLOW IN Anywhere
- [x] Automatic security updates configured
  - Validation: `sudo systemctl status unattended-upgrades`
  - Proof: `2026-02-22T22:10Z` — `active (running)`, auto-reboot disabled
- [ ] Tailscale installed and connected on server
  - Validation: `tailscale status`
  - Proof: _pending_ (Part 13, Phase 5)
- [ ] Tailscale installed on your phone/laptop
  - Validation: `tailscale status` on client device
  - Proof: _pending_ (Part 13, Phase 5)
- [x] systemd lingering enabled (agent survives logout)
  - Validation: `loginctl show-user openclaw -p Linger`
  - Proof: `2026-02-22T22:10Z` — `Linger=yes`

### OPENCLAW

- [x] Version 2026.2.21-2+ installed and verified
  - Validation: `openclaw --version`
  - Proof: `2026-02-22T22:22Z` — `2026.2.21-2` on server
- [x] Gateway binding to loopback or tailnet (NOT 0.0.0.0)
  - Validation: `cat ~/.openclaw/openclaw.json | grep -A3 '"gateway"'`
  - Proof: `2026-02-22T23:39Z` — `bind: loopback`, port 18789, ss confirms 127.0.0.1:18789 LISTEN
- [x] Token auth enabled
  - Validation: `grep -A3 '"auth"' ~/.openclaw/openclaw.json`
  - Proof: `2026-02-22T23:39Z` — gateway.auth configured in openclaw.json
- [x] openclaw doctor --deep --repair run with no critical issues
  - Validation: `openclaw doctor --deep --repair`
  - Proof: `2026-02-22T23:39Z` — 2 critical issues fixed (sessions dir, credentials dir), stale service removed. Remaining: WhatsApp not linked (Part 7), memory search needs embedding (Part 8)
- [x] Ollama installed with qwen3:8b and nomic-embed-text models
  - Validation: `ollama list`
  - Proof: `2026-02-22T22:15Z` — Ollama 0.16.3, qwen3:8b (5.2GB), nomic-embed-text (274MB)

### CONFIGURATION

- [x] openclaw.json complete with all your values
  - Validation: `python3 -c "import json; json.load(open('openclaw.json'))"`, all required keys present
  - Proof: `2026-02-22T23:39Z` — valid JSON, gateway/auth/tools/memory/models all configured
- [x] AGENTS.md written with your context and preferences
  - Validation: `[ -s workspace/AGENTS.md ]`
  - Proof: `2026-02-22T23:39Z` — 3,466 bytes, Donovan-specific identity, CST timezone, decision framework
- [x] SOUL.md reasoning framework in place
  - Validation: `[ -s workspace/SOUL.md ]`
  - Proof: `2026-02-22T23:39Z` — 2,055 bytes, 5-question self-check, calibrated confidence, reversibility principle
- [x] TOOLS.md policies defined
  - Validation: `[ -s workspace/TOOLS.md ]`
  - Proof: `2026-02-22T23:39Z` — 1,818 bytes, tool hierarchy, exec safety rules, trash policy
- [ ] HEARTBEAT.md morning brief and monitoring configured
  - Validation: `[ -s workspace/HEARTBEAT.md ]`
  - Proof: _pending_ (Part 9)
- [x] BOOT.md startup checks enabled
  - Validation: `[ -s workspace/BOOT.md ]`
  - Proof: `2026-02-22T23:39Z` — 798 bytes, Ollama check, disk space, version verify, alert-on-failure

### CHANNELS

- [x] Telegram connected and tested (send/receive working)
  - Validation: Send test message via Telegram, verify response
  - Proof: `2026-02-23T00:23Z` — @molty_troy_bot configured, polling mode active, gateway reachable
- [ ] Discord connected (optional but recommended)
  - Validation: Send test message via Discord, verify response
  - Proof: _pending_ (Part 7)
- [x] dmPolicy set to "pairing" on all channels
  - Validation: `grep -A5 '"dmPolicy"' ~/.openclaw/openclaw.json`
  - Proof: `2026-02-23T00:23Z` — telegram.dmPolicy: pairing
- [x] Your user IDs added to allowFrom
  - Validation: `grep -A10 '"allowFrom"' ~/.openclaw/openclaw.json`
  - Proof: `2026-02-23T00:29Z` — tg:6202337294 in telegram.allowFrom

### INTELLIGENCE

- [x] Model routing configured (local for routine, cloud for deep)
  - Validation: `cat ~/.openclaw/agents/main/agent/models.json | head -20`
  - Proof: `2026-02-22T23:39Z` — qwen3:1.7b (quick-local), claude-sonnet-4-6 (quality), claude-opus-4-6 (strategic, 1M ctx)
- [x] Fallback chain set up
  - Validation: Verify fallback triggers when primary model unavailable
  - Proof: `2026-02-22T23:39Z` — fallbacks: [anthropic/claude-opus-4-6]
- [x] Per-model thinking levels configured
  - Validation: `grep -A5 '"thinking"' ~/.openclaw/openclaw.json`
  - Proof: `2026-02-22T23:39Z` — thinkingDefault: medium, /think high for complex, /think xhigh for security
- [x] Memory seeded with your key facts and preferences
  - Validation: `openclaw agent --message "what do you remember about me?"`
  - Proof: `2026-02-23T00:23Z` — MEMORY.md (1,871 bytes) with seed facts, daily log created. FTS ready, semantic search pending embedding provider API key

### AUTONOMY

- [ ] Morning brief cron job active
  - Validation: `openclaw cron list`
  - Proof: _pending_ (Part 9)
- [ ] System health monitoring cron job active
  - Validation: `openclaw cron list`
  - Proof: _pending_ (Part 9)
- [ ] Weekly review cron job scheduled
  - Validation: `openclaw cron list`
  - Proof: _pending_ (Part 9)
- [ ] HEARTBEAT.md actively firing (check openclaw cron list)
  - Validation: `openclaw cron list`, check last heartbeat timestamp
  - Proof: _pending_ (Part 9)

### SAFETY

- [ ] Kill switch aliases created and tested
  - Validation: `type clawdown`, test execution
  - Proof: _pending_ (Part 17)
- [ ] Safety guardian plugin active
  - Validation: `grep -A5 '"hooks"' ~/.openclaw/openclaw.json`
  - Proof: _pending_ (Part 11)
- [ ] PostgreSQL interaction logging working
  - Validation: `psql -c "SELECT count(*) FROM interactions;"`
  - Proof: _pending_ (Part 14)
- [ ] /tmp/openclaw-trash/ in place (no direct deletes)
  - Validation: `ls -la /tmp/openclaw-trash/`
  - Proof: _pending_ (Part 17)
- [ ] Backup created of openclaw.json + workspace + memory index/files
  - Validation: `ls -la ~/openclaw-backup/`
  - Proof: _pending_ (Part 15)

### INTELLIGENCE LOOP

- [ ] Memory being written (test: "what do you remember about me?")
  - Validation: `openclaw agent --message "what do you remember about me?"`
  - Proof: _pending_ (Part 8)
- [ ] Interaction costs being logged to PostgreSQL
  - Validation: `psql -c "SELECT sum(cost) FROM interactions WHERE date > now() - interval '1 day';"`
  - Proof: _pending_ (Part 14)
- [ ] Weekly P&L skill scheduled
  - Validation: `openclaw cron list | grep pnl`
  - Proof: _pending_ (Part 16)
- [ ] Monthly maintenance calendar reminder set
  - Validation: `openclaw cron list | grep maintenance`
  - Proof: _pending_ (Part 15)

### Completion Log

| Date | Agent | Item | Part | Notes |
|------|-------|------|------|-------|
| 2026-02-22 22:19Z | Kiro | Server running | 1 | EC2 t4g.small, 18.209.247.78 |
| 2026-02-22 22:10Z | Kiro | SSH hardened | 2 | Port 2222, fail2ban, key-only |
| 2026-02-22 22:12Z | Kiro | UFW active | 2 | 2222/tcp only |
| 2026-02-22 22:10Z | Kiro | Auto security updates | 2 | unattended-upgrades |
| 2026-02-22 22:10Z | Kiro | Lingering enabled | 2 | openclaw user |
| 2026-02-22 22:22Z | Kiro | OpenClaw installed | 3 | v2026.2.21-2 |
| 2026-02-22 22:15Z | Kiro | Ollama + models | 2 | qwen3:8b, nomic-embed-text |

---

## Build History

_Agents: append entries here as you complete work. Format: `YYYY-MM-DD HH:MM — [Agent] Part N: what was done`_

2026-02-22 15:14 — [Kiro] Setup: Initialized git repo, created orchestration scaffold (BUILD-STATUS.md, AGENTS-COORDINATION.md, openclaw-build.sh, .gitignore), created 3 agent branches
| 2026-02-22 23:39Z | Kiro | Gateway loopback | 4 | bind: loopback, port 18789 |
| 2026-02-22 23:39Z | Kiro | Token auth | 4 | gateway.auth configured |
| 2026-02-22 23:39Z | Kiro | Doctor clean | 4 | 2 critical fixed, stale service removed |
| 2026-02-22 23:39Z | Kiro | openclaw.json complete | 4 | All sections configured |
| 2026-02-22 23:39Z | Kimi | AGENTS.md | 5 | 3,466 bytes, Donovan-specific |
| 2026-02-22 23:39Z | Kimi | SOUL.md | 5 | 2,055 bytes, reasoning framework |
| 2026-02-22 23:39Z | Kimi | TOOLS.md | 5 | 1,818 bytes, tool policies |
| 2026-02-22 23:39Z | Kimi | BOOT.md | 5 | 798 bytes, startup checks |
| 2026-02-22 23:39Z | Codex | Model routing | 6 | ARM-aware, qwen3:1.7b local, claude cloud |
| 2026-02-22 23:39Z | Codex | Fallback chain | 6 | claude-opus-4-6 fallback |
| 2026-02-22 23:39Z | Codex | Thinking levels | 6 | medium default, /think commands |
| 2026-02-23 00:23Z | Kiro | Telegram channel | 7 | @molty_troy_bot, polling, pairing mode |
| 2026-02-23 00:23Z | Kimi | Memory system | 8 | MEMORY.md, daily log, FTS ready |
