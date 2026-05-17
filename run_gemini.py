#!/usr/bin/env python3
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

# Configuration
SESSION_NAME = "qual_session"
repo_url = Path("url.txt").read_text(encoding="utf-8").strip()
basename = os.path.basename(repo_url)
PROJECT_FOLDER = basename[:-4]+"-start"
LOG_FILE = f"{PROJECT_FOLDER}-log.log"
USER_PROMPT = Path("prompt.txt").read_text(encoding="utf-8").strip()
GEMINI_MD = "GEMINI.md"

def run_command(cmd, shell=True, check=True, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=shell, check=check, cwd=cwd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout)
    if result.stderr.strip():
        print("STDERR:",result.stderr.strip())

def append_to_gemini_md(prompt: str, response: str):
    md_path = Path(GEMINI_MD)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"TURN {timestamp}\n"
    content += f"USER: {prompt}\n"
    content += f"GEMINI: {response.strip()}\n"
    if not md_path.exists():
        header = "Gemini CLI Conversation\n"
        md_path.write_text(header, "utf-8")
        print ("created new gemini md file")
    else:
        print("appending to existing gemini md file")
    with md_path.open("a", encoding = "utf-8") as f:
        f.write(content)

print("=== Starting Gemini Qualification Setup ===")
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set!")

# Kill any existing session
run_command(f"tmux kill-session -t {SESSION_NAME} 2>/dev/null || true")

# Start new tmux session
run_command(f"tmux new-session -d -s {SESSION_NAME}")

# Set environment variables and run commands inside tmux
commands = [
    f"export GEMINI_API_KEY={api_key}",
    f"export GOOGLE_GEMINI_BASE_URL=https://app.dataannotation.tech/api/llm_proxy/gemini",
    f"export GEMINI_CLI_TRUST_WORKSPACE=true",
    f"export TERM=xterm-256color",
    f"export COLORTERM=truecolor",
    f"cd {PROJECT_FOLDER}",
    "export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH",
    "which rg || echo 'rg not found in PATH'",
    "rg --version && echo '✅ ripgrep is working' || echo '❌ ripgrep still missing'",
    "echo '**********************'",
    f"gemini --approval-mode=auto_edit -p '{USER_PROMPT}. Start your response with GEMINI:'"
]

for cmd in commands:
    run_command(f'tmux send-keys -t {SESSION_NAME} "{cmd}" Enter')
    time.sleep(10)

# Wait for Gemini to load
time.sleep(120)   # Adjust if needed (Gemini can be slow)

# Capture the full conversation
run_command(f'tmux capture-pane -S -10000 -p -t {SESSION_NAME} > {LOG_FILE}', check=False)

try:
    log_content = Path(LOG_FILE).read_text(encoding="utf-8", errors="ignore")
    log_content_part = log_content.split("GEMINI:",2)[2].strip()
    lines = log_content_part.splitlines()
    response_lines = []
    for line in lines:
        stripped = line.strip()
        if not any(x in stripped for x in ["Ripgrep","STARTUP", "runner", "-start$"]):
            response_lines.append(stripped)
    if response_lines:
        full_response = "\n".join(response_lines)
    else:
        full_response = ""


    append_to_gemini_md(USER_PROMPT, full_response)
except Exception as e:
    print(f"Error reading log file {e}")
print ("Process completed .......")

