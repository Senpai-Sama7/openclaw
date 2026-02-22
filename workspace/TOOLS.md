# Tool Usage Policy

## Tool Selection Hierarchy
Use tools in this order of preference:

1. **memory (read)** — check what I already know first
2. **read** — check local files before fetching from web
3. **web_search** — when I need current or external information
4. **web_fetch** — when I need a specific URL's content
5. **browser** — only when the site requires JavaScript rendering
6. **write/edit** — when creating or modifying files
7. **exec** — only when I need to run commands (use sandbox when available)

## Critical Rules by Tool

### exec tool (HIGHEST RISK)
- **NEVER** run: rm -rf, DROP TABLE, DELETE FROM without explicit approval
- **ALWAYS** move files to /tmp/openclaw-trash/ instead of deleting
- **ALWAYS** use --dry-run flags first when available
- For long-running commands, use tmux or nohup so they survive disconnection
- Prefer sandbox mode when available (container isolation)

### browser tool
- Use semantic snapshots (ARIA) before full screenshots — 90% cheaper
- Always close browser sessions when done
- Do not store credentials in browser profiles
- Use for JavaScript-heavy sites (SPAs) where web_fetch fails

### web_fetch
- Results are cached 15 minutes — mention this if data freshness matters
- Max 50,000 chars per fetch — paginate for longer content
- Falls back to browser tool for JS-heavy content

### write/edit
- Create a backup before editing important files
- For config files: validate syntax before writing (jq for JSON, etc.)
- Use edit_file for line-based changes when possible
- Prefer atomic writes (write to temp, then move) for critical files

### memory
- Store structured facts, not conversation summaries
- Format: "Owner prefers X over Y because Z"
- Tag important memories with categories: [work], [personal], [technical], [preference]
