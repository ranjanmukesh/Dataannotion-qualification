#!/usr/bin/env python3
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

# Configuration
SESSION_NAME = "qual_session"
PROJECT_FOLDER = "my-qual-project-start"
LOG_FILE = f"{PROJECT_FOLDER}-log.log"
USER_PROMPT = "apply the design pattern discussed earlier"
GEMINI_MD = "GEMINI.md"

def run_command(cmd, shell=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=shell, check=False)

def append_to_gemini_md(prompt: str, response: str):
    md_path = Path(PROJECT_FOLDER)/GEMINI_MD
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"turn {timestamp}\n"
    content += f"User: {prompt}\n"
    content += f"Gemini: {response.strip()}"
    if not md_path.exists():
        header = "Gemini CLI Conversation\n"
        md_path.write_text(header, "utf-8")
        print ("created new gemini md file")
    else:
        print("appending to existing gemini md file")

def commit_gemini_md():
    md_path = Path(PROJECT_FOLDER)/GEMINI_MD
    if not md_path.exists():
        print ("gemini md file not found skipping commit")
        return

    try:
        run_command(f"cd {PROJECT_FOLDER} && git add {GEMINI_MD}")
        commit_message = "appending latest conversation"
        result = subprocess.run(f"cd {PROJECT_FOLDER} && git --quiet diff {GEMINI_MD} 2>/dev/null", shell = True) 
        if result.resultcode() == 1:
            run_command(f"cd {PROJECT_FOLDER} && git commit -m {commit_message}")
            run_command(f"cd {PROJECT_FOLDER} && git push")
            print("acommitted successfully")
        else:
            print("nothing to commit")
    except Exception as e:
        print(f"git commit/push failed {e}")
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
    f"gemini --approval-mode=auto_edit -p '{USER_PROMPT}'"
]

for cmd in commands:
    run_command(f'tmux send-keys -t {SESSION_NAME} "{cmd}" Enter')
    time.sleep(2)

# Wait for Gemini to load
time.sleep(8)


time.sleep(240)   # Adjust if needed (Gemini can be slow)

# Capture the full conversation
run_command(f'tmux capture-pane -S -10000 -p -t {SESSION_NAME} > {LOG_FILE}')
run_command(f'tmux capture-pane -S - -t {SESSION_NAME} && tmux save-buffer {LOG_FILE}')

try:
    log_content = Path(LOG_FILE).read_text(encoding="utf-8", errors="ignore")

    if "Gemini" in log_content or ">" in log_content:
        parts = log_split(USER_PROMPT)
        if len(parts) > 1:
            response = parts[-1].strip()
        else:
            response = log_content[-4000:]
    else:
        response = log_content[-3000:]

    append_to_gemini_md(USER_PROMPT, response)
    commit_gemini_md()
except Exception as e:
    print(f"Error reading log file {e}")
print ("Process completed .......")

