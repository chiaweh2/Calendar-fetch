# Calendar Fetch and Slack Summary

This project fetches events from a Google Calendar, summarizes them using a local Ollama model, and posts the summary to a Slack channel. It is designed to run daily as a cron job.

## Features
- Fetches events from a specified Google Calendar.
- Summarizes the day's events using a local AI model.
- Posts the summary to a Slack channel.

## Project Structure
```
Calendar-fetch/
├── agent.py             # Main script to fetch, summarize, and post events
├── config.py            # Configuration file (not in version control — copy from config.example.py)
├── config.example.py    # Example configuration with placeholder values
├── credentials.json     # Google API credentials (not in version control)
├── token.json           # Auto-generated OAuth token (not in version control)
├── run.sh               # Shell script for cron execution
├── docs/                # GitHub Pages site (Privacy Policy & Terms of Service)
├── .gitignore
└── README.md
```

## Prerequisites
- Python 3.12 or higher
- Google API credentials (download `credentials.json` from the Google Cloud Console).
- A Slack webhook URL.
- A local Ollama model (e.g., `llama3`).

## Setup

### 1. Copy and fill in config
```bash
cp config.example.py config.py
# Edit config.py with your Slack webhook URLs, calendar ID, etc.
```

### 2. Google Calendar API
- Go to [console.cloud.google.com](https://console.cloud.google.com)
- Create a new project → Enable "Google Calendar API"
- Go to "Credentials" → Create OAuth 2.0 Client ID → Desktop App
- Download the JSON → save as `credentials.json` in the project root
- First run opens a browser to authorize; afterwards `token.json` is saved automatically

### 3. Slack Incoming Webhook
- Go to [api.slack.com/apps](https://api.slack.com/apps) → Create an app → "Incoming Webhooks" → Activate → Add to a channel
- Copy the webhook URL into `config.py`

### 4. Ollama
- Install from [ollama.com](https://ollama.com) and pull your model:
  ```bash
  ollama pull llama3
  ```

### 5. Install dependencies
```bash
uv sync
source .venv/bin/activate
```

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

## License
MIT License
