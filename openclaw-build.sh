#!/usr/bin/env bash
# openclaw-build.sh — Launch 3-pane tmux session for multi-agent build
set -euo pipefail

SESSION="openclaw-build"
DIR="$HOME/.openclaw"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session '$SESSION' already exists. Attaching..."
    exec tmux attach -t "$SESSION"
fi

# Create session with first pane (Codex)
tmux new-session -d -s "$SESSION" -c "$DIR" -n build
tmux send-keys -t "$SESSION" "cd $DIR && git checkout codex/hardening 2>/dev/null || git checkout -b codex/hardening" Enter
tmux send-keys -t "$SESSION" "echo '=== CODEX PANE — branch: codex/hardening ===' && echo 'Parts: 2,3,6,14,17,18 (security/hardening)' && echo 'Run: codex'" Enter

# Split right for Kimi
tmux split-window -h -t "$SESSION" -c "$DIR"
tmux send-keys -t "$SESSION" "cd $DIR && git checkout kimi/skills 2>/dev/null || git checkout -b kimi/skills" Enter
tmux send-keys -t "$SESSION" "echo '=== KIMI PANE — branch: kimi/skills ===' && echo 'Parts: 5,8,9,10,11,12 (skills/hooks/autonomy)' && echo 'Run: kimi'" Enter

# Split bottom-right for Kiro
tmux split-window -v -t "$SESSION" -c "$DIR"
tmux send-keys -t "$SESSION" "cd $DIR && git checkout kiro/infra 2>/dev/null || git checkout -b kiro/infra" Enter
tmux send-keys -t "$SESSION" "echo '=== KIRO PANE — branch: kiro/infra ===' && echo 'Parts: 1,4,7,13,15,16 (infra/config/channels)' && echo 'Run: kiro-cli chat'" Enter

# Select first pane
tmux select-pane -t "$SESSION":0.0

tmux attach -t "$SESSION"
