# KIRO.md — Prompting, Planning & Task Guide for the OpenClaw Multi-Agent Build

> **Purpose:** Map each CLI agent's real capabilities to the OpenClaw build tasks where they're strongest. Use this to know exactly which agent to use, how to prompt it, and what tools/MCPs to leverage for each part.

---

## Agent Capability Matrix

### Kiro CLI (v1.26.2) — Infrastructure & Config Specialist

**Model:** Claude Sonnet/Opus (auto-selected)

**Built-in Tools:**
- `execute_bash` — Run shell commands directly
- `fs_read` / `fs_write` — File operations with line-level precision
- `grep` / `glob` — Pattern search and file discovery
- `code` — LSP-powered code intelligence (search symbols, find references, AST patterns)
- `knowledge` — Index and semantically search local files/docs
- `web_search` / `web_fetch` — Live internet access
- `use_subagent` — Delegate parallel subtasks to specialized subagents
- `use_aws` — **Native AWS CLI integration** (unique to Kiro)
- `puppeteer` — Browser automation
- `sequentialthinking` — Chain-of-thought reasoning
- `todo_list` — Multi-step task tracking

**MCP Servers (9):**
brave-search, fetch, filesystem, git, github, memory, puppeteer, sequential-thinking, serena (LSP)

**Unique Strengths:**
- Only agent with native AWS CLI (`use_aws` tool)
- Knowledge base indexing — can ingest the 89KB master guide and search it semantically
- Subagent delegation for parallel work
- LSP code intelligence via Serena
- Custom agent profiles (create task-specific agents)
- Steering files for persistent context
- Hooks for automated actions on file save/create

**Slash Commands:** `/model`, `/save`, `/load`, `/usage`, `/code init`, `/editor`, `/prompts`

---

### Codex CLI (v0.47.0) — Security & Review Specialist

**Model:** gpt-5.3-codex (flagship, also gpt-5.3-codex-spark for speed)

**Built-in Tools:**
- Shell execution (sandboxed by default)
- File read/write with `apply_patch`
- Web search (opt-in via `--search`)
- Image input (`-i`)
- Git-aware: ghost snapshots, undo per turn

**MCP Servers (16):**
filesystem, memory, sqlite, fetch, puppeteer, sequential-thinking, github, brave-search, context7, playwright, chrome-devtools, tavily, notion, linear, exa, ultimate-mcp

**Unique Strengths:**
- **Sandbox enforcement** — read-only, workspace-write, or full-access modes
- **`/plan` mode** — propose changes before executing (critical for security work)
- **`/review` mode** — 4 presets for code/config review
- **Multi-agent roles** — custom agents via config.toml (reviewer, planner, hardener, explorer)
- **`/compact`** — summarize conversation to free context window
- **`/diff`** — show all changes including untracked files
- **`exec` mode** — non-interactive, scriptable, JSON output for pipelines
- **Cloud exec** — offload tasks to cloud workers
- **Profile system** — switch between openclaw-build, openclaw-audit, openclaw-yolo configs
- **Undo** — per-turn git ghost snapshots

**Slash Commands:** `/plan`, `/review`, `/compact`, `/diff`, `/agent`, `/fork`, `/resume`, `/permissions`, `/approvals`, `/status`, `/mcp`, `/ps`

**⚠️ CLI Bug:** `model_reasoning_effort = "xhigh"` in `~/.codex/config.toml` is valid for gpt-5.3-codex at the API level, but Codex CLI v0.47.0 hasn't updated its config parser to accept it yet (known issue). Temporarily set to `"high"` to unblock CLI startup, or check if a newer CLI version has landed the fix.

---

### Kimi CLI (v1.12.0) — Skills & Integration Specialist

**Model:** Kimi K2.5 (also supports external models)

**Built-in Tools:**
- Task (subagent dispatch), Shell, ReadFile, ReadMediaFile, Glob, Grep
- WriteFile, StrReplaceFile, SearchWeb, FetchURL, SetTodoList

**MCP Servers (15):**
choreographer, omega, filesystem, memory, sqlite, fetch, puppeteer, sequential-thinking, github, brave-search, context7, playwright, chrome-devtools, tavily, exa

**43 Skills** (invoke with `/skill:name`):
- **Dev Core:** code-review-refactoring, debugging-root-cause-analysis, test-driven-development, performance-engineering, security-engineering, api-integration, database-design-optimization, architecture-design, observability-monitoring, multi-agent-orchestration
- **AI/Agent:** agent-cognitive-architecture, optimize-prompt, create-plan, hostile-auditor, spec-forge, mcp-builder
- **Docs:** docx, pptx, pdf, xlsx
- **GitHub:** gh-address-comments, gh-fix-ci
- **Web/Infra:** web-artifacts-builder, webapp-testing, cloudflare-403-triage

**Unique Strengths:**
- **Choreographer MCP** — custom workflow orchestration (unique to Kimi)
- **Omega MCP** — security ops, Docker, browser, network tools
- **43 skills** — pre-built specialist behaviors invokable on demand
- **`/skill:mcp-builder`** — can build new MCP servers
- **`/skill:agent-cognitive-architecture`** — design agent personalities/behaviors
- **`/skill:hostile-auditor`** — adversarial security review
- **Ralph mode** — iterative refinement loops
- **ACP server** — connect to editors (Zed, etc.)
- **Print mode** — non-interactive for scripting (`kimi --quiet -p "prompt"`)

**Slash Commands:** `/skill:*`, `/compact`, `/status`, `/model`, `/help`

---

## Part-by-Part Task Guide

### Phase 1 — Foundation (No Dependencies)

#### Part 1: Cloud Infrastructure → **Kiro**

Why Kiro: Native `use_aws` tool for OCI/cloud API calls, infrastructure expertise.

```
Prompt for Kiro:
"Read Part 1 of building_super_openclaw.md (lines 105-235). I need a cloud
VPS provisioned. Compare Oracle Cloud Free Tier ARM (4 OCPU, 24GB) vs
Hetzner CAX21 ($8.50/mo). Check current OCI ARM capacity availability.
If OCI is available, walk me through provisioning step by step including
the Security List firewall rules. If not, provision Hetzner via API."
```

#### Part 4: Configuration Validation → **Kiro**

Why Kiro: Config analysis, can index the master guide and cross-reference.

```
Step 1 — Index the reference:
"Index building_super_openclaw.md into your knowledge base. Then read
Part 4 (lines 474-626). Compare our current openclaw.json against the
reference config. List every missing field, every deviation, and every
security concern. Back up openclaw.json first."

Step 2 — Apply fixes:
"Apply the recommended changes from your analysis. Validate the result
with python3 JSON parsing. Do NOT touch auth tokens — only structural
config improvements."
```

---

### Phase 2 — Hardening (Needs Server from Phase 1)

#### Part 2: Server Hardening → **Codex**

Why Codex: Sandboxed execution prevents accidental damage. `/plan` mode proposes before executing.

```
Step 1 — Plan:
codex --cd ~/.openclaw -p openclaw-build "/plan
Read Part 2 of building_super_openclaw.md (lines 236-402).
Create a hardening plan for our VPS: SSH key-only on port 2222,
fail2ban, ufw, unattended-upgrades. Propose every change before
executing. CRITICAL: add port 2222 to firewall BEFORE changing SSH."

Step 2 — Execute with review:
codex --cd ~/.openclaw -p openclaw-build
"/review the hardening changes we just made. Check for:
1. Can we still SSH in on the new port?
2. Is root login disabled?
3. Are all unnecessary ports closed?
4. Is fail2ban monitoring SSH?"
```

#### Part 3: OpenClaw Installation & Security → **Codex**

Why Codex: Security audit capabilities, sandbox for safe testing.

```
codex --cd ~/.openclaw -p openclaw-build "/plan
Read Part 3 of building_super_openclaw.md (lines 403-473).
Install OpenClaw on the VPS via npm. Set up systemd service.
Rotate the gateway auth token. Verify the health endpoint.
Use /review after each step to audit security."
```

---

### Phase 3 — Agent Brain (Needs Running OpenClaw)

#### Part 5: Workspace Files → **Kimi**

Why Kimi: `/skill:agent-cognitive-architecture` for designing agent personality.

```
kimi -w ~/.openclaw/workspace --thinking -p "
Read Part 5 of ../building_super_openclaw.md (lines 627-877).
Use /skill:agent-cognitive-architecture to design the agent identity.

1. Fill in IDENTITY.md — name the agent, define its creature type, vibe, emoji
2. Fill in USER.md with Donovan's details (timezone: CST, pronouns: he/him)
3. Review and enhance SOUL.md based on the master guide recommendations
4. Delete BOOTSTRAP.md when done
5. Create workspace/MEMORY.md as the long-term memory file

Make the identity feel authentic, not generic."
```

#### Part 8: Memory System → **Kimi**

Why Kimi: Has sqlite MCP for direct DB queries, memory MCP for knowledge graph.

```
kimi -w ~/.openclaw --thinking -p "
Read Part 8 of building_super_openclaw.md (lines 1139-1283).
Use the sqlite MCP to inspect ~/.openclaw/memory/main.sqlite — show
tables, schema, and current row counts.
Configure memory search in openclaw.json per the guide.
Set up workspace memory sync. Test retrieval with a sample query."
```

#### Part 9: Autonomy Engine → **Kimi**

Why Kimi: Choreographer MCP for workflow orchestration, skill ecosystem.

```
kimi -w ~/.openclaw --thinking -p "
Read Part 9 of building_super_openclaw.md (lines 1284-1384).
Use /skill:create-plan to design the autonomy configuration:
1. Configure cron jobs in cron/jobs.json (morning briefing, periodic checks)
2. Enhance HEARTBEAT.md with the monitoring schedule
3. Set up heartbeat-state.json tracking
4. Test a cron job execution"
```

---

### Phase 4 — Capabilities (Needs Working Agent)

#### Part 6: Model Strategy → **Codex**

Why Codex: Multi-model expertise (runs on GPT-5.3), can benchmark and compare.

```
codex --cd ~/.openclaw --search "/plan
Read Part 6 of building_super_openclaw.md (lines 878-991).
Analyze our current model config (agents/main/agent/models.json).
Design an optimal model strategy:
- Primary: local Ollama qwen3:8b (free, fast)
- Fallback: Claude Sonnet 4 (quality)
- Deep thinking: Claude Opus 4 (expensive, powerful)
- Image: Claude Sonnet 4
Configure fallback chains and cost estimates per model."
```

#### Part 7: Channel Setup → **Kiro**

Why Kiro: Config analysis, can validate channel configs against docs.

```
Prompt for Kiro:
"Read Part 7 of building_super_openclaw.md (lines 992-1138).
WhatsApp is already connected. Set up:
1. Telegram bot — guide me through BotFather setup, then configure in openclaw.json
2. Discord bot — create application, configure token and permissions
Validate each channel config against the OpenClaw docs."
```

#### Part 10: Skills Installation → **Kimi**

Why Kimi: Has `/skill:*` system, can test skills directly.

```
kimi -w ~/.openclaw --thinking -p "
Read Part 10 of building_super_openclaw.md (lines 1385-1553).
1. Create ~/.openclaw/workspace/skills/ directory
2. Install the skills listed in the guide
3. Test each skill with a simple invocation
4. Configure skills.load.extraDirs in openclaw.json
Use /skill:mcp-builder if we need custom skills."
```

#### Part 11: Plugin Hooks → **Kimi**

Why Kimi: Omega MCP for system-level hooks, choreographer for workflow design.

```
kimi -w ~/.openclaw --thinking -p "
Read Part 11 of building_super_openclaw.md (lines 1554-1854).
Design and implement the hook pipeline:
1. Review current hooks (session-memory, boot-md, bootstrap-extra-files, command-logger)
2. Add hooks per the guide recommendations
3. Test the event pipeline end-to-end
Use /skill:observability-monitoring to set up hook logging."
```

#### Part 12: Multi-Agent Architecture → **Kimi**

Why Kimi: `/skill:multi-agent-orchestration`, choreographer MCP.

```
kimi -w ~/.openclaw --thinking -p "
Read Part 12 of building_super_openclaw.md (lines 1855-2026).
Use /skill:multi-agent-orchestration to design the agent fleet:
- main: ollama/qwen3:8b (personal, Telegram)
- deep: claude-opus-4 (research, high thinking)
- coder: claude-sonnet-4 (Discord, sandbox)
- monitor: ollama/qwen3:8b (background, read-only)
Configure named agents, routing, trust boundaries, and circuit breakers
in openclaw.json. Back up config first."
```

---

### Phase 5 — Polish (Needs Everything Above)

#### Part 13: Tailscale Remote Access → **Kiro**

Why Kiro: Infrastructure/networking expertise.

```
Prompt for Kiro:
"Read Part 13 of building_super_openclaw.md (lines 2027-2095).
Install Tailscale on the VPS. Configure openclaw.json gateway.tailscale
settings. Set up serve/funnel mode for secure remote access.
Test connectivity from a separate device."
```

#### Part 14: Cost Control → **Codex**

Why Codex: Analytical, can audit token usage and build monitoring dashboards.

```
codex --cd ~/.openclaw --search "/plan
Read Part 14 of building_super_openclaw.md (lines 2096-2205).
1. Analyze current API costs across all configured models
2. Set up token usage tracking and budget alerts
3. Create a cost monitoring script
4. Configure model fallback thresholds based on budget"
```

#### Part 15: Maintenance Runbook → **Kiro**

Why Kiro: Documentation generation, infrastructure knowledge.

```
Prompt for Kiro:
"Read Part 15 of building_super_openclaw.md (lines 2206-2283).
Create MAINTENANCE.md with procedures for:
- OpenClaw updates (npm update process)
- Backup procedures (config, memory, workspace)
- Recovery from crashes
- Log rotation
- Certificate renewal (if applicable)
Make it actionable — exact commands, not just descriptions."
```

#### Part 16: Money-Making Configurations → **Kiro**

Why Kiro: Config expertise, can design and validate agent configs.

```
Prompt for Kiro:
"Read Part 16 of building_super_openclaw.md (lines 2284-2430).
Design revenue-generating agent configurations:
- Content creation agent
- Research/analysis agent
- Customer support agent
For each, provide the openclaw.json config snippet, required skills,
and channel routing setup."
```

#### Part 17: Kill Switch → **Codex**

Why Codex: Security-critical, needs sandboxed testing and `/review` audit.

```
codex --cd ~/.openclaw -p openclaw-audit "/plan
Read Part 17 of building_super_openclaw.md (lines 2431-2518).
Create kill-switch.sh that:
1. Stops all OpenClaw processes immediately
2. Revokes all API tokens
3. Disconnects all channels
4. Preserves logs for forensics
5. Sends alert notification
/review the script for completeness and test in dry-run mode."
```

#### Part 18: Edge Cases → **Codex**

Why Codex: `/review` mode, hostile-auditor mindset, reads everything.

```
codex --cd ~/.openclaw -p openclaw-audit -s read-only
"Read Part 18 of building_super_openclaw.md (lines 2519-end).
Also read the entire openclaw.json, all workspace files, and the
kill-switch.sh. /review everything for:
1. Undocumented gotchas mentioned in Part 18
2. Config contradictions
3. Security gaps
4. Missing error handling
Produce a final audit report."
```

---

## Quick Reference: When to Use Which Agent

| Situation | Use | Why |
|-----------|-----|-----|
| AWS/cloud provisioning | **Kiro** | Native `use_aws` tool |
| Config validation | **Kiro** | Knowledge base indexing + config analysis |
| Security hardening | **Codex** | Sandbox + `/plan` + `/review` |
| Code/script review | **Codex** | `/review` with 4 presets |
| Dangerous operations | **Codex** | Sandbox enforcement, undo per turn |
| Agent personality design | **Kimi** | `/skill:agent-cognitive-architecture` |
| Skill installation | **Kimi** | 43 built-in skills, `/skill:mcp-builder` |
| Database inspection | **Kimi** | sqlite MCP server |
| Workflow orchestration | **Kimi** | Choreographer MCP |
| Multi-agent architecture | **Kimi** | `/skill:multi-agent-orchestration` |
| Documentation generation | **Kiro** | Subagent delegation, knowledge bases |
| Browser automation | **Kimi** or **Codex** | Both have playwright + puppeteer |
| Non-interactive scripting | **Codex** `exec` or **Kimi** `--quiet` | Both support headless mode |
| Parallel subtasks | **Kiro** | `use_subagent` for concurrent work |
| Live web research | Any | All three have web search |

## Pre-Flight Checklist

Before starting any agent on a task:

```bash
# 1. Workaround for Codex CLI xhigh parsing bug (if CLI version < 0.48)
# xhigh is valid for gpt-5.3-codex but CLI parser may not accept it yet
codex --version | grep -q "0.47" && sed -i 's/model_reasoning_effort = "xhigh"/model_reasoning_effort = "high"/' ~/.codex/config.toml && echo "Temporarily set to high (xhigh not yet supported in CLI parser)"

# 2. Verify all agents work
codex --version && kimi --version && kiro-cli --version

# 3. Check you're on the right branch
cd ~/.openclaw && git branch

# 4. Read current status
cat BUILD-STATUS.md | grep -E "✅|⬜"
```

---

*Generated 2026-02-22 by Kiro CLI as part of the OpenClaw multi-agent build orchestration.*
