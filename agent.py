"""
This script fetches today's calendar events from my personal Google Calendar
Specifically, the ucar calendar that I share with my personal account.

It summarizes the day's events using a local Ollama model, and posts the summary to Slack.

Current cron time is 6:01am every day.
1 6 * * * run.sh
"""

import os
import sys
import traceback
import datetime
from zoneinfo import ZoneInfo
import requests
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# load config variables from config.py
import config

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


# ── Step 1: Authenticate and fetch today's calendar events ────────────────────────

def get_calendar_service():
    """Use the authentifcation to create a google service object to 
    interact with google calendar API.

    This will first check if a valid token.json file exists (from previous auth).
    If not, it will run the OAuth flow to get a new token and save it for next time.

    The credential.json file should be obtained from the Google Cloud Console, with the Calendar API enabled.

    Returns
    -------
    googleapiclient.discovery.Resource
        A Google Calendar API service object that can be used to interact with the API.
    """

    creds = None
    # if token exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # if no token exists or token is invalid
    if not creds or not creds.valid:
        # refresh is expired
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove("token.json")
                raise
        # oauth flow to get new token
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # save the token for next time
        with open("token.json", "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def fetch_todays_events():
    """
    Fetches today's calendar events from the specified Google Calendar.
    It uses the Google Calendar API to retrieve events that start between
    the beginning and end of the current day, based on the configured timezone.

    Returns
    -------
    list
        A list of calendar events for today, where each event is represented as a dictionary containing details
        such as summary, start time, end time, location, and description.
    """
    service = get_calendar_service()
    tz = ZoneInfo(config.TIMEZONE)
    now = datetime.datetime.now(tz)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day   = now.replace(hour=23, minute=59, second=59, microsecond=0)

    # fetch events that start between start_of_day and end_of_day
    events_result = service.events().list(
        calendarId=config.CALENDAR_ID,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])


def format_events_for_prompt(events):
    """
    Formats the list of calendar events into a plain text format suitable for prompting the language model.

    Parameters
    ----------
    events : list
        A list of calendar events, where each event is represented as a dictionary containing details
        such as summary, start time, end time, location, and description.

    Returns
    -------
    str
        A formatted string representing the calendar events, suitable for use in a prompt.
    """
    # if no events, return a simple message
    if not events:
        return "No events scheduled today."
    # otherwise, format each event into a readable line
    lines = []
    for e in events:
        title = e.get("summary", "Untitled")
        start = e["start"].get("dateTime", e["start"].get("date", "All day"))
        end   = e["end"].get("dateTime", e["end"].get("date", ""))
        location = e.get("location", "")
        desc = e.get("description", "")

        # Parse and format the time nicely
        if "T" in start:
            dt = datetime.datetime.fromisoformat(start)
            start_fmt = dt.strftime("%-I:%M %p")
            dt_end = datetime.datetime.fromisoformat(end)
            end_fmt = dt_end.strftime("%-I:%M %p")
            time_str = f"{start_fmt} – {end_fmt}"
        else:
            time_str = "All day"

        line = f"- {time_str}: {title}"
        if location:
            line += f" @ {location}"
        if desc:
            line += f" (Note: {desc[:100]})"
        lines.append(line)

    return "\n".join(lines)



# ── Step 2: Send to local Ollama for summarization ────────────────────────────────

def summarize_with_ollama(events_text):
    """Sends the formatted events text to a local Ollama model to generate a morning briefing.
    The prompt instructs the model to create a friendly and concise summary of the day's events, suitable for posting on Slack.

    Parameters
    ----------
    events_text : str
        A formatted string representing the calendar events, suitable for use in a prompt.

    Returns
    -------
    str
        A short, friendly morning briefing for Slack.
    """
    
    today = datetime.date.today().strftime("%A, %B %-d")
    prompt = f"""You are a helpful personal assistant. Here are today's calendar events for {today}:
        {events_text}

        I want to make the events into the following format and post to slack.

        Say Good morning! 
        Give a short summary
        listed each event in the following bullet point format:
        - all day : Event title @ location (if exists)
        - 9:00 AM - 10:00 AM : Meeting with team @ Conference Room
        - 1:00 PM - 2:00 PM : Lunch with Sarah @ Cafe
        - ... so on
        Give a brief encouraging 
        
        add a short joke at closing line at the end.

        Besides the listed events, keep other message under 200 words, and make it friendly and concise.
    """

    response = requests.post(
        f"{config.OLLAMA_BASE_URL}/api/generate",
        json={
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["response"].strip()


<<<<<<< HEAD
# ── Step 3: Post to Slack ────────────────────────────────────────────────
=======
# ── Step 3: Post to Slack ────────────────────────────────────────────────────
>>>>>>> 89a3386 (gen repo and github page)

def post_to_slack(message, webhook_url=config.SLACK_WEBHOOK_URL_CAESAR):
    """Post the summarized message to slack

    The webhook url is configured in config.py. 
    The message is sent as a simple text payload with json headers.
    and the following format:
    {"text": "Your message here"}

    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' WEBHOOK_URL

    Parameters
    ----------
    message : str
        The message to post to Slack.
    """
    payload = {"text": message}

    # use webhook url to POST message to slack
    response = requests.post(
        webhook_url,
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    print("✓ Posted to Slack")


<<<<<<< HEAD
# ── Main ─────────────────────────────────────────────────────────────────
=======
# ── Main ─────────────────────────────────────────────────────────────────────
>>>>>>> 89a3386 (gen repo and github page)

if __name__ == "__main__":
    print("Fetching calendar events...")
    try:
        events = fetch_todays_events()
    except RefreshError:
        traceback.print_exc(file=sys.stderr)
        msg = (
            ":warning: *Google Calendar OAuth token has expired or been revoked.*\n"
            "Please re-run the OAuth flow manually to renew access:\n"
            "`python agent.py`"
        )
        post_to_slack(msg, webhook_url=config.SLACK_WEBHOOK_URL_UCAR_MINE)
        post_to_slack(msg, webhook_url=config.SLACK_WEBHOOK_URL_CAESAR)
        print("OAuth token expired — Slack warning sent.")
        raise SystemExit(1)

    print(f"Found {len(events)} event(s). Summarizing with Ollama...")
    events_text = format_events_for_prompt(events)
    summary = summarize_with_ollama(events_text)

    print("\n--- Generated summary ---")
    print(summary)
    print("-------------------------\n")

    post_to_slack(summary, webhook_url=config.SLACK_WEBHOOK_URL_UCAR_MINE)
    post_to_slack(summary, webhook_url=config.SLACK_WEBHOOK_URL_CAESAR)
