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
    f"cd {PROJECT_FOLDER}",
    "gemini"
]

for cmd in commands:
    run_command(f'tmux send-keys -t {SESSION_NAME} "{cmd}" Enter')
    time.sleep(2)

# Wait for Gemini to load
print("Waiting for Gemini to start...")
time.sleep(8)

# === Send Strong Topic 2 Prompt ===
prompt = '''Explain in detail how a user request flows through the entire application from the moment it arrives until a response is returned. 
Include authentication, validation, database interactions, and error handling. 
Also describe the overall architecture and where business logic is located.'''

run_command(f'tmux send-keys -t {SESSION_NAME} "{prompt}" Enter')

print("Prompt sent. Waiting for response...")
time.sleep(20)   # Adjust if needed (Gemini can be slow)

# Capture the full conversation
run_command(f'tmux capture-pane -S -10000 -p -t {SESSION_NAME} > {LOG_FILE}')
run_command(f'tmux capture-pane -S - -t {SESSION_NAME} && tmux save-buffer {LOG_FILE}')

print(f"\n✅ Done! Log saved to: {LOG_FILE}")
print(f"You can now download: {LOG_FILE} and the tarball from artifacts.")
