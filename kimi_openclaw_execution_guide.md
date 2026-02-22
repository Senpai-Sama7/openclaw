# 🦞🤖 KIMI CLI × OPENCLAW: EXECUTION PLAYBOOK
### Using Every Kimi Skill, MCP Server, and Tool to Build Your OpenClaw Agent
**Version: February 22, 2026 | Kimi CLI v1.12.0 | OpenClaw v2026.2.21-2**

---

> **What this document is:** A step-by-step execution guide that maps every task
> in `building_super_openclaw.md` to the specific Kimi CLI skill, MCP server,
> tool, or command that accomplishes it. Checklist format. Real commands. No fluff.

---

## YOUR KIMI ARSENAL — QUICK REFERENCE

### Built-in Tools (Default Agent)
```
Task            — Dispatch subagents for parallel work
SetTodoList     — Track multi-step progress
Shell           — Execute commands (requires approval)
ReadFile        — Read files (max 1000 lines/read)
ReadMediaFile   — Read images/video
Glob            — Find files by pattern
Grep            — Search file content (ripgrep)
WriteFile       — Create/overwrite files
StrReplaceFile  — Surgical string replacement edits
SearchWeb       — Web search via Kimi platform
FetchURL        — Fetch and extract web content
```

### Your 15 MCP Servers
```
choreographer   — Custom workflow orchestration (Python)
omega           — Security ops, Docker, browser, network tools
filesystem      — File operations scoped to /home/donovan
memory          — Persistent knowledge graph
sqlite          — Query ~/.local/share/mcp-sqlite/database.db
fetch           — HTTP content fetching
puppeteer       — Headless Chrome automation
playwright      — Browser automation (most capable)
chrome-devtools — Chrome DevTools Protocol
sequential-thinking — Chain-of-thought reasoning
github          — GitHub API (PAT configured)
brave-search    — Web search (API key configured)
context7        — Upstash context (⚠️ keys empty)
tavily          — AI search (⚠️ key empty)
exa             — Exa AI search (HTTP)
```

### Your 43 Skills (invoke with `/skill:name`)
```
DEVELOPMENT CORE:
  code-review-refactoring    debugging-root-cause-analysis
  test-driven-development    performance-engineering
  security-engineering       frontend-design
  api-integration            database-design-optimization
  ci-cd-devops               architecture-design
  context-management         observability-monitoring
  multi-agent-orchestration

AI/AGENT DESIGN:
  agent-cognitive-architecture   optimize-prompt
  create-plan                    hostile-auditor
  spec-forge                     mcp-builder

DOCUMENT GENERATION:
  docx    pptx    pdf    xlsx

GITHUB WORKFLOWS:
  gh-address-comments    gh-fix-ci

NOTION INTEGRATION:
  notion-knowledge-capture       notion-meeting-intelligence
  notion-research-documentation  notion-spec-to-implementation

ANDROID:
  android-app    android-app-dev    android-instructor-led-curriculum

WEB/INFRA:
  web-artifacts-builder    webapp-testing    cloudflare-403-triage

UPS-SPECIFIC:
  ups-causal-interventions       ups-decision-intelligence-ui
  ups-evaluation-calibration     ups-kb-authoring
  ups-predict-dashboard          ups-probabilistic-answering
  ups-system-blueprint-mlops

PROJECT MANAGEMENT:
  linear
```

---

## HOW TO USE THIS GUIDE

Each OpenClaw part maps to a Kimi execution block:

```
[ ] TASK DESCRIPTION
    Kimi Skill:  /skill:skill-name
    MCP Server:  server-name (what it provides)
    Kimi Tool:   Shell / ReadFile / WriteFile / etc.
    Command:     The exact kimi prompt or shell command
    Context:     Why this approach, what to watch for
```

Run Kimi from the relevant working directory:
```bash
kimi -w /path/to/workdir           # Start in specific directory
kimi -C                            # Continue previous session
kimi -p "your prompt"              # One-shot prompt
kimi --thinking                    # Enable extended thinking
kimi --yolo                        # Auto-approve all actions (use carefully)
```

## VALIDATION SOURCES (Checked February 22, 2026)

- OpenClaw configuration reference: `https://docs.openclaw.ai/gateway/configuration-reference`
- OpenClaw memory behavior and index pathing: `https://docs.openclaw.ai/concepts/memory`
- OpenClaw CLI `security audit`: `https://docs.openclaw.ai/cli/security`
- OpenClaw CLI gateway lifecycle commands: `https://docs.openclaw.ai/cli/gateway`
- OpenClaw CLI channel login/status commands: `https://docs.openclaw.ai/cli/channels`
- OpenClaw CLI logs (`--limit` usage): `https://docs.openclaw.ai/cli/logs`
- OCI firewall/security-list operations: `https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/Network/Concepts/working-security-lists-and-network-security-groups.htm`
- Hetzner firewall behavior: `https://docs.hetzner.com/cloud/firewalls/getting-started/creating-a-firewall/`

---

# PART 0: PHILOSOPHY & ARCHITECTURE — Understanding the Stack

```
[ ] Read and internalize the OpenClaw architecture (4-layer stack)
    Kimi Skill:  /skill:architecture-design
    Kimi Tool:   ReadFile
    Command:
      kimi -p "Read /home/donovan/.openclaw/building_super_openclaw.md
      lines 1-120. Summarize the 4-layer architecture and golden rules.
      Store key concepts in memory for reference during the build."
    Context: This seeds Kimi's memory MCP with the architecture model
             so all subsequent tasks have context.

[ ] Create a mental model diagram
    Kimi Skill:  /skill:web-artifacts-builder
    Kimi Tool:   WriteFile
    Command:
      kimi -p "Create an HTML file with a Mermaid diagram showing the
      OpenClaw 4-layer architecture: You → Channel Adapters → Gateway →
      AI Brains & Tools. Save to /home/donovan/.openclaw/openclaw-arch.html"
    Context: web-artifacts-builder skill generates standalone HTML with
             embedded diagrams. View in browser for reference.
```

---

# PART 1: CLOUD INFRASTRUCTURE — Server Provisioning

```
[ ] Research and compare cloud providers (Oracle vs Hetzner vs Fly.io)
    Kimi Skill:  /skill:create-plan
    MCP Server:  brave-search (web research)
    Kimi Tool:   SearchWeb, FetchURL
    Command:
      kimi --thinking -p "Research current pricing and availability for:
      1. Oracle Cloud Free Tier ARM (4 OCPU, 24GB) — check capacity status
      2. Hetzner CAX21 ARM ($8.50/mo)
      3. Fly.io performance-2x ($20/mo)
      Compare for running a 24/7 Node.js agent + Ollama.
      Include current Oracle capacity availability reports."
    Context: brave-search MCP provides real-time pricing. Kimi's SearchWeb
             tool queries the Kimi platform's search service. Use both for
             cross-validation.

[ ] Provision the server (Oracle or Hetzner)
    Kimi Skill:  /skill:create-plan
    Kimi Tool:   Shell, FetchURL
    Command (Oracle):
      kimi -p "Walk me through Oracle Cloud instance creation step by step.
      I need: VM.Standard.A1.Flex, 4 OCPU, 24GB RAM, Ubuntu 24.04.
      After each step, wait for my confirmation before proceeding.
      Include the iptables and Security List firewall commands.
      IMPORTANT: when we later switch SSH to 2222, we must add 2222 in
      Oracle Security List first, verify SSH on 2222, then remove 22."

    Command (Hetzner):
      kimi -p "Generate the Hetzner Cloud API call to create a CAX21 ARM
      server with Ubuntu 24.04 and my SSH key. Use the hcloud CLI if
      available, otherwise show the console steps."
    Context: Kimi's Shell tool can run hcloud CLI commands directly if
             installed. For Oracle, it's console-based so Kimi guides you.

[ ] Verify server connectivity
    Kimi Tool:   Shell
    Command:
      kimi -p "SSH into my new server at [IP] on port 22, run
      'uname -a && free -h && df -h' and report the specs."
    Context: Shell tool executes SSH commands. Requires approval per command.
```

---

# PART 2: SERVER HARDENING — Security Baseline

```
[ ] Run the complete hardening sequence
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   Shell
    Command:
      kimi --thinking -p "/skill:security-engineering
      Harden my Ubuntu 24.04 server. Execute these in order, waiting for
      approval on each:
      1. Create non-root user 'openclaw' with sudo
      2. Cloud firewall migration safety:
         - add TCP 2222 from my IP in Oracle Security List/NSG or Hetzner Firewall
         - keep TCP 22 open until SSH on 2222 is verified
      3. SSH hardening: port 2222, key-only, no root login
      4. UFW firewall: deny all incoming, allow 2222/tcp only
      5. Fail2ban on SSH with 3 retries, 1hr ban
      6. Unattended security upgrades
      7. Enable systemd lingering for openclaw user
      8. After verification, remove TCP 22 from cloud firewall rules
      After each step, verify it worked before moving to the next."
    Context: security-engineering skill provides structured security
             hardening workflows. Shell tool requires approval per command
             (good — you want to review each hardening step).

[ ] Install system dependencies (Node.js, Docker, Ollama)
    Kimi Tool:   Shell
    Command:
      kimi -p "Install on my Ubuntu 24.04 ARM server:
      1. Node.js 22+ via nodesource
      2. pnpm globally
      3. Docker + docker-compose-plugin, add openclaw to docker group
      4. Ollama, enable service, pull qwen3:8b and nomic-embed-text
      5. Useful tools: git curl wget htop tmux jq
      Verify each installation with version checks."
    Context: For ARM servers, verify Ollama ARM binary is used (it auto-detects).
             Docker on ARM uses aarch64 images.

[ ] Verify hardening with hostile audit
    Kimi Skill:  /skill:hostile-auditor
    Kimi Tool:   Shell
    Command:
      kimi --thinking -p "/skill:hostile-auditor
      Audit my server hardening:
      - Can root SSH in? Try it.
      - Can password auth work? Try it.
      - Is UFW blocking non-2222 ports? Test with nc.
      - Is cloud firewall updated (2222 open, 22 removed after cutover)?
      - Is fail2ban running? Check status.
      - Is lingering enabled? Verify.
      - Is Docker accessible to openclaw user? Test.
      Produce a PASS/FAIL report with evidence for each check."
    Context: hostile-auditor skill runs adversarial verification — it
             doesn't trust claims, it tests them. Perfect for security.
```

---

# PART 3: OPENCLAW INSTALLATION & SECURITY

```
[ ] Install and verify OpenClaw
    Kimi Tool:   Shell
    Command:
      kimi -p "Run these commands and report results:
      npm install -g openclaw@latest
      openclaw --version
      Verify version is 2026.2.21-2 or newer.
      Then run: openclaw onboard --install-daemon
      Guide me through the wizard choices."
    Context: Shell tool will show each command's output. The onboard wizard
             is interactive — Kimi can guide your choices but you'll need
             to enter them in the actual terminal.

[ ] Run post-install security audit
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   Shell, ReadFile
    Command:
      kimi -p "Run the OpenClaw security audit sequence:
      1. openclaw doctor --deep --repair
      2. openclaw security audit
      3. openclaw gateway status
      4. cat ~/.openclaw/openclaw.json | grep -A3 gateway
      Verify gateway binds to loopback (127.0.0.1), NOT 0.0.0.0.
      Verify exec tool is disabled by default.
      Report any security findings."
    Context: ReadFile can inspect the config directly. Shell runs the
             audit commands. Cross-reference with Part 3's security posture
             documentation.

[ ] Verify sandbox is functional
    Kimi Tool:   Shell
    Command:
      kimi -p "Test OpenClaw sandbox:
      1. docker ps > /dev/null 2>&1 && echo 'Docker OK' || echo 'FAIL'
      2. After enabling sandbox in config, run:
         openclaw agent --message 'Run: cat /etc/hostname'
      3. Verify output shows container hostname (random hex), not server hostname
      Report: sandbox working or broken."
```

---

# PART 4: THE COMPLETE CONFIGURATION

```
[ ] Generate and validate openclaw.json
    Kimi Skill:  /skill:architecture-design
    Kimi Tool:   ReadFile, WriteFile, Shell
    Command:
      kimi --thinking -p "Read the complete configuration template from
      /home/donovan/.openclaw/building_super_openclaw.md Part 4 (the JSON5
      config block). Generate a customized version with:
      - My Anthropic API key from environment
      - Ollama at localhost:11434
      - Gateway on loopback:18789 with token auth
      - Telegram as primary channel
      - Memory search under agents.defaults.memorySearch (NOT top-level memorySearch)
      - Sandbox mode: non-main
      - tools.web.search + tools.web.fetch enabled
      - hooks.defaultSessionKey set
      Validate with JSON5 parser semantics (comments/trailing commas allowed)
      before writing to ~/.openclaw/openclaw.json.
      Show me the diff of what changed."
    Context: WriteFile creates the config. Validate by running
             `openclaw doctor --deep --repair` (schema-aware) instead of `jq`,
             because OpenClaw config is JSON5. Use StrReplaceFile for surgical edits later.

[ ] Validate config with openclaw doctor
    Kimi Tool:   Shell
    Command:
      kimi -p "Run 'openclaw doctor --deep --repair' and report any issues.
      If there are warnings, explain what each means and whether to fix it."
```

---

# PART 5: WORKSPACE FILES — Agent Identity

```
[ ] Create all workspace files (AGENTS.md, SOUL.md, TOOLS.md, HEARTBEAT.md, BOOT.md)
    Kimi Skill:  /skill:spec-forge
    Kimi Tool:   WriteFile, ReadFile
    Command:
      kimi --thinking -p "/skill:spec-forge
      Read Part 5 of /home/donovan/.openclaw/building_super_openclaw.md.
      Create all 5 workspace files in ~/.openclaw/workspace/:
      1. AGENTS.md — personalized with Donovan's context:
         - Location: Houston, TX (America/Chicago)
         - Languages: Python, TypeScript, Rust
         - Active projects: reference ~/Projects/ structure
         - PostgreSQL at localhost:5433, DB: intelligent_storage
      2. SOUL.md — reasoning framework (use template from guide)
      3. TOOLS.md — tool usage policies
      4. HEARTBEAT.md — morning brief, weekly review, health monitoring
      5. BOOT.md — startup verification checks
      Create the skills/ and logs/ subdirectories too.
      Show me each file before writing."
    Context: spec-forge skill specializes in generating specification
             documents. WriteFile creates each file. The personalization
             uses facts from Donovan's system (PostgreSQL on 5433, Projects
             directory structure, timezone).

[ ] Verify workspace structure
    Kimi Tool:   Glob, ReadFile
    Command:
      kimi -p "Show me the complete file tree under ~/.openclaw/workspace/
      and confirm all 5 .md files exist with non-zero content."
```

---

# PART 6: MODEL STRATEGY — Intelligence Routing

```
[ ] Configure model routing matrix
    Kimi Skill:  /skill:optimize-prompt
    Kimi Tool:   ReadFile, StrReplaceFile
    Command:
      kimi --thinking -p "/skill:optimize-prompt
      Read the model routing matrix from Part 6 of building_super_openclaw.md.
      My server is ARM CPU (no GPU), so use the hardware-aware routing table.
      Update ~/.openclaw/openclaw.json to configure:
      - Default: ollama/qwen3:1.7b (fast on ARM)
      - Fallback: anthropic/claude-sonnet-4-6
      - Route model selection by session policy (not legacy channels.modelByChannel)
      - Thinking levels per model as specified
      Use StrReplaceFile for surgical config edits."
    Context: optimize-prompt skill helps tune model selection. On ARM CPU
             without GPU, qwen3:8b is too slow (~2-5 tok/s). Use 1.7b for
             speed or route to cloud for quality.

[ ] Test model routing
    Kimi Tool:   Shell
    Command:
      kimi -p "Test the model routing by sending test messages:
      1. openclaw agent --message 'What time is it?' (should use local model)
      2. openclaw agent --message 'Review this architecture design...' (should use cloud)
      Report which model handled each request."

[ ] Configure 1M context for Opus deep work
    Kimi Tool:   StrReplaceFile
    Command:
      kimi -p "In ~/.openclaw/openclaw.json, ensure the Opus model config
      has context1m: true and thinkingDefault: high. Use StrReplaceFile."
```

---

# PART 7: CHANNEL SETUP — Telegram, Discord, WhatsApp

```
[ ] Set up Telegram bot
    Kimi Skill:  /skill:api-integration
    Kimi Tool:   Shell, FetchURL
    Command:
      kimi -p "/skill:api-integration
      Guide me through Telegram bot setup:
      1. I'll create the bot via @BotFather — tell me what to send
      2. Once I have the token, update ~/.openclaw/openclaw.json channels.telegram
      3. Get my chat ID by fetching https://api.telegram.org/bot<TOKEN>/getUpdates
      4. Restart gateway and test with:
         openclaw message send --channel telegram --target <CHAT_ID> --message 'OpenClaw online 🦞'
      5. Verify with: openclaw channels status"
    Context: FetchURL can hit the Telegram API to get your chat ID.
             api-integration skill handles API setup workflows.

[ ] Set up Discord bot (optional)
    Kimi Skill:  /skill:api-integration
    MCP Server:  github (for bot token management)
    Kimi Tool:   Shell, FetchURL
    Command:
      kimi -p "Guide me through Discord bot creation:
      1. Create application at discord.com/developers
      2. Generate bot token, set permissions (Send/Read Messages, Slash Commands)
      3. Generate OAuth2 invite URL
      4. Update openclaw.json with Discord config
      5. Test connection"
    Context: Discord setup is console-based. Kimi guides the steps.

[ ] Configure WhatsApp (if accepting risks)
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   Shell, ReadFile
    Command:
      kimi --thinking -p "/skill:security-engineering
      I want to set up WhatsApp for OpenClaw. First, show me the risk
      disclosure from Part 7 of building_super_openclaw.md. Then:
      1. Configure with a dedicated number (NOT primary)
      2. Set dmPolicy: pairing, responsesApi: true
      3. Test pairing flow
      4. Set up the daily reconnection check in HEARTBEAT.md
      Emphasize: this uses Baileys (unofficial), ban risk is real."
    Context: security-engineering skill will flag the risks. The WhatsApp
             reconnection heartbeat is critical — sessions expire silently.
```

---

# PART 8: MEMORY SYSTEM — Seeding and Security

```
[ ] Seed the memory system with personal facts
    MCP Server:  memory (persistent knowledge graph)
    Kimi Tool:   Shell
    Command:
      kimi -p "Send these memory-seeding messages to OpenClaw via CLI:
      openclaw agent --message 'Remember: My name is Donovan. Houston TX, America/Chicago.'
      openclaw agent --message 'Remember: Primary languages: Python, TypeScript, Rust.'
      openclaw agent --message 'Remember: PostgreSQL at localhost:5433, DB: intelligent_storage, user: storage_admin'
      openclaw agent --message 'Remember: When I say deploy, I mean push to git main.'
      openclaw agent --message 'Remember: I prefer concise responses. Get to the point.'
      Verify each was stored: openclaw agent --message 'What do you remember about me?'"
    Context: Kimi's own memory MCP server is separate from OpenClaw's memory.
             These commands seed OpenClaw's markdown-backed memory
             (`MEMORY.md` + `memory/YYYY-MM-DD.md`) and are indexed in
             `~/.openclaw/memory/<agentId>.sqlite`.

[ ] Set up memory backup schedule
    Kimi Tool:   Shell
    Command:
      kimi -p "Create a cron job that backs up OpenClaw memory monthly:
      ts=\$(date +%Y%m%d-%H%M%S)
      mkdir -p ~/openclaw-memory-backups/\$ts
      cp -a ~/.openclaw/workspace/memory ~/openclaw-memory-backups/\$ts/ 2>/dev/null || true
      cp ~/.openclaw/workspace/MEMORY.md ~/openclaw-memory-backups/\$ts/ 2>/dev/null || true
      cp ~/.openclaw/memory/main.sqlite ~/openclaw-memory-backups/\$ts/main.sqlite 2>/dev/null || true
      Add this to the monthly maintenance cron."

[ ] Implement memory poisoning defense
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   Shell, ReadFile
    Command:
      kimi --thinking -p "/skill:security-engineering
      Set up memory poisoning defenses for OpenClaw:
      1. Create a monthly memory audit cron job that dumps all entries
      2. Add to HEARTBEAT.md: monthly 'List ALL memory entries verbatim'
      3. Create a backup rotation: keep last 3 monthly snapshots
      4. Document the nuclear recovery procedure in the workspace
      Reference: Schneier Promptware Kill Chain (arxiv 2601.09625v1)"
```


---

# PART 9: AUTONOMY ENGINE — Cron, Heartbeat, Webhooks

```
[ ] Configure all cron jobs
    Kimi Skill:  /skill:ci-cd-devops
    Kimi Tool:   Shell
    Command:
      kimi -p "Set up all OpenClaw cron jobs:
      1. Morning brief (8 AM weekdays):
         openclaw cron add --name morning-brief --cron '0 8 * * 1-5' \
           --message 'Run the morning brief from HEARTBEAT.md' --channel telegram
      2. Weekly review (Sunday 6 PM):
         openclaw cron add --name weekly-review --cron '0 18 * * 0' \
           --message 'Run the weekly summary from HEARTBEAT.md' --channel telegram
      3. Health check (every 30 min, 6AM-11PM):
         openclaw cron add --name health-check --cron '*/30 6-23 * * *' \
           --message 'Check system health. Only message me if something is wrong.' \
           --channel telegram
      4. Verify all: openclaw cron list"
    Context: ci-cd-devops skill handles automation pipeline setup.
             Cron expressions use server timezone — ensure it matches
             America/Chicago.

[ ] Set up webhook triggers for GitHub
    Kimi Skill:  /skill:api-integration
    MCP Server:  github (GitHub API access)
    Kimi Tool:   Shell, WriteFile
    Command:
      kimi -p "/skill:api-integration
      1. Get my webhook token from openclaw.json cron.webhookToken
      2. Create the github-push-handler skill in ~/.openclaw/workspace/skills/
         (use the template from Part 9 of building_super_openclaw.md)
      3. Show me the webhook URL format for my Tailscale IP
      4. Use the github MCP to list my repos and identify which ones
         should have push webhooks"
    Context: github MCP server has your PAT configured. It can list repos,
             create webhooks, and manage PR workflows directly.

[ ] Test the heartbeat system
    Kimi Tool:   Shell
    Command:
      kimi -p "Trigger a manual heartbeat test:
      openclaw agent --message 'Run the morning brief from HEARTBEAT.md now'
      Verify it produces the expected output (system health, tasks, brief format).
      Then check: openclaw cron list — confirm all 3 jobs are active."
```

---

# PART 10: SKILLS — Building Custom Capabilities

```
[ ] Create the PostgreSQL query skill
    Kimi Skill:  /skill:database-design-optimization
    MCP Server:  sqlite (for testing query patterns)
    Kimi Tool:   WriteFile
    Command:
      kimi -p "/skill:database-design-optimization
      Create the postgres-query skill at ~/.openclaw/workspace/skills/postgres-query/SKILL.md
      Customize for my setup:
      - Host: localhost, Port: 5433
      - Database: intelligent_storage
      - User: storage_admin
      - Read-only queries only (SELECT)
      - LIMIT 100 default
      Use the template from Part 10 of building_super_openclaw.md."
    Context: database-design-optimization skill knows SQL patterns and
             safety constraints. Your PostgreSQL is on port 5433 (not default).

[ ] Create the web research skill
    Kimi Skill:  /skill:create-plan
    MCP Server:  brave-search (web search capability)
    Kimi Tool:   WriteFile
    Command:
      kimi -p "Create the web-research skill at
      ~/.openclaw/workspace/skills/web-research/SKILL.md
      Use the template from Part 10. This skill should:
      - Break questions into 3-5 sub-questions
      - Search with multiple sources
      - Synthesize with citations
      - Save to ~/.openclaw/workspace/research/"

[ ] Create the think-first meta-skill
    Kimi Skill:  /skill:agent-cognitive-architecture
    Kimi Tool:   WriteFile
    Command:
      kimi --thinking -p "/skill:agent-cognitive-architecture
      Create the think-first skill at ~/.openclaw/workspace/skills/think-first/SKILL.md
      This is a meta-skill that activates for complex/high-stakes tasks.
      It enforces: plan → present → approve → execute → summarize.
      Use the template from Part 10 of building_super_openclaw.md.
      Cross-reference with the cognitive architecture skill's concepts
      about metacognition and goal arbitration."
    Context: agent-cognitive-architecture skill provides the theoretical
             framework. think-first is the practical implementation of
             metacognitive planning for OpenClaw.

[ ] Build a GitHub PR review skill
    Kimi Skill:  /skill:code-review-refactoring
    MCP Server:  github (PR access)
    Kimi Tool:   WriteFile
    Command:
      kimi -p "/skill:code-review-refactoring
      Create a github-pr-review skill at ~/.openclaw/workspace/skills/github-pr-review/SKILL.md
      It should:
      - Fetch PR diff using GitHub API
      - Review for: bugs, security issues, style violations, test coverage
      - Post review comments directly via GitHub API
      - Summarize findings in Telegram
      Reference the code-review-refactoring skill's methodology."

[ ] Verify all skills load correctly
    Kimi Tool:   Shell, Glob
    Command:
      kimi -p "List all skills in ~/.openclaw/workspace/skills/ and verify
      each has a valid SKILL.md. Then run:
      openclaw skills list --eligible
      Report any skills that fail to load."
```

---

# PART 11: PLUGIN HOOKS — Logging, Routing, Security

```
[ ] Create the interaction-logger plugin
    Kimi Skill:  /skill:database-design-optimization
    Kimi Tool:   WriteFile, Shell
    Command:
      kimi --thinking -p "/skill:database-design-optimization
      Create the interaction-logger plugin at ~/.openclaw/plugins/interaction-logger/index.ts
      Use the template from Part 11 of building_super_openclaw.md.
      Customize:
      - PostgreSQL at localhost:5433
      - Database: intelligent_storage (or create a new 'openclaw_logs' DB)
      - User: storage_admin
      - Updated pricing: Opus $5/$25 per MTok, Sonnet $3/$15 per MTok
      Create the ai_interactions table.
      Register the plugin in openclaw.json.
      Test with a sample interaction."
    Context: Your PostgreSQL is already running on port 5433 with the
             intelligent_storage database from the storage nexus project.
             You can either add the table there or create a separate DB.

[ ] Create the smart-router plugin
    Kimi Skill:  /skill:optimize-prompt
    Kimi Tool:   WriteFile
    Command:
      kimi -p "/skill:optimize-prompt
      Create the smart-router plugin at ~/.openclaw/plugins/smart-router/index.ts
      Use the template from Part 11. This routes:
      - Keywords like 'architecture', 'security audit' → Opus + high thinking
      - Keywords like 'quick', 'remind me', 'schedule' → local model + off
      - Everything else → channel default
      Register in openclaw.json plugins array."

[ ] Implement defense-in-depth security layers
    Kimi Skill:  /skill:security-engineering
    MCP Server:  omega (security operations)
    Kimi Tool:   WriteFile, StrReplaceFile, Shell
    Command:
      kimi --thinking -p "/skill:security-engineering
      Implement the 6-layer defense-in-depth from Part 11:
      Layer 1: Input perimeter — add suspicious pattern detection hook
      Layer 2: Goal-lock — add to SOUL.md
      Layer 3: Per-tool privilege minimization — configure in openclaw.json
               (main: deny exec, monitor: deny exec+browser+write)
      Layer 4: Outbound network allowlists — configure web_fetch urlAllowlist
      Layer 5: Risk-tiered HITL — document in TOOLS.md
      Layer 6: Comprehensive logging — verify interaction-logger captures tool calls
      Use omega MCP for security testing/validation of each layer."
    Context: omega MCP server has red/blue/purple team security capabilities.
             Use it to test whether the security layers actually work.
             security-engineering skill provides the methodology.

[ ] Audit the security implementation
    Kimi Skill:  /skill:hostile-auditor
    MCP Server:  omega (security testing)
    Kimi Tool:   Shell
    Command:
      kimi --thinking -p "/skill:hostile-auditor
      Adversarially test the defense-in-depth implementation:
      1. Try to bypass input perimeter with encoded injection
      2. Verify per-tool restrictions actually block denied tools
      3. Test outbound allowlist by attempting fetch to non-allowed URL
      4. Verify logging captures all tool invocations
      Produce PASS/FAIL evidence for each layer."
```

---

# PART 12: MULTI-AGENT ARCHITECTURE

```
[ ] Configure the agent fleet (main, deep, coder, monitor)
    Kimi Skill:  /skill:multi-agent-orchestration
    Kimi Tool:   ReadFile, StrReplaceFile
    Command:
      kimi --thinking -p "/skill:multi-agent-orchestration
      Read Part 12 of building_super_openclaw.md. Configure the 4-agent fleet
      in ~/.openclaw/openclaw.json:
      - main: ollama/qwen3:1.7b, telegram, deny exec
      - deep: claude-opus-4-6, high thinking, sandbox non-main
      - coder: claude-sonnet-4-6, discord, sandbox on, medium thinking
      - monitor: ollama/qwen3:1.7b, read-only + notify only
      Set routing: telegram→main, discord→coder
      Use StrReplaceFile for surgical config edits."
    Context: multi-agent-orchestration skill handles agent fleet design.
             On ARM CPU, use qwen3:1.7b (not 8b) for local agents.

[ ] Implement trust boundaries between agents
    Kimi Skill:  /skill:agent-cognitive-architecture
    Kimi Tool:   Shell, WriteFile
    Command:
      kimi --thinking -p "/skill:agent-cognitive-architecture
      Implement multi-agent trust boundaries from Part 12:
      1. Create isolated workspaces:
         mkdir -p ~/.openclaw/workspace/{main,coder,monitor}
      2. Set filesystem permissions so agents can't cross-write
      3. Add circuit breaker monitoring to HEARTBEAT.md:
         - Alert if any agent makes >50 tool calls in 5 minutes
         - Alert if any agent accesses files outside its workspace
      4. Configure subagent privilege ceiling: maxSpawnDepth: 2
      5. Verify no cross-agent config modification is possible"

[ ] Test subagent spawning
    Kimi Tool:   Shell
    Command:
      kimi -p "Test OpenClaw subagent spawning:
      openclaw agent --message 'Spawn a research subagent to find the top 3
      open-source Telegram bot frameworks. Report back when done.'
      Verify: subagent spawns, completes, returns results to main agent."
```

---

# PART 13: REMOTE ACCESS — Tailscale

```
[ ] Install and configure Tailscale
    Kimi Tool:   Shell
    Command:
      kimi -p "Install Tailscale on the server:
      curl -fsSL https://tailscale.com/install.sh | sh
      sudo tailscale up
      Show me the auth URL, then after I authenticate:
      tailscale ip -4
      Report the Tailscale IP."

[ ] Update OpenClaw for Tailscale binding
    Kimi Tool:   StrReplaceFile
    Command:
      kimi -p "Update ~/.openclaw/openclaw.json:
      Change gateway.bind from 'loopback' to 'tailnet'
      Add gateway.tailscale.mode: 'serve'
      WARN ME: loopback 127.0.0.1 will stop working after this change.
      All local connections must use the Tailscale IP instead."

[ ] Verify remote access from phone/laptop
    Kimi Tool:   Shell
    Command:
      kimi -p "Test Tailscale connectivity:
      1. From server: tailscale status (show connected devices)
      2. Test gateway access: openclaw gateway health --url ws://<TAILSCALE_IP>:18789 --token <GATEWAY_TOKEN>
      3. Verify web dashboard is accessible
      Report the full access architecture."
```

---

# PART 14: COST CONTROL & MONITORING

```
[ ] Set up the cost dashboard
    Kimi Skill:  /skill:database-design-optimization
    MCP Server:  sqlite (query cost data)
    Kimi Tool:   Shell
    Command:
      kimi -p "/skill:database-design-optimization
      After the interaction-logger plugin is running, create these
      cost monitoring queries and save as a skill:
      1. Weekly cost by model
      2. Daily cost trend
      3. Most expensive sessions
      4. Cost per channel
      Save as ~/.openclaw/workspace/skills/cost-dashboard/SKILL.md"

[ ] Configure cost alerts
    Kimi Tool:   Shell
    Command:
      kimi -p "Create a daily cost alert cron job:
      openclaw cron add --name cost-alert --cron '0 20 * * *' \
        --message 'Query ai_interactions for today total cost.
        If over \$2, alert with breakdown. If under, just log.'
      Verify: openclaw cron list"

[ ] Implement the /compact habit
    Kimi Tool:   Shell, WriteFile
    Command:
      kimi -p "Add to HEARTBEAT.md — Weekly Context Cleanup:
      Every Sunday 11 PM: compact all sessions over 20 turns.
      Create the cron job:
      openclaw cron add --name weekly-compact --cron '0 23 * * 0' \
        --message 'Run /compact on any session over 20 turns.
        Archive summaries to ~/.openclaw/workspace/logs/session-summaries/'"

[ ] Disable unused skills to reduce token overhead
    Kimi Tool:   Shell
    Command:
      kimi -p "Run: openclaw skills list --eligible
      Each enabled skill costs ~24 tokens per request overhead.
      Identify any skills not used in 30 days and disable them.
      Report: how many skills active, estimated token overhead per message."
```

---

# PART 15: MAINTENANCE RUNBOOK

```
[ ] Create the weekly maintenance script
    Kimi Skill:  /skill:ci-cd-devops
    Kimi Tool:   WriteFile, Shell
    Command:
      kimi -p "/skill:ci-cd-devops
      Create a maintenance script at ~/.openclaw/workspace/scripts/weekly-maintenance.sh:
      #!/bin/bash
      npm install -g openclaw@latest
      openclaw --version
      openclaw doctor --deep
      openclaw logs --limit 500 --plain | grep -Ei 'error|warn' | tail -20
      openclaw security audit
      openclaw pairing list
      Make it executable. Add a cron job to run it weekly."

[ ] Create the monthly maintenance script
    Kimi Skill:  /skill:ci-cd-devops
    Kimi Tool:   WriteFile, Shell
    Command:
      kimi -p "Create ~/.openclaw/workspace/scripts/monthly-maintenance.sh:
      Full skill audit, memory review, cost analysis, server updates,
      Ollama model updates, backup of config+workspace+memory index/files,
      kill switch test. Use the Part 15 runbook as template.
      Make executable, add monthly cron."

[ ] Verify openclaw doctor works
    Kimi Tool:   Shell
    Command:
      kimi -p "Run 'openclaw doctor --deep --repair' and explain every
      line of output. Flag anything that needs attention."
```

---

# PART 16: MONEY-MAKING CONFIGURATIONS

```
[ ] Create the client automation skill
    Kimi Skill:  /skill:create-plan
    Kimi Tool:   WriteFile
    Command:
      kimi -p "/skill:create-plan
      Create the client-automation skill from Part 16 at
      ~/.openclaw/workspace/skills/client-automation/SKILL.md
      Include: client workspace creation, workflow documentation,
      ROI assessment template, pricing guide ($500-$8000 tiers)."

[ ] Create the competitive intelligence skill
    Kimi Skill:  /skill:create-plan
    MCP Server:  brave-search (web research)
    Kimi Tool:   WriteFile
    Command:
      kimi -p "Create the competitive-intel skill from Part 16 at
      ~/.openclaw/workspace/skills/competitive-intel/SKILL.md
      Include: daily news monitoring, pricing page tracking,
      Reddit sentiment, hiring signals, weekly digest format.
      Configure weekly cron to run it automatically."

[ ] Set up ACP bridge for editor integration
    Kimi Tool:   Shell
    Command:
      kimi -p "Set up the OpenClaw ACP bridge:
      openclaw acp
      This makes the agent visible in VS Code/Cursor.
      Verify it's running and accessible from the editor.
      Note: Kimi CLI also supports ACP via 'kimi acp' — both can
      coexist for different use cases."
    Context: You already have the Kimi Code VS Code extension (v0.4.1)
             in both Cursor and Antigravity. OpenClaw's ACP adds a second
             agent option in your editor.

[ ] Create the weekly P&L skill
    Kimi Skill:  /skill:database-design-optimization
    Kimi Tool:   WriteFile
    Command:
      kimi -p "Create the weekly-pnl skill from Part 16 at
      ~/.openclaw/workspace/skills/weekly-pnl/SKILL.md
      Query ai_interactions for: API costs, tasks completed, time saved.
      Calculate ROI at my hourly rate. Send Sunday evening via Telegram.
      Add the cron job."
```

---

# PART 17: KILL SWITCH & INCIDENT RESPONSE

```
[ ] Create kill switch aliases
    Kimi Tool:   Shell, WriteFile
    Command:
      kimi -p "Add these aliases to ~/.bashrc AND ~/.zshrc:
      alias claw-status='openclaw gateway status && openclaw channels status'
      alias claw-kill='openclaw gateway stop && echo Gateway stopped && ss -tlnp | grep 18789'
      alias claw-restart='openclaw gateway restart'
      alias claw-lockdown='openclaw gateway stop && sudo ufw deny 18789/tcp && echo LOCKED DOWN'
      Source both files. Test claw-kill and claw-restart."

[ ] Test the kill switch
    Kimi Skill:  /skill:hostile-auditor
    Kimi Tool:   Shell
    Command:
      kimi -p "/skill:hostile-auditor
      Test the kill switch end-to-end:
      1. Run claw-kill — verify gateway stops, port 18789 is closed
      2. Run claw-restart — verify gateway comes back and channels recover
      3. Run claw-lockdown — verify UFW blocks the port
      4. Undo lockdown: sudo ufw delete deny 18789/tcp
      Produce PASS/FAIL evidence for each step."

[ ] Set up monthly kill switch drill
    Kimi Tool:   Shell
    Command:
      kimi -p "Create a monthly cron job for kill switch testing:
      openclaw cron add --name kill-switch-drill --cron '0 10 1 * *' \
        --message 'Time for monthly kill switch drill. Run claw-kill,
        wait 5 seconds, run claw-restart. Report results.'"

[ ] Verify incident response playbook
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   ReadFile
    Command:
      kimi --thinking -p "/skill:security-engineering
      Read the incident response playbook from Part 17 of
      building_super_openclaw.md. Verify it covers:
      1. Isolation (claw-lockdown)
      2. Evidence preservation (logs + memory backup)
      3. Cause identification (log grep + skill audit)
      3b. Memory poisoning check (Promptware Kill Chain)
      4. Threat removal
      5. Safe restoration (doctor --deep --repair)
      Flag any gaps."
```

---

# PART 18: EDGE CASES & OPERATIONAL WISDOM

```
[ ] Implement token debt management
    Kimi Tool:   Shell, StrReplaceFile
    Command:
      kimi -p "Add to HEARTBEAT.md — Weekly Context Cleanup:
      Every Sunday 11 PM: /compact all sessions over 20 turns.
      Archive summaries. Start fresh sessions per channel.
      Create the cron job for this."

[ ] Add hallucination defense to SOUL.md
    Kimi Skill:  /skill:agent-cognitive-architecture
    Kimi Tool:   StrReplaceFile
    Command:
      kimi -p "Append the Hallucination Defense section from Part 18
      to ~/.openclaw/workspace/SOUL.md using StrReplaceFile.
      Include: confidence calibration, 'I think' vs 'it is',
      web_search verification for specific facts."

[ ] Set up WhatsApp reconnection monitoring
    Kimi Tool:   StrReplaceFile
    Command:
      kimi -p "Add to HEARTBEAT.md:
      Daily at 9 PM: Run 'openclaw channels status' and check WhatsApp.
      If disconnected, send Telegram alert with reconnect command.
      Create the cron job."

[ ] Configure memory poisoning recovery procedure
    Kimi Skill:  /skill:security-engineering
    Kimi Tool:   WriteFile
    Command:
      kimi -p "Create ~/.openclaw/workspace/docs/memory-recovery.md
      documenting the safe memory recovery procedure:
      1. Stop gateway
      2. Backup current memory markdown + main.sqlite
      3. Quarantine main.sqlite (do not hard-delete first)
      4. Remove poisoned entries from MEMORY.md and memory/YYYY-MM-DD.md
      5. Restart gateway
      6. Rebuild index: openclaw memory index --force
      7. Re-seed with critical facts from the seed list
      Include the seed list from Part 8."
```

---

# THE FINAL VERIFICATION — Full System Audit

```
[ ] Run the complete hostile audit
    Kimi Skill:  /skill:hostile-auditor
    MCP Server:  omega (security testing)
    Kimi Tool:   Shell, ReadFile
    Command:
      kimi --thinking -p "/skill:hostile-auditor
      Perform a full adversarial audit of the OpenClaw installation:

      INFRASTRUCTURE:
      - Server specs match requirements (4+ GB RAM, ARM/x86)
      - SSH hardened (test: can root login? can password auth?)
      - UFW active (test: are non-SSH ports blocked?)
      - Fail2ban running
      - Lingering enabled
      - Tailscale connected

      OPENCLAW:
      - Version 2026.2.21-2+ verified
      - Gateway binds to loopback/tailnet (NOT 0.0.0.0)
      - Token auth enabled
      - Doctor passes with no critical issues
      - Ollama running with correct models

      CONFIGURATION:
      - All 5 workspace files exist and have content
      - openclaw.json validates (jq parse test)
      - Skills directory has custom skills
      - Plugins registered and loading

      CHANNELS:
      - Telegram connected and responding
      - dmPolicy is 'pairing' on all channels
      - allowFrom configured

      SECURITY:
      - Defense-in-depth layers verified
      - Kill switch works (test it)
      - Memory backup exists
      - Interaction logging active

      Produce a PASS/FAIL report with evidence for EVERY check.
      Save to ~/.openclaw/workspace/logs/system-audit-$(date +%Y%m%d).md"
    Context: This is the capstone verification. hostile-auditor skill
             runs everything, trusts nothing, produces evidence.
             omega MCP adds security testing capabilities.
```

---

# CROSS-REFERENCE: KIMI SKILL → OPENCLAW PART

```
KIMI SKILL                        OPENCLAW PARTS WHERE IT'S USED
─────────────────────────────────────────────────────────────────────
architecture-design               0, 4, 12
security-engineering              2, 3, 7, 8, 11, 17, 18
hostile-auditor                   2, 11, 17, Final Audit
create-plan                       1, 10, 16
api-integration                   7, 9
database-design-optimization      10, 11, 14, 16
optimize-prompt                   6, 11
agent-cognitive-architecture      10, 12, 18
multi-agent-orchestration         12
ci-cd-devops                      9, 15
code-review-refactoring           10
spec-forge                        5
web-artifacts-builder             0
mcp-builder                       (extend with custom MCP servers)

MCP SERVER                        OPENCLAW PARTS WHERE IT'S USED
─────────────────────────────────────────────────────────────────────
brave-search                      1, 10, 16
github                            9, 10
omega                             11, 17, Final Audit
memory                            8 (Kimi's own memory for context)
sqlite                            14
filesystem                        (general file operations)
playwright                        (web dashboard testing)
```

---

# EXECUTION ORDER — OPTIMAL SEQUENCE

For maximum efficiency, execute in this order (dependencies flow downward):

```
Phase 1: Foundation (Parts 1-3)
  Server → Harden → Install OpenClaw
  Skills: security-engineering, hostile-auditor
  Time: ~2 hours

Phase 2: Identity (Parts 4-5)
  Config → Workspace files
  Skills: architecture-design, spec-forge
  Time: ~1 hour

Phase 3: Intelligence (Parts 6-8)
  Model routing → Channels → Memory
  Skills: optimize-prompt, api-integration, security-engineering
  Time: ~1.5 hours

Phase 4: Autonomy (Parts 9-10)
  Cron jobs → Custom skills
  Skills: ci-cd-devops, database-design-optimization, create-plan
  Time: ~1.5 hours

Phase 5: Power (Parts 11-12)
  Plugins → Multi-agent → Trust boundaries
  Skills: security-engineering, multi-agent-orchestration, hostile-auditor
  Time: ~2 hours

Phase 6: Operations (Parts 13-18)
  Tailscale → Cost control → Maintenance → Kill switch → Edge cases
  Skills: ci-cd-devops, database-design-optimization, security-engineering
  Time: ~2 hours

Phase 7: Verification
  Full hostile audit of everything
  Skills: hostile-auditor + omega MCP
  Time: ~30 minutes

TOTAL ESTIMATED TIME: ~10-11 hours (spread across 2-3 sessions)
```

---

*This guide turns your Kimi CLI installation — with its 43 skills, 15 MCP
servers, and full tool suite — into a systematic execution engine for building
the OpenClaw agent described in building_super_openclaw.md. Every task has a
specific skill, tool, and command. No guessing.*
