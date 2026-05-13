# Calendar Fetch and Slack Summary

A personal automation tool that fetches today's Google Calendar events, summarizes them using a local Ollama model, and posts the morning briefing to Slack. Designed to run daily as a cron job.

## Features

- Fetches events from a specified Google Calendar (read-only)
- Summarizes the day using a local AI model via Ollama (no data leaves your machine)
- Posts the summary to one or more Slack channels
- Sends a Slack alert if the OAuth token expires and needs renewal

## Project Structure

```
Calendar-fetch/
├── agent.py             # Main script: fetch → summarize → post
├── config.py            # Your local config (not in version control)
├── config.example.py    # Template — copy this to config.py
├── credentials.json     # Google OAuth credentials (not in version control)
├── token.json           # Auto-generated OAuth token (not in version control)
├── run.sh               # Shell wrapper for cron
├── docs/                # GitHub Pages (Privacy Policy & Terms of Service)
├── .gitignore
└── README.md
```

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/chiaweh2/Calendar-fetch.git
cd Calendar-fetch
uv sync
source .venv/bin/activate
```

### 2. Configure

```bash
cp config.example.py config.py
# Edit config.py with your values
```

### 3. Google Calendar API

- Go to [console.cloud.google.com](https://console.cloud.google.com)
- Create a project → enable **Google Calendar API**
- Go to **Credentials** → Create **OAuth 2.0 Client ID** → Desktop App
- Download the JSON → save as `credentials.json` in the project root
- First run opens a browser to authorize; `token.json` is saved automatically after that

### 4. Slack Incoming Webhook

- Go to [api.slack.com/apps](https://api.slack.com/apps) → Create app → **Incoming Webhooks** → Activate → Add to channel
- Copy the webhook URL into `config.py`

### 5. Ollama

- Install from [ollama.com](https://ollama.com) and pull a model:
  ```bash
  ollama pull llama3
  ```
- Ollama exposes a local REST API at `http://localhost:11434` — no data leaves your machine

## Usage

Run manually:
```bash
python agent.py
```

Schedule with cron (6:01 AM daily):
```bash
crontab -e
# Add:
1 6 * * * /path/to/Calendar-fetch/run.sh
```

## Pages

- [Privacy Policy](https://chiaweh2.github.io/Calendar-fetch/privacy-policy.html)
- [Terms of Service](https://chiaweh2.github.io/Calendar-fetch/terms-of-service.html)

## Acknowledgments

- [Google Calendar API](https://developers.google.com/calendar)
- [Slack Webhooks](https://api.slack.com/messaging/webhooks)
- [Ollama](https://ollama.ai/)

## License

MIT License
