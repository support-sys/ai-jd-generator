# JD Generator — Project Context

## What this project does
AI-powered Job Description generator for HR teams.
Input: role details → Output: structured professional JD.

## Stack
Python 3.11, OpenAI API (gpt-4o), Gradio, python-dotenv

## Key files
- app.py — Gradio UI + OpenAI API call (main entry point)
- prompt_builder.py — builds prompts dynamically
- .env — contains OPENAI_API_KEY (never commit)

## Rules
- Never hardcode API keys
- Always use os.environ for secrets
- Prompts live in prompt_builder.py only
- Keep functions small and commented
- My Python is basic — explain non-obvious code

## Run command
python app.py → opens on http://127.0.0.1:7860
