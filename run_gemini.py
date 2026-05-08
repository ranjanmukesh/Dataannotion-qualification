#!/usr/bin/env python3
import subprocess
import time
import os

# Configuration
SESSION_NAME = "qual_session"
PROJECT_FOLDER = "my-qual-project-start"
LOG_FILE = f"{PROJECT_FOLDER}-log.log"

def run_command(cmd, shell=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=shell, check=False)

print("=== Starting Gemini Qualification Setup ===")

# Kill any existing session
run_command(f"tmux kill-session -t {SESSION_NAME} 2>/dev/null || true")

# Start new tmux session
run_command(f"tmux new-session -d -s {SESSION_NAME}")

# Set environment variables and run commands inside tmux
commands = [
    f"export GEMINI_API_KEY=Q9A4AXWDH3V7K6GWMGWQ7TNW",
    f"export GOOGLE_GEMINI_BASE_URL=https://app.dataannotation.tech/api/llm_proxy/gemini",
    f"export GEMINI_CLI_TRUST_WORKSPACE=true",
    f"export TERM=xterm-256color",
    f"export COLORTERM=truecolor",
    f"cd {PROJECT_FOLDER}",
    "gemini --approval-mode=auto_edit -p 'make the app user friendly'"
]

for cmd in commands:
    run_command(f'tmux send-keys -t {SESSION_NAME} "{cmd}" Enter')
    time.sleep(2)

# Wait for Gemini to load
time.sleep(8)


time.sleep(120)   # Adjust if needed (Gemini can be slow)

# Capture the full conversation
run_command(f'tmux capture-pane -S -10000 -p -t {SESSION_NAME} > {LOG_FILE}')
run_command(f'tmux capture-pane -S - -t {SESSION_NAME} && tmux save-buffer {LOG_FILE}')

