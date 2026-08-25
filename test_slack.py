import os
import requests

webhook_url = os.environ["SLACK_WEBHOOK_URL"]

message = {
    "text": "🚨 Internship Bot is connected! Slack alerts are working."
}

response = requests.post(webhook_url, json=message)
response.raise_for_status()

print("Slack message sent successfully!")
