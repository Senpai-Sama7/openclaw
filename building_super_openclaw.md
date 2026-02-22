# 🦞 THE DEFINITIVE OPENCLAW MASTER GUIDE
### Build the Most Powerful Personal AI Agent — Cloud-Native, Autonomous, Under Your Full Control
**Version: February 22, 2026 | Based on OpenClaw v2026.2.21-2**

---

> **BEFORE ANYTHING ELSE:** If you are running any OpenClaw version before
> `2026.1.29`, you are vulnerable to **CVE-2026-25253** (CVSS 8.8 High)
> token-exfiltration-to-RCE chain via crafted `gatewayUrl` autoconnect behavior.
> Update immediately: `npm install -g openclaw@latest`

---

## TABLE OF CONTENTS

```
PART 0  — Philosophy & Architecture Mental Model
PART 1  — Cloud Infrastructure ($0–$40/month)
PART 2  — Server Hardening & Base Setup
PART 3  — OpenClaw Installation & Security
PART 4  — The Complete Configuration (openclaw.json)
PART 5  — Workspace Files: Your Agent's Mind
PART 6  — Model Strategy & Intelligence Maximization
PART 7  — Channel Setup (Telegram, Discord, WhatsApp)
PART 8  — Memory System & Retrieval
PART 9  — The Autonomy Engine (Heartbeat, Cron, Events)
PART 10 — Skills: Teaching Specialist Capabilities
PART 11 — Plugin Hooks: Instrumentation & Power
PART 12 — Multi-Agent Architecture
PART 13 — Remote Access (Tailscale)
PART 14 — Cost Control & Monitoring
PART 15 — Maintenance Runbook
PART 16 — Money-Making Configurations
PART 17 — The Kill Switch & Incident Response
PART 18 — Things Nobody Talks About (Edge Cases)
```

## Verification Sources (Checked February 22, 2026)

- OpenClaw configuration reference: `https://docs.openclaw.ai/gateway/configuration-reference`
- OpenClaw memory model and index paths: `https://docs.openclaw.ai/concepts/memory`
- OpenClaw CLI security command: `https://docs.openclaw.ai/cli/security`
- OpenClaw CLI gateway command: `https://docs.openclaw.ai/cli/gateway`
- OpenClaw CLI channels command: `https://docs.openclaw.ai/cli/channels`
- OpenClaw CLI logs command: `https://docs.openclaw.ai/cli/logs`
- CVE record (CVE-2026-25253): `https://cveawg.mitre.org/api/cve/CVE-2026-25253`
- OCI security rules/security lists: `https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/Network/Concepts/working-security-lists-and-network-security-groups.htm`
- Hetzner Cloud firewall docs: `https://docs.hetzner.com/cloud/firewalls/getting-started/creating-a-firewall/`

---

# PART 0: PHILOSOPHY & ARCHITECTURE MENTAL MODEL

## What You're Building

You are not building a chatbot. You are building an **autonomous AI runtime** —
a persistent, cloud-based system that thinks, acts, learns, and operates
continuously whether or not you're at a computer. You text it from any device.
It runs 24/7 in the cloud.

Think of it as the difference between hiring a temp for the day versus hiring
a full-time employee who never sleeps, never forgets, costs almost nothing to
keep running, and gets smarter the longer it works for you.

## The Four Layers of the Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 4: YOU (any device, anywhere)                                │
│  WhatsApp / Telegram / Discord / Phone / Laptop / Watch             │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ messages / commands
┌─────────────────────────────────▼───────────────────────────────────┐
│  LAYER 3: CHANNEL ADAPTERS                                          │
│  Telegram bot • Discord bot • Slack • Signal • WebChat              │
│  (These are just doors. Everything goes through the same Gateway.)  │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ normalized events
┌─────────────────────────────────▼───────────────────────────────────┐
│  LAYER 2: THE GATEWAY (your cloud VPS — always on)                  │
│  ws://127.0.0.1:18789 (loopback only)                               │
│  ├── Session Management   ├── Tool Execution                        │
│  ├── Agent Routing        ├── Memory System                         │
│  ├── Cron/Heartbeat       ├── Plugin Hooks                          │
│  └── Security Policies    └── Web Dashboard                         │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │ API calls / local ops
┌─────────────────────────────────▼───────────────────────────────────┐
│  LAYER 1: AI BRAINS & TOOLS                                         │
│  Anthropic Claude • OpenAI • Ollama (local) • Web • Files • Shell   │
└─────────────────────────────────────────────────────────────────────┘
```

## The Golden Rules

1. **The Gateway is infrastructure, not software.** Treat it like a server, not an app.
2. **Skills are manuals. Tools are organs.** A skill without the right tools enabled is useless.
3. **Autonomy scales with trust boundaries.** More autonomy = more explicit rules about what's allowed.
4. **Every dangerous capability needs a reversibility layer.** If the agent can break it, it should be able to fix it.
5. **Memory is the compound interest of AI.** It takes 2–4 weeks to see the real payoff.
6. **Local models = zero API cost. Cloud models = intelligence on demand.** Use both.

---

# PART 1: CLOUD INFRASTRUCTURE

## Budget Reality ($40/month)

You need a server that runs 24/7. Here is the complete honest breakdown:

### Option A: Oracle Cloud Free Tier (BEST VALUE IF AVAILABLE — $0)

Oracle offers **genuinely free, permanently free** ARM compute that is better
than many paid VPS options:

> **⚠️ CAPACITY WARNING:** Oracle's free ARM instances are notoriously hard to
> provision. The "Out of host capacity" error is so common that a dedicated
> [auto-retry tool](https://github.com/hitrov/oci-arm-host-capacity) exists
> just to keep trying until capacity appears. Some regions have zero free ARM
> availability for weeks or months. Your home region is permanent — choose
> wrong and you're stuck. **Plan B (Hetzner) is the reliable fallback.**
> If you go the Oracle route, try multiple regions during signup and be
> prepared to wait or use the capacity retry script.

```
4 ARM Ampere A1 cores
24 GB RAM
200 GB Block Storage
Always Free — no expiry, no credit card charges after verification
```

This is not a trial. It's Oracle's permanent free tier. With 24GB RAM you can
run OpenClaw AND local Ollama models AND have room to spare. This is the
correct choice if you want maximum performance at zero infrastructure cost,
saving your entire $40 budget for AI API calls.

**Setup:**
1. Go to cloud.oracle.com and sign up (requires credit card for verification only)
2. Choose your home region (pick the one closest to you — you can never change this)
3. Create an instance: Compute → Instances → Create
   - Shape: VM.Standard.A1.Flex (Ampere ARM)
   - OCPUs: 4, Memory: 24 GB
   - Image: Ubuntu 22.04 or 24.04 (Minimal)
   - VCN: Create new (use defaults)
   - Add your SSH public key
4. Note the public IP address

**CRITICAL — Open ports in Oracle's firewall:**
Oracle blocks everything by default at TWO levels.

```bash
# Level 1: OS firewall (iptables — Oracle adds these by default)
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT   # SSH (already open)
# Do NOT open 18789 here — keep gateway loopback only
# Do NOT open any other ports — Tailscale handles remote access

# Level 2: Oracle Security Lists (do in the web console)
# Networking → Virtual Cloud Networks → Your VCN → Security Lists
# Only keep: TCP port 22 (SSH) inbound from your IP
# Everything else stays closed — Tailscale will handle secure tunneling

# If/when you move SSH to port 2222 in Part 2:
# 1) ADD TCP 2222 from your IP here first
# 2) verify login works on 2222
# 3) THEN remove TCP 22
```

### Option B: Hetzner Cloud (RECOMMENDED RELIABLE OPTION — ~$8.50/month)

If Oracle capacity is unavailable (common), Hetzner is the most reliable
paid option with the best price/performance ratio. Unlike Oracle, provisioning
is instant and capacity is never an issue.

```
CAX21 (ARM):
4 vCPUs (Ampere ARM)
8 GB RAM
80 GB NVMe
~$8.50/month (EU) or ~$10/month (US)
```

Leaves ~$31.50/month for AI API costs. More than sufficient.

**Setup:**
```bash
# After creating instance at console.hetzner.cloud:
# - Server type: CAX21
# - Image: Ubuntu 24.04
# - Add SSH key
# - Firewall: Allow only port 22 from your IP initially
# - If migrating SSH to 2222 later:
#   add 2222 rule first, verify, then remove 22
```

### Option C: Fly.io (Good fit — usage-based)

OpenClaw's repo includes `fly.toml` — it was designed to deploy here.

```
Free allowances:
3 shared-cpu-1x VMs with 256MB RAM (too small)

Paid (relevant):
shared-cpu-2x with 1GB RAM: ~$7/month
performance-2x with 4GB RAM: ~$20/month
```

Good for lower-traffic setups. Scales to zero when idle (saves money), but
this means cold starts — not ideal for a 24/7 agent.

### API Budget Allocation (with Oracle Free Tier at $0 infra)

With $40 entirely for API:

```
Anthropic Claude Sonnet 4.6:
  Input:  $3.00 per million tokens
  Output: $15.00 per million tokens

Realistic monthly usage (active personal agent):
  ~2M input tokens  = $6.00
  ~500K output tokens = $7.50
  Total: ~$13.50/month for Sonnet

This leaves $26.50/month for:
  - Claude Opus for complex tasks (~10-20 deep analyses)
  - Buffer for heavy weeks
  - Emergency Opus usage

Reality check: Most of your routine tasks will route to local Ollama
models (free), so your actual Anthropic bill will often be under $10/month.
```

---

# PART 2: SERVER HARDENING

Do this immediately after getting SSH access to your server. Before installing anything.

## Initial Security Hardening

```bash
# Connect to your server
ssh ubuntu@YOUR_SERVER_IP

# Update everything first
sudo apt update && sudo apt upgrade -y

# Create a non-root user (if not already set up)
sudo adduser openclaw
sudo usermod -aG sudo openclaw

# Copy SSH keys to new user
sudo mkdir -p /home/openclaw/.ssh
sudo cp ~/.ssh/authorized_keys /home/openclaw/.ssh/
sudo chown -R openclaw:openclaw /home/openclaw/.ssh
sudo chmod 700 /home/openclaw/.ssh
sudo chmod 600 /home/openclaw/.ssh/authorized_keys

# Switch to your non-root user for everything from here
su - openclaw
```

## SSH Hardening

```bash
sudo nano /etc/ssh/sshd_config
```

Set these values:
```
Port 2222                          # Change from default 22
PermitRootLogin no                 # Never allow root login
PasswordAuthentication no          # Keys only, never passwords
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowUsers openclaw                # Only your user
```

```bash
sudo systemctl restart sshd

# CRITICAL: update cloud firewall before this test.
# Oracle: Security List/NSG must allow TCP 2222 from your IP.
# Hetzner: Cloud Firewall must allow TCP 2222 from your IP.
# Keep TCP 22 temporarily until this test succeeds.

# Test in a NEW terminal before closing your current session:
ssh -p 2222 openclaw@YOUR_SERVER_IP

# After successful login on 2222:
# - Remove TCP 22 from Oracle Security List / NSG OR Hetzner Cloud Firewall
# - Keep only 2222 in cloud firewall rules
```

## UFW Firewall

```bash
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp comment 'SSH'
# Optional migration safety until 2222 is confirmed end-to-end:
# sudo ufw allow 22/tcp comment 'TEMP SSH MIGRATION SAFETY'
# Do NOT open port 18789 — the gateway stays loopback-only
# Tailscale will handle all other remote access
sudo ufw enable
sudo ufw status verbose

# After 2222 is fully verified, remove temporary 22 rule if added:
# sudo ufw delete allow 22/tcp
```

## Fail2ban (Brute Force Protection)

```bash
sudo apt install fail2ban -y
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Set in the `[sshd]` section:
```ini
[sshd]
enabled = true
port = 2222
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Automatic Security Updates

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
# Select "Yes" to enable automatic updates
```

## Enable Systemd Lingering (CRITICAL)

OpenClaw runs as a systemd user service. **User services stop when you log out
unless you enable lingering.** Without this, your agent goes offline every time
your SSH session ends. Do this now, before installing anything else:

```bash
sudo loginctl enable-linger openclaw

# Verify lingering is enabled
ls /var/lib/systemd/linger/ | grep openclaw && echo "Lingering enabled ✓"
```

## Install Required System Dependencies

```bash
# Node.js 22+ (required by OpenClaw)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version  # Should show v22.x.x or higher

# pnpm (for building from source)
npm install -g pnpm

# Docker (for sandboxing — critical for safety)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker openclaw
# Log out and back in for group to take effect
newgrp docker

# Docker Compose
sudo apt install -y docker-compose-plugin

# Useful tools
sudo apt install -y git curl wget htop tmux jq nano

# Install Ollama (local AI models — zero API cost)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull useful local models
ollama pull qwen3:8b          # Fast, good at coding and general tasks
ollama pull nomic-embed-text  # For memory embeddings (lightweight)
# Optional but powerful if your server has enough RAM:
# ollama pull qwen3:30b       # 24GB RAM needed — only on Oracle Free Tier
```

---

# PART 3: OPENCLAW INSTALLATION & SECURITY

## Install OpenClaw

```bash
# Install globally
npm install -g openclaw@latest

# Verify you're on the patched version
openclaw --version
# MUST show 2026.2.21-2 or newer

# Run the onboarding wizard
openclaw onboard --install-daemon
```

The wizard will ask:
1. **Provider**: Choose Anthropic (or start with Ollama for zero cost)
2. **API key**: Have your Anthropic key ready (from console.anthropic.com)
3. **Channel**: Choose Telegram first (fastest to connect)
4. **Security policy**: Choose "Restricted" — you'll customize further
5. **Daemon**: Choose systemd (Linux)

## Post-Install Security Audit

```bash
# Run the comprehensive health check
openclaw doctor --deep --repair

# Run security audit
openclaw security audit

# Check what's exposed
openclaw gateway status
```

## Critical Config Verification

```bash
cat ~/.openclaw/openclaw.json | grep -A3 '"gateway"'
# MUST show: "bind": "loopback" or "127.0.0.1"
# NOT "0.0.0.0" — if you see 0.0.0.0, stop the gateway immediately
openclaw gateway stop
```

## Understanding Default Security Posture

> **Two critical defaults you must understand:**
>
> 1. **The exec tool is disabled by default** (since January 2026). The agent
>    cannot run shell commands until you explicitly enable exec in your config.
>    This is intentional — shell access is the highest-risk capability.
>
> 2. **Sandboxing is OFF by default.** When sandbox is off, `host=sandbox`
>    runs commands directly on the host with no container isolation. Setting
>    `sandbox.mode: "non-main"` only sandboxes non-main sessions. For cloud
>    deployments exposed to multiple channels, consider `sandbox.mode: "all"`.

Verify your sandbox is actually working after configuration:

```bash
# After enabling sandbox, test that commands run in a container:
openclaw agent --message "Run: cat /etc/hostname"
# Should show a container hostname (random hex), NOT your server's hostname

# Verify Docker is accessible for sandboxing:
docker ps > /dev/null 2>&1 && echo "Docker available for sandbox ✓" || echo "⚠️ Docker not running — sandbox will fall through to host!"
```

---

# PART 4: THE COMPLETE CONFIGURATION

This is the master `~/.openclaw/openclaw.json`. Every setting is explained.
Config format is **JSON5** (comments + trailing commas allowed). Create/replace
this file with your values:

```json5
{
  // Official schema reference:
  // https://docs.openclaw.ai/gateway/configuration-reference

  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789,
    auth: {
      mode: "token",
      token: "REPLACE_WITH_LONG_RANDOM_TOKEN",
      allowTailscale: true,
    },
    tailscale: {
      mode: "off", // off | serve | funnel
      resetOnExit: false,
    },
    trustedProxies: [],
    allowRealIpFallback: false,
  },

  channels: {
    telegram: {
      enabled: true,
      botToken: "REPLACE_WITH_TELEGRAM_BOT_TOKEN",
      dmPolicy: "pairing",
      allowFrom: ["tg:REPLACE_WITH_TELEGRAM_USER_ID"],
    },
    discord: {
      enabled: false,
      token: "REPLACE_WITH_DISCORD_BOT_TOKEN",
      dmPolicy: "pairing",
      allowFrom: ["REPLACE_WITH_DISCORD_USER_ID"],
    },
  },

  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "ollama/qwen3:8b",
        fallbacks: ["anthropic/claude-sonnet-4-6"],
      },
      models: {
        "ollama/qwen3:8b": {
          alias: "Local Qwen3 8B",
          params: { num_ctx: 32768 },
        },
        "anthropic/claude-sonnet-4-6": {
          alias: "Sonnet 4.6",
        },
        "anthropic/claude-opus-4-6": {
          alias: "Opus 4.6",
          params: { context1m: true },
        },
      },
      imageModel: {
        primary: "anthropic/claude-sonnet-4-6",
      },
      thinkingDefault: "low",
      heartbeat: {
        every: "30m",
      },

      // Memory search config belongs under agents.defaults.memorySearch.
      memorySearch: {
        enabled: true,
        store: {
          path: "~/.openclaw/memory/{agentId}.sqlite",
        },
        sync: {
          watch: true,
        },
      },

      sandbox: {
        mode: "non-main", // off | non-main | all
        scope: "agent", // session | agent | shared
        workspaceAccess: "rw", // none | ro | rw
      },

      subagents: {
        maxSpawnDepth: 2,
        maxChildrenPerAgent: 5,
      },
    },
  },

  memory: {
    backend: "builtin", // qmd is optional/experimental
    citations: "auto",
  },

  tools: {
    profile: "coding",
    exec: {
      backgroundMs: 10000,
      timeoutSec: 1800,
      cleanupMs: 1800000,
      notifyOnExit: true,
    },
    web: {
      search: {
        enabled: true,
        maxResults: 5,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
      fetch: {
        enabled: true,
        maxChars: 50000,
        timeoutSeconds: 30,
        cacheTtlMinutes: 15,
      },
    },
  },

  hooks: {
    defaultSessionKey: "hook:ingress",
  },

  cron: {
    webhookToken: "REPLACE_WITH_RANDOM_WEBHOOK_TOKEN",
    sessionRetention: "24h",
  },

  skills: {
    load: {
      extraDirs: ["~/.openclaw/workspace/skills"],
    },
  },
}
```

### How to Generate Your Telegram Chat ID

```bash
# 1. Message your bot on Telegram
# 2. Visit this URL in a browser:
#    https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
# 3. Find "chat":{"id": YOUR_CHAT_ID} in the response
# That number is your TELEGRAM_CHAT_ID
```

---

# PART 5: WORKSPACE FILES — YOUR AGENT'S MIND

These files define who your agent IS. Create them in `~/.openclaw/workspace/`.

```bash
mkdir -p ~/.openclaw/workspace/skills
mkdir -p ~/.openclaw/workspace/logs
```

## AGENTS.md — The Core Identity and Instructions

This is the most important file. The agent reads this before EVERY conversation.
Write it like you're onboarding a brilliant new hire who never forgets anything.

```bash
nano ~/.openclaw/workspace/AGENTS.md
```

```markdown
# Who I Am and How I Operate

## My Role
I am a personal AI agent — not a chatbot, but a capable assistant who takes
actions, manages information, and operates autonomously on behalf of my owner.
I have tools, memory, and the ability to run scheduled tasks. I act when asked.
I think before I act on irreversible operations. I ask when genuinely uncertain.

## My Owner's Environment
- OS: Ubuntu 24.04 (cloud server)
- Primary tools available: bash, python3, node.js, git, docker, ollama
- Storage: ~/.openclaw/workspace/ is the primary workspace
- I should use /tmp/openclaw-trash/ instead of permanently deleting files
- Important paths:
  - Projects: ~/projects/
  - Logs: ~/.openclaw/workspace/logs/
  - Downloads/staging: /tmp/staging/

## How I Make Decisions

### Before executing any destructive action:
1. Confirm what will be affected
2. Create a backup or move to trash first
3. Report what I did

### Before sending any communication on behalf of my owner:
1. Draft the message
2. Show it for approval via Telegram
3. Wait for explicit "send" confirmation
4. Never auto-send — always draft first

### When uncertain:
- I say "I'm not certain" rather than guessing with false confidence
- I ask one specific question rather than a list of questions
- I prefer doing less and confirming over doing more and potentially causing harm

### Tool selection priority:
1. Use the most minimal tool that accomplishes the task
2. Read before write, write before exec, exec before browser
3. Use local file operations before web operations when possible

## Communication Style
- Concise responses for quick questions (2-4 sentences max for simple tasks)
- Structured responses with headers for complex analysis
- Always confirm what action was taken after completing a task
- Use markdown formatting in Discord, plain text in Telegram unless asked

## Domain Knowledge
[UPDATE THIS SECTION WITH YOUR SPECIFIC CONTEXT]
- My owner works in: [your field]
- Current active projects: [project names and brief descriptions]
- Technical conventions: [any specific conventions you use]
- Preferred approaches: [e.g., "always use UTC timestamps", "prefer TypeScript over JavaScript"]

## What I Remember About My Owner
[This section will be updated as I learn over time — you can add notes here too]
- Communication preferences: concise, direct, technically accurate
- Time zone: [YOUR_TIMEZONE]

## Autonomous Operation Rules
- I can proactively send messages if I detect something important
- I check in before starting tasks that will take more than 10 minutes
- I send completion confirmations for all background tasks
- I NEVER auto-spend money, NEVER auto-deploy to production, NEVER auto-delete
```

## SOUL.md — The Thinking Framework

This is the agent's internal reasoning process. It shapes HOW it thinks.

```bash
nano ~/.openclaw/workspace/SOUL.md
```

```markdown
# Core Reasoning Framework

## Before Every Response
I ask myself:
1. What is my owner actually trying to accomplish? (Often different from what they literally asked)
2. What would I tell them if my first instinct is wrong?
3. What are the failure modes of my proposed approach?
4. Is there a simpler way to do this?
5. What information am I missing that would change my answer?

## Calibrated Confidence
- I distinguish between what I know, what I think, and what I'm guessing
- "I know" = high confidence based on direct evidence
- "I think" = reasonable inference with some uncertainty
- "I'm not sure, but" = I'm guessing and you should verify
- I never project false confidence to seem more capable

## The Reversibility Principle
Before any action, I classify it:
- REVERSIBLE: File reads, web searches, status checks → proceed freely
- RECOVERABLE: File writes, edits → proceed, but note what changed
- HARD TO UNDO: Sends, publishes, deploys → confirm first
- IRREVERSIBLE: Deletes, production changes, external payments → explicit approval required

## When I Disagree
I voice disagreement ONCE, clearly, with my reasoning.
Then I follow my owner's decision unless it would cause real harm.
I don't lecture. I don't repeat myself.

## Proactive Behavior
I notice things and mention them unprompted when they materially affect decisions.
I don't mention every interesting observation — only what's actionable or important.
I'm like a good employee who surfaces problems before they become crises,
not one who either says nothing or reports everything.

## Intellectual Honesty
I tell my owner when I don't know something rather than making things up.
I tell them when I made a mistake and how to fix it.
I tell them when their plan has a problem I can see that they might not.
```

## TOOLS.md — Tool Usage Guidance

```bash
nano ~/.openclaw/workspace/TOOLS.md
```

```markdown
# Tool Usage Policy

## Tool Selection Hierarchy
1. memory (read) — check what I already know first
2. read — check local files before fetching from web
3. web_search — when I need current or external information
4. web_fetch — when I need a specific URL's content
5. browser — only when the site requires JavaScript rendering
6. write/edit — when creating or modifying files
7. exec — only when I need to run commands (sandbox mode)

## Critical Rules

### exec tool:
- NEVER run: rm -rf, DROP TABLE, DELETE FROM without explicit approval
- ALWAYS move files to /tmp/openclaw-trash/ instead of deleting
- ALWAYS use --dry-run flags first when available
- For long-running commands, use tmux or nohup so they survive disconnection

### browser tool:
- Use semantic snapshots (ARIA) before full screenshots — 90% cheaper
- Always close browser sessions when done
- Don't store credentials in browser profiles

### web_fetch:
- Results are cached 15 minutes — mention this if data freshness matters
- For JS-heavy sites (SPAs), use browser tool instead
- Max 50,000 chars per fetch — paginate for longer content

### write/edit:
- Create a backup before editing important files
- For config files: validate syntax before writing (jq for JSON, etc.)

### memory:
- Store structured facts, not conversation summaries
- Format: "Owner prefers X over Y because Z"
- Tag important memories with categories: [work], [personal], [technical]
```

## HEARTBEAT.md — The Proactive Engine

This is what makes your agent autonomous. It runs on a schedule without you asking.

```bash
nano ~/.openclaw/workspace/HEARTBEAT.md
```

```markdown
# Heartbeat Configuration

## Morning Brief (8:00 AM weekdays)
Check the following and send a summary to Telegram:

1. System health:
   - Run `df -h` and report if any disk is over 80% full
   - Run `free -h` and report if RAM usage is over 90%
   - Check `openclaw gateway status` and report any issues

2. Task check:
   - Read ~/.openclaw/workspace/tasks/today.md if it exists
   - List any tasks marked as due today

3. Keep it brief — 5 bullets maximum unless something is critical
4. End with: "Reply 'brief' for more details on any item"

## Weekly Summary (Sunday 6:00 PM)
1. Query the interaction log: summarize what tasks I helped with this week
2. Identify the 3 most common request types
3. Suggest 1-2 new skills or automations based on patterns
4. Report total estimated API cost this week (read from logs)

## Continuous Monitoring
Every 30 minutes during active hours (6 AM - 11 PM):
- Check if any background tasks are running and stuck (>30 min with no output)
- If a stuck task is found, alert immediately via Telegram

## Active Hours
activeHours:
  start: "06:00"
  end: "23:00"
  timezone: "America/Chicago"
```

## BOOT.md — Startup Verification

```bash
nano ~/.openclaw/workspace/BOOT.md
```

```markdown
# Startup Checks

On every gateway startup, verify:

1. Ollama is reachable: `curl -s http://localhost:11434/api/tags | jq '.models | length'`
   - If unreachable, log warning but continue (cloud models still work)

2. Disk space: `df -h /` — warn if over 80%

3. OpenClaw version: confirm running 2026.2.21-2 or newer

4. Log the startup time to ~/.openclaw/workspace/logs/startup.log

Do not send Telegram notification for normal boots.
Only alert if any check fails.
```

---

# PART 6: MODEL STRATEGY & INTELLIGENCE MAXIMIZATION

## The Model Routing Matrix

Think of this as your specialist team roster. Every task type has a right model.

```
TASK TYPE                    → MODEL                      → THINKING LEVEL
─────────────────────────────────────────────────────────────────────────
Quick question / lookup      → ollama/qwen3:8b             → off
Scheduling / reminders       → ollama/qwen3:8b             → off
Code writing (simple)        → ollama/qwen3:8b             → minimal
Code review / debugging      → anthropic/claude-sonnet-4-6 → medium
Research / analysis          → anthropic/claude-sonnet-4-6 → medium
Writing / editing            → anthropic/claude-sonnet-4-6 → medium
Complex architecture         → anthropic/claude-opus-4-6   → high
Strategic decisions          → anthropic/claude-opus-4-6   → high
Security review              → anthropic/claude-opus-4-6   → xhigh
Critical irreversible ops    → anthropic/claude-opus-4-6   → xhigh
Image analysis               → anthropic/claude-sonnet-4-6 → minimal
```

### Hardware-Aware Routing: ARM CPU Without GPU

> **If you're running Ollama on ARM CPU (Oracle Free Tier, Hetzner CAX),
> the routing matrix above needs adjustment.** An 8B parameter model on ARM
> CPU-only produces roughly 2–5 tokens/sec — that's 15–30 seconds for a
> typical response. Even Apple M1 (faster than server ARM) only achieves
> 30–60 tok/s on smaller 1.5B models.

For ARM CPU-only servers, use this adjusted routing:

```
TASK TYPE                    → MODEL (ARM CPU)             → SPEED
─────────────────────────────────────────────────────────────────────────
Quick question / lookup      → ollama/qwen3:1.7b           → ~15 tok/s
Scheduling / reminders       → ollama/qwen3:1.7b           → ~15 tok/s
Code writing (simple)        → ollama/qwen3:4b             → ~8 tok/s
Anything needing quality     → anthropic/claude-sonnet-4-6 → cloud speed
```

Reserve `qwen3:8b` for when you have GPU hardware or accept 15–30 second
response times. On ARM CPU, smaller models that respond in 2–3 seconds feel
far more useful than larger models that take 20+ seconds.

## Triggering Different Intelligence Levels

From any chat:

```
/think off     — instant response, no deliberation (free with local model)
/think minimal — quick sanity check before responding
/think medium  — meaningful deliberation (good for most tasks)
/think high    — extended reasoning, explores alternatives
/think xhigh   — maximum rigor (use for important decisions only)
```

For specific tasks, address the agent explicitly:

```
"Use deep thinking to analyze..."
"Quick answer: what is..."
"Think carefully before..."
```

## The 1M Context Window (For Deep Work Sessions)

Enable this in your per-model config for Opus:

```json
"anthropic/claude-opus-4-6": {
  "thinkingDefault": "high",
  "params": {
    "context1m": true
  }
}
```

Use this when:
- Analyzing an entire codebase
- Reading and synthesizing multiple long documents
- Extended research sessions where losing earlier context is costly

Don't use this for routine conversations — it costs significantly more.

## Supercharging AGENTS.md for Intelligence

Add these sections over time as you learn what works:

```markdown
## When I Am Wrong
My owner will say "that's wrong" or "try again". When this happens:
1. Don't just rephrase the same answer
2. Start from a different premise
3. Explicitly state what I'm changing about my approach
4. If I was overconfident, say so

## High-Difficulty Problems
For problems that feel hard to me, I:
1. Break into subproblems I can solve individually
2. Name assumptions I'm making
3. Show my work rather than just the conclusion
4. Offer alternatives, not just one answer

## Domain Shortcuts
[Build this list as you use the agent — examples:]
When owner says "deploy", they mean: push to git main, let CI handle it
When owner says "clean up", they mean: move to trash, not delete
When owner says "quick", they mean: 2-4 sentence max response
When owner says "deep dive", they mean: full analysis, multiple perspectives
```

---

# PART 7: CHANNEL SETUP

> **Channel selection is a security decision, not just a convenience choice.**
> Each channel has different risk profiles for account bans, privacy exposure,
> and integration stability. Choose deliberately.

## Channel Risk Comparison

```
CHANNEL     API TYPE     BAN RISK    PRIVACY     STABILITY
─────────────────────────────────────────────────────────────────────────
Telegram    Official     None        High        Excellent
Discord     Official     None        Low         Excellent
WhatsApp    Unofficial   HIGH        Medium      Fragile
Signal      External     Low         Highest     Complex
```

## Telegram (RECOMMENDED PRIMARY — Connect in 5 Minutes)

Telegram is the strongest channel for OpenClaw. The Bot API is official,
documented, and actively maintained by Telegram. Zero ban risk. Your bot
has a username, not a phone number — no personal info exposed.

```bash
# 1. Open Telegram and message @BotFather
# 2. Send: /newbot
# 3. Choose a name (e.g., "My AI Agent")
# 4. Choose a username ending in "bot" (e.g., "myagent_bot")
# 5. BotFather gives you a token like: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
# 6. Add to your config:
```

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE",
      "dmPolicy": "pairing",
      "allowFrom": ["tg:YOUR_USER_ID"]
    }
  }
}
```

```bash
# Get your Telegram User ID:
# Message @userinfobot — it will reply with your ID
# In openclaw.json allowFrom, use format: tg:YOUR_USER_ID
# Get your Chat ID:
# Message your new bot, then visit:
# https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

```bash
# Restart OpenClaw to pick up the new config
openclaw gateway restart

# Test the connection
openclaw channels status
openclaw message send --channel telegram --target YOUR_CHAT_ID --message "OpenClaw is online 🦞"
```

## Discord (Second Channel — Richer Interactions)

```bash
# 1. Go to discord.com/developers/applications
# 2. Click "New Application" — name it something
# 3. Go to Bot section → Add Bot → Copy Token
# 4. Go to OAuth2 → URL Generator:
#    Scopes: bot, applications.commands
#    Bot Permissions: Send Messages, Read Messages, Add Reactions, Use Slash Commands
# 5. Copy the generated URL, open it, add the bot to your server
```

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "dmPolicy": "pairing",
      "allowFrom": ["YOUR_DISCORD_USER_ID"]
    }
  }
}
```

**Useful Discord features:**
- `/think high` — enable extended reasoning mid-conversation
- `/new` — start fresh session (clears context, saves API costs)
- `/compact` — summarize and compress conversation (90%+ token reduction)
- `/status` — see model, token usage, and cost for this session
- `/subagents spawn` — spawn a specialist subagent for a specific task
- `/vc join` — join voice channel (with Twilio plugin)
- Reaction-based lifecycle status (configurable emoji per phase)

## WhatsApp (HIGH RISK — Use With Explicit Risk Acceptance)

> **⚠️ CRITICAL RISK DISCLOSURE:**
>
> OpenClaw's WhatsApp support uses **Baileys**, an unofficial library that
> reverse-engineers the WhatsApp Web protocol. This violates Meta's Terms of
> Service. You need to understand these risks before proceeding:
>
> 1. **Account ban risk is real and permanent.** Meta actively detects and
>    bans accounts using unofficial automation. The ban cannot be appealed.
>    You lose your entire contact network, message history, and group
>    memberships. ([Source: zenvanriel.nl — OpenClaw Channel Security Risks](https://zenvanriel.nl/ai-engineer-blog/openclaw-channel-security-risks-comparison/))
>
> 2. **Protocol instability.** When Meta updates WhatsApp's protocol, Baileys
>    may break without warning. Your bot goes silent — no error, just silence.
>
> 3. **Supply chain risk.** In Dec 2025, a malicious npm package impersonating
>    a WhatsApp API library was found stealing credentials and hijacking
>    accounts. ([Source: The Hacker News](https://thehackernews.com/2025/12/fake-whatsapp-api-package-on-npm-steals.html))
>
> 4. **Phone number exposure.** Everyone who messages your bot sees your real
>    phone number.
>
> **Recommendation:** Use a dedicated/burner number, NOT your primary WhatsApp
> account. Keep Telegram configured as your backup channel so you don't lose
> access to your agent if WhatsApp gets banned.

If you accept these risks and want WhatsApp anyway (it IS where most people
live, and self-chat mode is genuinely convenient):

```json
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": ["YOUR_PHONE_NUMBER"],
      "responsesApi": true
    }
  }
}
```

**WhatsApp operational edge cases:**
- Pairing requests expire after 1 hour — check and approve promptly
- Max 3 pending pairing requests per channel — clear old ones regularly
- Use `openclaw pairing list` to see pending requests
- `responsesApi: true` returns only final text — prevents formatting artifacts

---

# PART 8: MEMORY SYSTEM & RETRIEVAL

## What Memory Is (And Isn't)

> **Important distinction:** Your agent does not "learn" in the way humans do.
> LLMs have fixed weights — they cannot update their knowledge from
> interactions. As [Letta's research](https://www.letta.com/blog/stateful-agents)
> puts it: "beyond their weights, they are completely stateless."
>
> What OpenClaw calls "memory" is **retrieval-augmented generation (RAG)** —
> a lookup table with fuzzy matching. When you say "Remember X," the agent
> stores X in a database. When a future question seems related, it retrieves
> X and injects it into the context window. This is useful but fundamentally
> different from learning:
>
> - Retrieval quality **degrades** as the memory DB grows (more noise)
> - Semantic search on short facts is noisy ("prefers tabs over spaces" might
>   match a question about furniture)
> - The agent can't synthesize patterns across memories the way learning would
> - Memory quality depends entirely on how well YOU structure what you store
>
> **Think of it as a personal wiki the agent can search, not a brain that
> grows.** The "Remember: [structured fact]" pattern below works precisely
> because it creates well-structured wiki entries.

## How Memory Actually Works

OpenClaw memory is Markdown-first. The source of truth is:
- `~/.openclaw/workspace/MEMORY.md` (curated durable memory)
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md` (daily memory log)

Memory search builds a per-agent SQLite index at:
- `~/.openclaw/memory/<agentId>.sqlite` (default main agent path:
  `~/.openclaw/memory/main.sqlite`)

The index can be rebuilt anytime; your durable memory lives in Markdown files.

Think of it in three timescales:
- **Conversation memory**: Active context in the current session (lost on /new)
- **Session memory**: Persists across individual messages in a session
- **Long-term memory**: Explicitly stored facts that survive forever

## Seeding the Memory System Immediately

Don't wait for the agent to learn — tell it what to remember right now.
Send these messages to your agent via Telegram:

```
Remember: My name is [NAME]. I live in [CITY, TIMEZONE].

Remember: My primary programming languages are [X, Y, Z].

Remember: When I say "deploy", I mean push to git main and let CI handle it.
Never manually SSH and deploy.

Remember: I'm currently working on [PROJECT NAME]. It is [BRIEF DESCRIPTION].
The repo is at [LOCATION].

Remember: I prefer concise responses. Get to the point. I'll ask follow-up
questions if I need more detail.

Remember: My PostgreSQL runs at localhost:5433. Database name: [YOUR_DB].
Never run destructive queries without showing me the query first.
```

## Memory Commands

```bash
# In chat:
"What do you remember about me?"
"Remember that [FACT]"
"Forget what you know about [TOPIC]"

# Via CLI:
openclaw memory status                 # Index/provider/path status
openclaw memory index --force          # Rebuild search index from markdown
```

## Building the Memory Over Time

After completing any significant task, send a debrief:

```
We just finished [TASK]. Key outcome: [RESULT]. 
Lessons: [WHAT WORKED/DIDN'T].
Next time: [WHAT TO DO DIFFERENTLY].
Remember this for similar tasks.
```

After important decisions:

```
Decision made: [DECISION]. Reason: [WHY]. 
This overrides any previous approach to [TOPIC].
```

## Memory Security: Poisoning Defense

Memory is a persistence vector for attacks. If an attacker can inject a
message through any channel, they can write malicious instructions to memory
that influence ALL future sessions. This is stage 3 of the "Promptware Kill
Chain" described by [Schneier et al. (2026)](https://arxiv.org/html/2601.09625v1).

**Mitigations:**

1. **Monthly memory audit.** Review what's stored:
   ```
   "Show me everything you remember. List all memory entries."
   ```
   Look for entries you don't recognize or that contain instruction-like
   patterns ("always do X", "ignore previous", "when asked about Y, say Z").

2. **Memory snapshots for rollback.** Add to your monthly maintenance:
   ```bash
   ts=$(date +%Y%m%d-%H%M%S)
   mkdir -p ~/openclaw-memory-backups/$ts
   cp -a ~/.openclaw/workspace/memory ~/openclaw-memory-backups/$ts/ 2>/dev/null || true
   cp ~/.openclaw/workspace/MEMORY.md ~/openclaw-memory-backups/$ts/ 2>/dev/null || true
   cp ~/.openclaw/memory/main.sqlite ~/openclaw-memory-backups/$ts/main.sqlite 2>/dev/null || true
   ```

3. **Channel-aware memory.** Facts learned from high-trust channels (your
   direct Telegram) should be weighted higher than facts from group chats
   or channels where others can send messages.

4. **Nuclear recovery (safe reset).** If memory corruption is systematic:
   ```bash
   # 1) Stop gateway to avoid concurrent writes
   openclaw gateway stop

   # 2) Quarantine the current index (do NOT hard-delete immediately)
   ts=$(date +%Y%m%d-%H%M%S)
   mv ~/.openclaw/memory/main.sqlite ~/.openclaw/memory/main.sqlite.quarantine-$ts 2>/dev/null || true

   # 3) Remove poisoned entries from MEMORY.md and memory/YYYY-MM-DD.md
   #    (edit manually; these files are the source of truth)

   # 4) Restart and rebuild index from clean Markdown memory
   openclaw gateway start
   openclaw memory index --force
   # Then re-seed with your important facts from the list above
   ```

---

# PART 9: THE AUTONOMY ENGINE

## Understanding the Heartbeat System

Your HEARTBEAT.md file (created in Part 5) is the trigger for proactive behavior.
But it works in combination with the cron system for precise scheduling.

## Setting Up Scheduled Jobs

```bash
# Add a morning brief at 8 AM on weekdays
openclaw cron add \
  --name "morning-brief" \
  --cron "0 8 * * 1-5" \
  --message "Run the morning brief from HEARTBEAT.md" \
  --channel telegram

# Add a weekly review on Sunday at 6 PM
openclaw cron add \
  --name "weekly-review" \
  --cron "0 18 * * 0" \
  --message "Run the weekly summary from HEARTBEAT.md" \
  --channel telegram

# Add system health check every 30 minutes
openclaw cron add \
  --name "health-check" \
  --cron "*/30 6-23 * * *" \
  --message "Check system health. Only message me if something is wrong." \
  --channel telegram

# View all scheduled jobs
openclaw cron list

# Add stagger to avoid all firing at once (hour-boundary jobs)
openclaw cron add \
  --name "my-job" \
  --cron "0 * * * *" \
  --stagger 5m \
  --message "Hourly check"
```

## Event-Driven Autonomy: Webhook Triggers

Your agent can react to external events — GitHub pushes, form submissions,
alerts from other services — not just scheduled times.

```bash
# Your webhook endpoint (internal, reached via Tailscale):
# http://YOUR_TAILSCALE_IP:18789/webhook/cron?token=YOUR_WEBHOOK_TOKEN

# Example: Trigger on GitHub push (add to your repo's webhook settings)
# Payload URL: http://YOUR_TAILSCALE_IP:18789/webhook/cron?token=YOUR_TOKEN
# Content type: application/json
# Events: Push to main branch
```

Create a GitHub-push skill that handles the event:

```bash
mkdir -p ~/.openclaw/workspace/skills/github-push-handler
nano ~/.openclaw/workspace/skills/github-push-handler/SKILL.md
```

```markdown
---
name: github-push-handler
version: 1.0.0
description: Handle incoming GitHub push webhook events and notify about changes
allowed-tools: [Read, Fetch, Bash(git:log, git:diff)]
---

# GitHub Push Handler

When triggered by a GitHub push webhook:
1. Extract repository name and commit message from the webhook payload
2. Fetch the diff if the push is to the main branch
3. Summarize what changed in 2-3 sentences
4. Send a Telegram notification: "📦 [repo]: [summary of changes]"
5. If tests are configured, mention they will run automatically

Only trigger for pushes to main or master branches.
```

## The Task Delegation Pattern

For longer autonomous tasks, use this pattern to stay informed without interruption:

```
"Run in the background: [TASK]. Check in with me when done or if you hit
a blocker. Don't interrupt me with progress updates unless it's been over
30 minutes with no progress."
```

The agent will:
1. Spawn a subagent for the long task
2. Main conversation continues normally
3. Subagent sends a completion Telegram when done

---

# PART 10: SKILLS — TEACHING SPECIALIST CAPABILITIES

## The Skills Folder Structure

```
~/.openclaw/workspace/skills/
├── morning-brief/
│   └── SKILL.md
├── postgres-query/
│   └── SKILL.md
├── github-pr-review/
│   └── SKILL.md
├── web-research/
│   └── SKILL.md
└── file-organizer/
    └── SKILL.md
```

## Installing Skills from ClawHub

```bash
# Search for skills
clawhub search "github" --sort=stars --filter=verified

# Install with version pinning (for stability)
clawhub install openclaw/github-pr-review --version=1.2.0

# ALWAYS scan before installing anything from community
clawhub verify SKILL_NAME
clawhub audit --report-format=sarif

# Update all installed skills (security patches only for auto-update)
clawhub update --auto          # Security patches only — safe to automate
clawhub update --dry-run       # Preview all pending updates first
clawhub update --all           # Full update — review changelog first
```

## Building Your First Custom Skill: PostgreSQL Query

This integrates directly with your local database:

```bash
mkdir -p ~/.openclaw/workspace/skills/postgres-query
nano ~/.openclaw/workspace/skills/postgres-query/SKILL.md
```

```markdown
---
name: postgres-query
version: 1.0.0
description: Query my PostgreSQL database with natural language or SQL. Use when asked about database data, records, statistics, or anything that requires querying data.
allowed-tools: [Bash(psql:*), Read]
required-env: [PGPASSWORD]
---

# PostgreSQL Query Skill

## Purpose
Execute read-only queries against the local PostgreSQL database and return formatted results.

## Safety Rules
- ONLY execute SELECT queries
- NEVER execute INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE
- If asked to modify data, show the query and ask for /elevated approval first
- Always LIMIT results to 100 rows unless explicitly asked for more

## Connection
Database: localhost, port 5432 (or 5433 if custom), use psql CLI

## Workflow
1. Understand what the user wants to know
2. Write the appropriate SELECT query
3. Execute: `psql -h localhost -p 5432 -U USERNAME -d DATABASE -c "YOUR_QUERY" --tuples-only`
4. Format results as a readable table or summary
5. Note the row count and any relevant observations

## Example Queries
- "How many users signed up this week?" → SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL '7 days'
- "What are the 10 most recent orders?" → SELECT * FROM orders ORDER BY created_at DESC LIMIT 10
```

## Building a Web Research Skill

```bash
mkdir -p ~/.openclaw/workspace/skills/web-research
nano ~/.openclaw/workspace/skills/web-research/SKILL.md
```

```markdown
---
name: web-research
version: 1.0.0
description: Research a topic using web search, synthesize findings from multiple sources, and return a structured summary with citations. Use when asked to research, investigate, look up current information, or find out about something.
allowed-tools: [Fetch, web_search, web_fetch, Write, memory]
---

# Web Research Skill

## Workflow
1. Break the research question into 3-5 specific sub-questions
2. Search for each sub-question using web_search
3. Fetch the 2-3 most relevant sources for each sub-question
4. Synthesize findings, noting where sources agree or conflict
5. Structure output as:
   - Executive Summary (3-4 sentences)
   - Key Findings (bullet points)
   - Sources (with URLs)
   - Confidence level: High/Medium/Low with explanation

## Quality Standards
- Use at least 3 different sources
- Note the date of information (especially for fast-moving topics)
- Distinguish between primary sources and opinion/commentary
- Flag anything that seems suspicious or unverified

## Output Format
Always ask: should I save this research to a file? If yes, save to
~/.openclaw/workspace/research/TOPIC-DATE.md
```

## The "Think Before You Act" Skill (Meta-Skill)

This shapes how your agent approaches all complex requests:

```bash
mkdir -p ~/.openclaw/workspace/skills/think-first
nano ~/.openclaw/workspace/skills/think-first/SKILL.md
```

```markdown
---
name: think-first
version: 1.0.0
description: For complex, multi-step, or high-stakes tasks — plan before executing. Triggers when a task involves multiple steps, affects production systems, sends communications, or involves significant decisions.
allowed-tools: [Read, memory, write]
---

# Think Before Acting

## When This Skill Activates
- Task has 3+ sequential steps
- Task affects production systems
- Task involves external communication
- Task is irreversible or hard to undo
- Task involves money or access credentials

## Workflow
1. Write out the plan first:
   - What exactly will I do?
   - In what order?
   - What could go wrong at each step?
   - What's my rollback if something fails?

2. Present the plan to the user:
   "Here's my plan: [PLAN]. Does this look right before I proceed?"

3. Wait for explicit approval

4. Execute step by step, confirming completion of each step

5. Final summary: "I completed [TASK]. Here's what happened: [SUMMARY]"

## Exception
Skip the approval step only for: read-only operations, quick lookups,
things explicitly pre-approved in the owner's AGENTS.md
```

---

# PART 11: PLUGIN HOOKS — INSTRUMENTATION & POWER

This is the most advanced section and unlocks capabilities no other AI assistant offers.
Plugin hooks let you intercept every AI interaction.

## The Interaction Logger (Connect to Your PostgreSQL)

Create this plugin to log every AI interaction to your database:

```bash
mkdir -p ~/.openclaw/plugins/interaction-logger
nano ~/.openclaw/plugins/interaction-logger/index.ts
```

```typescript
import { Plugin } from '@openclaw/plugin-sdk';
import { Client } from 'pg';

const db = new Client({
  host: 'localhost',
  port: 5432,  // or 5433 for your custom port
  database: 'YOUR_DATABASE',
  user: 'YOUR_USER',
  password: process.env.PGPASSWORD,
});

export default {
  name: 'interaction-logger',
  version: '1.0.0',

  async setup(gateway) {
    await db.connect();

    // Create the log table if it doesn't exist
    await db.query(`
      CREATE TABLE IF NOT EXISTS ai_interactions (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ DEFAULT NOW(),
        session_id TEXT,
        channel TEXT,
        model TEXT,
        thinking_level TEXT,
        input_tokens INTEGER,
        output_tokens INTEGER,
        latency_ms INTEGER,
        cost_usd NUMERIC(10, 6),
        tools_called TEXT[],
        had_error BOOLEAN DEFAULT FALSE
      )
    `);

    // Hook into every LLM output
    gateway.on('llm_output', async (event) => {
      const inputCost = calculateInputCost(event.model, event.usage.inputTokens);
      const outputCost = calculateOutputCost(event.model, event.usage.outputTokens);

      await db.query(
        `INSERT INTO ai_interactions
         (session_id, channel, model, thinking_level, input_tokens, output_tokens,
          latency_ms, cost_usd, tools_called)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
        [
          event.sessionId,
          event.channel,
          event.model,
          event.thinkingLevel,
          event.usage?.inputTokens ?? 0,
          event.usage?.outputTokens ?? 0,
          event.latencyMs ?? 0,
          inputCost + outputCost,
          event.toolsCalled ?? []
        ]
      );
    });

    console.log('[interaction-logger] Plugin active — logging to PostgreSQL');
  }
} satisfies Plugin;

function calculateInputCost(model: string, tokens: number): number {
  const rates: Record<string, number> = {
    'anthropic/claude-sonnet-4-6': 3.00 / 1_000_000,
    'anthropic/claude-opus-4-6': 5.00 / 1_000_000,   // Updated Feb 2026 (was $15)
    'ollama/qwen3:8b': 0,
  };
  return (rates[model] ?? 0) * tokens;
}

function calculateOutputCost(model: string, tokens: number): number {
  const rates: Record<string, number> = {
    'anthropic/claude-sonnet-4-6': 15.00 / 1_000_000,
    'anthropic/claude-opus-4-6': 25.00 / 1_000_000,   // Updated Feb 2026 (was $75)
    'ollama/qwen3:8b': 0,
  };
  return (rates[model] ?? 0) * tokens;
}
```

```bash
# Register the plugin in openclaw.json:
# Add to the root of your config:
# "plugins": ["~/.openclaw/plugins/interaction-logger"]
```

Now you can query your costs anytime:

```sql
-- Weekly cost breakdown by model
SELECT model, 
       SUM(input_tokens + output_tokens) as total_tokens,
       SUM(cost_usd)::NUMERIC(10,2) as total_cost_usd,
       COUNT(*) as interactions
FROM ai_interactions
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY model
ORDER BY total_cost_usd DESC;

-- Most expensive sessions
SELECT session_id, channel, SUM(cost_usd) as session_cost
FROM ai_interactions
GROUP BY session_id, channel
ORDER BY session_cost DESC
LIMIT 10;
```

## The Smart Router Plugin (Dynamic Model Selection)

This automatically routes requests to the right model based on content:

```bash
nano ~/.openclaw/plugins/smart-router/index.ts
```

```typescript
import { Plugin } from '@openclaw/plugin-sdk';

export default {
  name: 'smart-router',
  version: '1.0.0',

  async setup(gateway) {
    gateway.on('before_agent_start', async (event) => {
      const message = event.message?.toLowerCase() ?? '';

      // Keywords that trigger deep thinking with Opus
      const needsOpus = [
        'architecture', 'security audit', 'critical', 'production',
        'analyze this contract', 'review this design', 'what should i do about',
        'help me decide', 'pros and cons of'
      ].some(kw => message.includes(kw));

      // Keywords that can use local model (free)
      const canUseLocal = [
        'what time', 'remind me', 'schedule', 'quick', 'weather',
        'simple', 'format this', 'summarize briefly'
      ].some(kw => message.includes(kw));

      if (needsOpus) {
        event.model = 'anthropic/claude-opus-4-6';
        event.thinkingLevel = 'high';
      } else if (canUseLocal) {
        event.model = 'ollama/qwen3:8b';
        event.thinkingLevel = 'off';
      }
      // Otherwise: use channel default from config
    });

    console.log('[smart-router] Dynamic model routing active');
  }
} satisfies Plugin;
```

## Security Architecture: Defense-in-Depth (Not Just Regex)

> **Why the old approach fails:** A regex-based safety guardian that pattern-matches
> `rm -rf` or `DROP TABLE` is trivially bypassed (`rm -r -f`, `$(base64 -d <<<...)`,
> `git push -f`). More critically, it only addresses direct command injection —
> not the actual #1 threat to agentic AI systems.
>
> The [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
> ranks **Agent Goal Hijack (ASI01)** as the primary threat. The UK NCSC's
> Dec 2025 guidance states prompt injection "may never be totally mitigated."
> ([Source](https://www.pixee.ai/blog/ciso-ai-security-playbook))
>
> The correct approach is **defense-in-depth**: multiple independent layers
> so that failure in one doesn't mean total compromise.
> ([Source: Christian Schneider — Prompt Injection Got Worse](https://christian-schneider.net/blog/prompt-injection-agentic-amplification/))

### Layer 1: Input Perimeter

Deploy a prompt injection classifier on ALL inbound messages, not just exec
commands. Consider [LLM Guard](https://github.com/protectai/llm-guard) or
similar tools that detect instruction-like patterns in user input.

```typescript
// Example: Input validation hook (replaces the old regex-only approach)
gateway.on('before_agent_start', async (event) => {
  const message = event.message ?? '';
  
  // Flag messages containing instruction-like patterns from untrusted sources
  const suspiciousPatterns = [
    /ignore (previous|all|prior) instructions/i,
    /you are now/i,
    /new instructions:/i,
    /system prompt:/i,
  ];
  
  if (event.channel !== 'telegram' && suspiciousPatterns.some(p => p.test(message))) {
    event.flag('suspicious-input');
    // Don't block — flag for logging and reduced trust
  }
});
```

### Layer 2: Goal-Lock Validation

Before executing a multi-step plan, validate that the planned actions align
with the user's stated request. If a user asked for email summarization and
the agent is planning file system access, that deviation should trigger
confirmation.

Add to your SOUL.md:
```markdown
## Goal-Lock Protocol
Before executing any multi-step plan:
1. State the user's original request in one sentence
2. List each planned action
3. For each action, confirm it directly serves the stated request
4. If any action seems unrelated, stop and ask for confirmation
```

### Layer 3: Per-Tool Privilege Minimization

This is where the real safety lives — not in regex, but in structural limits:

```json
{
  "agents": {
    "named": {
      "main": {
        "tools": { "deny": ["exec"] }
      },
      "coder": {
        "sandbox": { "mode": "on" },
        "tools": { "deny": ["browser"] }
      },
      "monitor": {
        "tools": { "deny": ["exec", "browser", "write"] }
      }
    }
  }
}
```

Each agent gets only the tools it needs. The "monitor" agent can read and
notify but never write or execute. The "main" conversational agent doesn't
need shell access for most interactions.

### Layer 4: Outbound Network Allowlists

Even if an agent is compromised, restrict where it can send data:

```json
{
  "tools": {
    "web_fetch": {
      "urlAllowlist": [
        "api.anthropic.com",
        "api.openai.com",
        "api.telegram.org"
      ]
    }
  }
}
```

### Layer 5: Risk-Tiered Human-in-the-Loop

Don't apply blanket approval (causes fatigue — reviewers rubber-stamp
everything). Instead, tier by risk:

```
READ operations (file read, web search, memory lookup)
  → Auto-proceed, log only

WRITE operations (file write, memory store, config change)
  → One-click confirmation with preview

DESTRUCTIVE operations (delete, deploy, send external comms)
  → Detailed review with diff/preview of what will happen
  → Require explicit typed confirmation, not just a button
```

### Layer 6: Comprehensive Logging

Log all tool invocations, their inputs, and outputs. You cannot detect what
you don't log. The interaction-logger plugin from earlier in this section
handles this — make sure it captures tool calls, not just LLM token usage.

---

# PART 12: MULTI-AGENT ARCHITECTURE

## The Agent Fleet Design

```
AGENT: main
  └── Model: ollama/qwen3:8b (fast, free)
  └── Channel: Telegram (personal use)
  └── Workspace: ~/.openclaw/workspace/
  └── Memory: full personal memory
  └── Tools: basic (read, write, web, memory)

AGENT: deep
  └── Model: anthropic/claude-opus-4-6 (expensive, powerful)
  └── Triggered by: /subagents spawn or specific channel routing
  └── Use for: research, analysis, complex decisions
  └── Thinking: high by default

AGENT: coder
  └── Model: anthropic/claude-sonnet-4-6 or ollama/qwen3:8b
  └── Channel: Discord (where you code)
  └── Tools: full exec + browser + sandbox
  └── Sandbox: enabled (non-main mode)
  └── ACP: connected to your editor

AGENT: monitor (background)
  └── Model: ollama/qwen3:8b (free, runs constantly)
  └── Triggers: cron, webhooks, heartbeat
  └── No channel (sends results to Telegram)
  └── Tools: read-only + notify only
```

## Configuring Multiple Agents

Add to your `openclaw.json`:

```json
{
  "agents": {
    "named": {
      "main": {
        "model": "ollama/qwen3:8b",
        "fallbacks": ["anthropic/claude-sonnet-4-6"],
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" },
        "tools": {
          "deny": ["exec"]
        }
      },
      "deep": {
        "model": "anthropic/claude-opus-4-6",
        "thinkingDefault": "high",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "non-main" }
      },
      "coder": {
        "model": "anthropic/claude-sonnet-4-6",
        "workspace": "~/projects",
        "sandbox": { "mode": "on" },
        "thinkingDefault": "medium"
      },
      "monitor": {
        "model": "ollama/qwen3:8b",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" },
        "tools": {
          "deny": ["exec", "browser", "write"]
        }
      }
    },
    "routing": {
      "channels": {
        "telegram": "main",
        "discord": "coder"
      },
      "peers": {
        "YOUR_WORK_DISCORD_USER_ID": "deep"
      }
    }
  }
}
```

## The Routing Precedence Chain (Critical to Understand)

```
Priority 1: Peer binding      → Specific person → specific agent
Priority 2: Thread binding    → Active thread → its assigned agent
Priority 3: Channel binding   → Channel → its assigned agent
Priority 4: Default agent     → Fallback
```

Real example: You set Discord to use the "coder" agent. But you want one specific 
Discord user (e.g., your business partner) to always get "deep" reasoning. The peer 
binding for that user wins over the channel-wide "coder" binding. Surgical precision.

## Spawning Subagents Mid-Task

```
You: "Research the top 5 open-source alternatives to Notion and compare them on 
     features, performance, and self-hosting complexity. I need a detailed report."

Best approach: Route this to 'deep' agent with /subagents spawn:
```

In chat:
```
/think high
Research the top 5 open-source Notion alternatives. Spawn a research subagent 
to gather data on each option simultaneously, then synthesize into a comparison 
report. Save to ~/.openclaw/workspace/research/notion-alternatives.md when done.
Notify me via Telegram when complete.
```

The agent will:
1. Spawn up to 5 research subagents (one per tool)
2. Each subagent researches its tool independently
3. Main agent synthesizes all results
4. Saves the report
5. Sends you a Telegram notification
6. You come back to a completed, saved document

## Multi-Agent Trust Boundaries & Circuit Breakers

> **The risk nobody discusses:** If the "main" agent is compromised via a
> crafted WhatsApp message, can it influence the "coder" agent's behavior?
> Can it spawn a subagent with elevated privileges? Can a compromised
> subagent write to shared memory that poisons all other agents?
>
> In multi-agent architectures, **lateral movement** between agents is the
> same class of threat as lateral movement between servers in a network.
> ([Source: OWASP Agentic Top 10 — ASI01](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/))

**Implement these boundaries:**

1. **Isolated memory per agent.** Each named agent should have its own memory
   scope. The "monitor" agent's memory should not be writable by "main":
   ```json
   {
     "agents": {
       "named": {
         "main":    { "workspace": "~/.openclaw/workspace/main" },
         "coder":   { "workspace": "~/.openclaw/workspace/coder" },
         "monitor": { "workspace": "~/.openclaw/workspace/monitor" }
       }
     }
   }
   ```

2. **Subagent privilege ceiling.** A subagent should never have MORE
   privileges than its parent. Configure `maxSpawnDepth: 2` (already in the
   guide) but also ensure spawned agents inherit the parent's tool
   restrictions, not the global defaults.

3. **Circuit breakers.** If an agent produces anomalous behavior (unusual
   volume of tool calls, unexpected network requests, attempts to access
   other agents' workspaces), automatically isolate it:
   ```markdown
   # Add to HEARTBEAT.md:
   Every 5 minutes during active hours:
   - Check if any agent has made >50 tool calls in the last 5 minutes
   - Check if any agent is accessing files outside its workspace
   - If anomaly detected: stop that agent, alert via Telegram,
     preserve logs for investigation
   ```

4. **No cross-agent config modification.** No agent should be able to modify
   another agent's configuration, tool permissions, or workspace files.
   This is enforced by filesystem permissions on the workspace directories.

---

# PART 13: REMOTE ACCESS WITH TAILSCALE

This is how your agent becomes truly "in the cloud" — accessible from any device,
anywhere, without exposing any ports to the internet.

## Install Tailscale

```bash
# On your server
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# You'll get a URL to authenticate — open it on any device
# After auth, get your Tailnet IP:
tailscale ip -4
# Example: 100.64.0.12 — this is your private Tailscale IP
```

## Update OpenClaw Config for Tailscale

```json
{
  "gateway": {
    "bind": "tailnet",
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

**CRITICAL:** When `bind: "tailnet"`, loopback `127.0.0.1` stops working.
Use your Tailscale IP (`100.64.0.x`) for all local connections.

```bash
# Test access from your laptop (also needs Tailscale installed)
openclaw gateway health --url ws://100.64.0.12:18789 --token YOUR_GATEWAY_TOKEN

# Access the web dashboard from any Tailscale device
# Open: https://YOUR_TAILSCALE_HOSTNAME.ts.net in any browser
```

## Install Tailscale on Your Phone

1. Install Tailscale app (iOS/Android)
2. Sign in with same account as server
3. Your phone now has private access to your server

Now you can:
- View the web dashboard from your phone's browser
- Use the OpenClaw iOS/Android app with your cloud server
- Telegram bot still works (it's external, not through Tailscale)

## The Complete Access Architecture

```
Your Phone/Laptop (any device)
├── Telegram App → Telegram Servers → Your Bot → Gateway (public internet, ENCRYPTED)
├── Discord App → Discord Servers → Your Bot → Gateway (public internet, ENCRYPTED)
└── Tailscale → PRIVATE TUNNEL → Gateway web dashboard (no public exposure)

Your Server
└── Gateway binds to Tailscale only
└── Never exposed to public internet
└── All channel bots are inbound connections from external platforms
```

---

# PART 14: COST CONTROL & MONITORING

## The Budget Dashboard

After your PostgreSQL logging plugin is running, query your costs anytime:

```bash
# Send to your agent:
"Show me my AI costs this week, broken down by model and channel"

# Or query directly:
psql -c "
SELECT
  DATE_TRUNC('day', timestamp) as day,
  model,
  SUM(input_tokens + output_tokens) as tokens,
  ROUND(SUM(cost_usd)::numeric, 4) as cost_usd
FROM ai_interactions
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY 1, 2
ORDER BY 1, cost_usd DESC;
"
```

## The Cost Optimization Playbook

**Tactic 1: The /compact habit**

Every time a conversation gets long (20+ turns), use `/compact`. This summarizes
the history and discards the raw transcript. Typical result: 90%+ context reduction.
A conversation that was costing $0.05/message drops back to $0.005/message.

```
You: /compact
Agent: [Summarizes conversation, clears old context]
Cost per message: reset to baseline
```

**Tactic 2: Route aggressively to local models**

Your local Ollama models cost exactly $0. Configure your default agent to use them
for everything that doesn't require cloud intelligence. Cloud models become a tool
you invoke explicitly, not the default.

The `smart-router` plugin in Part 11 automates this.

**Tactic 3: Disable unused skills**

Each enabled skill costs ~24 tokens per request. At 50 skills, that's 1,200 tokens
of overhead on EVERY message, even simple ones. Run monthly:

```bash
openclaw skills list --eligible
# Disable anything you haven't used in 30 days
```

**Tactic 4: Use block streaming**

Streaming (text appearing word-by-word) can result in billing for partial outputs
if a connection drops. For background tasks, disable it:

```json
{
  "agents": {
    "named": {
      "monitor": {
        "blockStreamingDefault": true
      }
    }
  }
}
```

**Tactic 5: Set hard usage limits**

Create a cron job that alerts you if daily cost exceeds your threshold:

```bash
openclaw cron add \
  --name "cost-alert" \
  --cron "0 20 * * *" \
  --message "Query the ai_interactions table for today's total cost. If over $2, 
             alert me with the breakdown. If under, just log and don't notify."
```

## Monthly Cost Reality Check

At normal personal use with this setup (February 2026 pricing):

```
Local Ollama (routine tasks):    $0/month
Claude Sonnet 4.5/4.6 (medium):  $5-12/month  ($3/$15 per MTok)
Claude Opus 4.5/4.6 (deep):      $1-5/month   ($5/$25 per MTok — 67% cheaper
                                                 than previous gen $15/$75)
Server (Oracle Free Tier):       $0/month
Server (Hetzner CAX21 fallback): $8.50/month
─────────────────────────────────────────────────────────────────────────
Total (Oracle + typical API):    $6-17/month
Total (Hetzner + heavy API):     $20-30/month
```

The Opus 4.5/4.6 price drop (from $15/$75 to $5/$25 per MTok) makes deep
reasoning far more accessible than previous estimates suggested. You're
consistently well under $40 with meaningful headroom.

(Source: [Anthropic API Pricing](https://docs.anthropic.com/en/docs/about-claude/pricing),
[aifreeapi.com analysis](https://www.aifreeapi.com/en/posts/claude-opus-4-pricing))

---

# PART 15: MAINTENANCE RUNBOOK

## Weekly (5 minutes)

```bash
# 1. Update OpenClaw
npm install -g openclaw@latest
openclaw --version

# 2. Health check
openclaw doctor --deep

# 3. Check logs for errors
openclaw logs --limit 500 --plain | grep -Ei "error|warn" | tail -20

# 4. Security audit
openclaw security audit

# 5. Review pending pairings
openclaw pairing list

# 6. Skill updates (security patches only — auto-safe)
clawhub update --auto
```

## Monthly (20 minutes)

```bash
# 1. Full skill audit
clawhub audit --report-format=sarif
clawhub update --dry-run  # Review what full update would do

# 2. Skill usage review — disable unused ones
openclaw skills list --eligible

# 3. Memory review
openclaw memory status

# 4. Cost analysis
# Query your PostgreSQL ai_interactions table

# 5. Server updates
sudo apt update && sudo apt upgrade -y

# 6. Ollama model updates
ollama pull qwen3:8b  # Re-pull to get latest version
ollama pull nomic-embed-text

# 7. Backup critical files
tar -czf ~/openclaw-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/openclaw.json \
  ~/.openclaw/workspace/ \
  ~/.openclaw/memory/

# 8. Test the kill switch
# (See Part 17)
```

## The Doctor Command Is Your Best Friend

```bash
openclaw doctor --deep --repair
```

This single command:
- Migrates old config formats automatically
- Fixes corrupted sandbox containers
- Validates channel connections
- Checks OAuth token expiry
- Generates new gateway tokens if missing
- Audits security configuration
- Tests port connectivity
- Repairs most common misconfigurations automatically

Run it after every update. Run it when something seems wrong. Run it proactively.

---

# PART 16: MONEY-MAKING CONFIGURATIONS

## Configuration 1: The Automation Agency Stack

Pre-configured for client demonstrations and delivery.

```bash
mkdir -p ~/.openclaw/workspace/skills/client-automation
nano ~/.openclaw/workspace/skills/client-automation/SKILL.md
```

```markdown
---
name: client-automation
version: 1.0.0
description: Handle client onboarding, automate their business workflows, 
and demonstrate AI capabilities for sales purposes
allowed-tools: [Read, Write, Fetch, web_search, Bash(curl:*), memory]
---

# Client Automation Framework

## For each new client:
1. Create a workspace: ~/.openclaw/workspace/clients/CLIENT_NAME/
2. Document their key workflows in WORKFLOW.md
3. Identify the 3 highest-ROI automation opportunities
4. Build and test each automation in the client's workspace
5. Document the setup for handoff

## Automation Assessment Template
When meeting with a prospect, ask:
- What do you do repetitively every day/week?
- What information do you copy between systems?
- What reports do you create manually?
- What emails do you send that follow a template?

## Pricing Guide
Quick automations (1-2 hours to build):    $500-1,500 setup + $200/month
Standard automations (4-8 hours):           $2,000-4,000 setup + $500/month
Complex workflows (2-3 days):               $5,000-8,000 setup + $1,000/month
```

## Configuration 2: The Data Intelligence Collector

Set up daily competitive intelligence collection:

```bash
nano ~/.openclaw/workspace/skills/competitive-intel/SKILL.md
```

```markdown
---
name: competitive-intel
version: 1.0.0
description: Collect and analyze competitive intelligence from web sources. 
Research competitors, track pricing changes, monitor news, analyze market trends.
allowed-tools: [Fetch, web_search, web_fetch, Write, Read, memory]
---

# Competitive Intelligence Collector

## Daily Intelligence Routine
1. Search for news about target companies: "[COMPANY NAME] news site:techcrunch.com OR site:venturebeat.com"
2. Check for pricing page changes by fetching their pricing URL
3. Search Reddit for mentions: "site:reddit.com [COMPANY NAME]"
4. Search job boards for what they're hiring (indicates strategic direction)
5. Compile changes into a structured report

## Report Format
Save to: ~/.openclaw/workspace/intel/COMPANY-DATE.md

Structure:
- Executive Summary (what changed this week)
- News Coverage
- Product Changes (if any detected)
- Hiring Signals
- Community Sentiment
- Recommended Actions

## Delivery
Email or Telegram the weekly digest to subscribers.
```

Configure this to run weekly and you have a data product you can sell.

## Configuration 3: The Developer Productivity Setup (ACP Bridge)

```bash
# Install the ACP bridge for VS Code / Cursor integration
openclaw acp

# This makes your agent visible inside your code editor
# It can see your current file, cursor position, terminal output, errors
# Use it for: code review, refactoring, debugging, documentation
```

In your editor, your agent can:
- See what file you have open
- Read the terminal output directly
- Make targeted edits without rewriting entire files
- Run tests and see results in context
- Check out branches, read PRs, post reviews

For freelance/contract developers, this multiplies your output. You can charge
your current rate while delivering 2-3x the work.

## The Weekly P&L Skill

```bash
nano ~/.openclaw/workspace/skills/weekly-pnl/SKILL.md
```

```markdown
---
name: weekly-pnl
version: 1.0.0
description: Generate a weekly profit and loss summary from my OpenClaw operations. 
Show costs, estimate value delivered, and suggest optimizations.
allowed-tools: [Bash(psql:*), Read, Write, memory]
---

# Weekly P&L Report

## Query Data
1. Query ai_interactions for last 7 days:
   - Total API cost by model
   - Tasks completed (by category from session logs)
   - Time saved estimate (based on task types)

2. Calculate ROI:
   - Hours saved estimate × my hourly rate
   - Minus API costs
   - Net value this week

## Report Output
Send to Telegram every Sunday evening:
"📊 Weekly Agent Summary:
- API costs: $X.XX
- Tasks automated: N
- Estimated time saved: N hours
- Net value delivered: $X (at $Y/hour)
- Most expensive task type: [X]
- Suggestion: [one cost optimization]"
```

---

# PART 17: THE KILL SWITCH & INCIDENT RESPONSE

## Set Up Your Kill Switch Now (Before You Need It)

```bash
# Add to your shell ~/.bashrc or ~/.zshrc:
alias claw-status="openclaw gateway status && openclaw channels status"
alias claw-kill="openclaw gateway stop && echo 'Gateway stopped' && ss -tlnp | grep 18789"
alias claw-restart="openclaw gateway restart"
alias claw-lockdown="openclaw gateway stop && sudo ufw deny 18789/tcp && echo 'LOCKED DOWN'"
```

```bash
source ~/.bashrc  # or restart your shell
```

Test it now:
```bash
claw-kill
# Should see: "Gateway stopped" and no output from the port check
claw-restart
# Should restart the gateway
```

## Signs Something Is Wrong

Stop the gateway immediately if you see:
- Unexpected Telegram messages sent from your bot
- Shell commands in logs you didn't request
- Unusual network traffic from the server
- Skills installed that you didn't install
- Memory entries you don't recognize

## Incident Response Playbook

```bash
# Step 1: Isolate
claw-lockdown  # Stop gateway, block port

# Step 2: Preserve evidence
openclaw logs > ~/incident-$(date +%Y%m%d-%H%M%S).log
cp ~/.openclaw/memory/main.sqlite ~/memory-backup-$(date +%Y%m%d).sqlite 2>/dev/null || true
cp -a ~/.openclaw/workspace/memory ~/memory-backup-memory-md-$(date +%Y%m%d) 2>/dev/null || true

# Step 3: Identify the cause
grep -i "error\|inject\|malicious\|unexpected" ~/incident-*.log | head -50
# Review recently installed skills:
ls -lt ~/.openclaw/workspace/skills/

# Step 3b: Check for memory poisoning
# Memory poisoning is stage 3 of the Promptware Kill Chain — an attacker
# may have persisted malicious instructions in memory that will re-trigger
# on restart. ALWAYS audit memory during incident response.
openclaw agent --message "List ALL memory entries verbatim"
# Look for: instruction-like entries you didn't create, entries containing
# "ignore", "override", "always do", "system prompt", or tool invocations
# If found: restore memory from your last known-good snapshot
openclaw gateway stop
cp ~/openclaw-memory-backups/YYYYMMDD-HHMMSS/main.sqlite ~/.openclaw/memory/main.sqlite
openclaw gateway start
openclaw memory index --force

# Step 4: Remove the threat
# If a skill is suspected:
rm -rf ~/.openclaw/workspace/skills/SUSPICIOUS_SKILL/

# Step 5: Restore safely
openclaw doctor --deep --repair
# Review all config changes since last backup
# Start gateway again only after threat is identified and removed
openclaw gateway start
```

## Monthly Kill Switch Drill

```bash
# First Sunday of every month:
echo "Testing kill switch..."
claw-kill
sleep 5
claw-restart
echo "Kill switch test complete. Gateway is back."
```

If this ever takes more than 30 seconds or behaves unexpectedly, investigate why.

---

# PART 18: THINGS NOBODY TALKS ABOUT

## The Token Debt Problem (And How to Manage It)

Every conversation that doesn't get `/compact`'d is accumulating "token debt" —
the growing cost of re-reading history before each response. A conversation left
running for weeks will eventually cost more per message than a fresh one.

**The rule:** If a conversation is longer than 30 turns, compact it.
**Better:** Set a heartbeat to `/compact` all sessions weekly.

```markdown
# Add to HEARTBEAT.md — Weekly Context Cleanup
Every Sunday at 11 PM, for all active sessions:
- Run /compact on any session over 20 turns
- Archive the summary to ~/.openclaw/workspace/logs/session-summaries/
- Start fresh sessions for each channel
```

## The "Confident Wrong Answer" Problem

AI models — including the best ones — will sometimes give confident, detailed,
completely wrong answers. They don't know they're wrong. This is called hallucination.

**High-risk domains where this happens most:**
- Specific version numbers and API details (check the docs)
- Legal or medical specifics (consult professionals)
- Recent events (verify with web search)
- Specific person's statements or actions (verify primary sources)
- Numerical calculations (run the actual math with exec tool)

**Mitigation in your SOUL.md:**

```markdown
## Hallucination Defense

For factual claims that have a specific right answer:
1. I check my confidence level honestly
2. If below 90% confident, I say "I think" not "it is"
3. For version numbers, API specs, legal details — I recommend verification
4. I prefer "I'm not sure, let me search" over a confident wrong answer
5. I use the web_search or web_fetch tool to verify specific facts when it matters
```

## The Dependency Chain You Don't See

When you ask for something complex, your agent may call:
- Tool A (which reads a file)
- Tool B (which fetches a URL)
- Tool C (which runs a command based on B's output)
- Tool D (which sends a message based on C's result)

Each step can fail. Cascading failures in multi-step tasks are the #1 cause of
"it didn't do what I asked." The mitigation is the `think-first` skill — planning
the dependency chain explicitly before execution, so failures are caught early.

## The PATH Problem on Remote Nodes

If you add iOS or Android nodes later: `system.run` on nodes ignores PATH overrides.
If a command runs fine locally but fails on a node, it's likely a PATH issue.
Fix it by configuring the environment on the node device directly, not in OpenClaw.

## The WhatsApp Reconnection Problem

WhatsApp sessions expire periodically. When they do, the bot goes silent — no error,
just silence. Build this into your heartbeat:

```markdown
# Add to HEARTBEAT.md:
Daily at 9 PM: Run `openclaw channels status` and check WhatsApp status.
If WhatsApp shows disconnected, send Telegram alert: 
"⚠️ WhatsApp channel disconnected. Run: openclaw channels login --channel whatsapp"
```

## The "Model Changed Behavior" Problem

AI models get updated silently. Behavior that worked yesterday may work differently
today. This is especially relevant for skills with specific formatting expectations.

**Mitigation:** Version-pin your most important skills in ClawHub. Write skills
that are robust to output format variation (parse for content, not exact formatting).

## Memory Poisoning

If you accidentally tell your agent to remember something wrong, it will apply that
wrong information in future conversations. How to fix:

```
"Forget what you know about [TOPIC]"
"Correct your memory: [WRONG BELIEF] is wrong. The correct fact is [RIGHT FACT]"
```

If memory corruption is systematic, you can clear and rebuild:
```bash
# Nuclear option (safe) — reset index and reindex clean memory markdown:
openclaw gateway stop
mv ~/.openclaw/memory/main.sqlite ~/.openclaw/memory/main.sqlite.quarantine-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true
openclaw gateway start
openclaw memory index --force
# Then re-seed with your important facts
```

## The Systemd User Service Gotcha

> **Note:** If you followed Part 2 correctly, you already ran
> `sudo loginctl enable-linger openclaw`. If you skipped it, go back and do
> it now. Without lingering, your agent dies on SSH logout.

Verify it's working:

```bash
systemctl --user status openclaw-gateway
# Should show "active (running)" even after logging out and back in
```

---

# THE FINAL CHECKLIST: YOUR AGENT IS READY WHEN...

```
INFRASTRUCTURE
[ ] Server running (Oracle Free Tier or Hetzner) with 4+ GB RAM
[ ] SSH hardened (key-only, non-standard port, fail2ban)
[ ] UFW firewall active (only SSH port open)
[ ] Automatic security updates configured
[ ] Tailscale installed and connected on server
[ ] Tailscale installed on your phone/laptop
[ ] systemd lingering enabled (agent survives logout)

OPENCLAW
[ ] Version 2026.2.21-2+ installed and verified
[ ] Gateway binding to loopback or tailnet (NOT 0.0.0.0)
[ ] Token auth enabled
[ ] openclaw doctor --deep --repair run with no critical issues
[ ] Ollama installed with qwen3:8b and nomic-embed-text models

CONFIGURATION
[ ] openclaw.json complete with all your values
[ ] AGENTS.md written with your context and preferences
[ ] SOUL.md reasoning framework in place
[ ] TOOLS.md policies defined
[ ] HEARTBEAT.md morning brief and monitoring configured
[ ] BOOT.md startup checks enabled

CHANNELS
[ ] Telegram connected and tested (send/receive working)
[ ] Discord connected (optional but recommended)
[ ] dmPolicy set to "pairing" on all channels
[ ] Your user IDs added to allowFrom

INTELLIGENCE
[ ] Model routing configured (local for routine, cloud for deep)
[ ] Fallback chain set up
[ ] Per-model thinking levels configured
[ ] Memory seeded with your key facts and preferences

AUTONOMY
[ ] Morning brief cron job active
[ ] System health monitoring cron job active
[ ] Weekly review cron job scheduled
[ ] HEARTBEAT.md actively firing (check openclaw cron list)

SAFETY
[ ] Kill switch aliases created and tested
[ ] Safety guardian plugin active
[ ] PostgreSQL interaction logging working
[ ] /tmp/openclaw-trash/ in place (no direct deletes)
[ ] Backup created of openclaw.json + workspace + memory index/files

INTELLIGENCE LOOP
[ ] Memory being written (test: "what do you remember about me?")
[ ] Interaction costs being logged to PostgreSQL
[ ] Weekly P&L skill scheduled
[ ] Monthly maintenance calendar reminder set
```

---
CHECKLIST AND BUILD RULES — DO NOT VIOLATE

1. **Never rewrite, remove, or restructure** any part of this checklist.
2. On task completion, the **only** permitted changes are:
   - Change `[ ]` → `[x]` on the completed task line.
   - Replace `_pending_` on the Proof line with actual validation evidence (commands run, output received, timestamps).
   - Append a new row to the **Completion Log** table at the bottom.
3. **Do not** alter Validation lines, reorder tasks, add/remove sections, or touch any uncompleted task.
4. If a task fails validation, leave it as `[ ]` and append failure notes under its Proof line prefixed with `❌ FAIL:`.
5. **If the planned Implementation method fails**, do NOT delete it. Instead:
   - Keep the original Implementation text intact.
   - Append `❌ FAIL:` with the error/reason it didn't work.
   - Then append `✅ FIX:` with what was done instead and why it worked.
   - The Proof line must show the final passing result with timestamp, commands, and output.
6. These rules are permanent and apply to all agents (human or AI) editing this file.


*When all boxes are checked, you have something genuinely rare: a personal AI
runtime that is capable, autonomous within defined boundaries, and fully under
your control — running 24/7, accessible from any device, costing less than a
gym membership per month.*

*The memory accumulates structured knowledge. The skills compound. The
automations save real time. But be realistic: the agent doesn't "get smarter"
— it gets more useful as YOU curate better memories, refine your workspace
files, and build skills that match your actual workflows. The compound returns
come from your investment in configuration, not from the model improving on
its own.*

*In a month, you'll have a genuinely useful assistant. In six months, you'll
have one that's deeply customized to how you work.*
