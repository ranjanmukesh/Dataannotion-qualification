# DataAnnotation Qualification - Gemini CLI Automation

A specialized repository for completing the **DataAnnotation "Teaching AI to be More Helpful - Coding Tasks with Agentic Tool Uses"** qualification using **Gemini CLI**.

## 🎯 Purpose

This repository automates the setup, execution, and logging required for the DataAnnotation qualification project. It:

- Clones a target codebase
- Runs Gemini CLI inside a `tmux` session
- Executes custom prompts (Topic 1 or Topic 2)
- Captures full conversation transcripts
- Generates artifacts for easy submission

## 🚀 How It Works

1. **Input Preparation**
   - Put target repo URL in `url.txt`
   - Write your prompt in `prompt.txt`
   - Delete GEMINI.md file for new conversation

All the previous convesation get appended to GEMINI.md file so if you do not want that you need to delete this file.

On push the github actions get triggered and runs the python script which sets up tmux and launches Gemini CLI . All the artifacts needed for this task are available at the completion of github acion pipeline.
	

