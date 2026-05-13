#!/bin/bash
cd /Users/chiaweih/Private/Calendar-fetch

source /Users/chiaweih/Private/Calendar-fetch/.venv/bin/activate

python agent.py > morning-summary.log 2> morning-summary-error.log
