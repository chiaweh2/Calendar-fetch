# Copy this file to config.py and fill in your values.

# Slack incoming webhook URLs
SLACK_WEBHOOK_URL_UCAR_MINE = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
SLACK_WEBHOOK_URL_CAESAR    = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Ollama settings — must be running locally
OLLAMA_MODEL    = "llama3"               # or mistral, phi3, gemma2, etc.
OLLAMA_BASE_URL = "http://localhost:11434"

# Google Calendar settings
CALENDAR_ID = "primary"                  # or a specific calendar email
TIMEZONE    = "America/Denver"
