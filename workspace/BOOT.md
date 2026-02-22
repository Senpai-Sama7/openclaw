# Startup Verification Checks

On every gateway startup, verify:

## 1. Ollama Availability
Command: curl -s http://localhost:11434/api/tags | jq ".models | length"
- If unreachable, log warning but continue (cloud models still work)
- Expected: 2+ models (qwen3:8b, nomic-embed-text)

## 2. Disk Space
Command: df -h /
- Warn if over 80% full
- Critical alert if over 90% full

## 3. OpenClaw Version
Confirm running 2026.2.21-2 or newer:
Command: openclaw --version

## 4. Gateway Health
Command: openclaw gateway status

## 5. Log Startup
Log the startup time to ~/.openclaw/workspace/logs/startup.log:
Format: [YYYY-MM-DD HH:MM:SS] OpenClaw gateway started (version X)

## Alert Policy
- Do NOT send Telegram notification for normal boots
- Only alert if any check fails or shows warning state
