import json
import os
from pathlib import Path

import requests

from sources import get_internships


SEEN_FILE = Path("seen_jobs.json")


def load_seen_jobs():
    if not SEEN_FILE.exists():
        return set()

    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen_jobs(seen_jobs):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(seen_jobs), f, indent=2)


def get_job_id(job):
    # The feed already gives every internship a unique ID.
    return job["id"]


def get_apply_url(job):
    # Prefer the company's actual application page.
    return job.get("listingUrl") or job.get("url")


def send_slack_alert(job):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    company = job.get("company", "Unknown company")
    title = job.get("title", "Software Engineering Internship")
    location = job.get("location", "Location not listed")
    posted = job.get("posted", "Not listed")
    apply_url = get_apply_url(job)

    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 NEW SUMMER 2027 SWE INTERNSHIP"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*{company} — {title}*\n\n"
                        f"📍 *Location:* {location}\n"
                        f"🗓 *Posted:* {posted}\n"
                        f"🎓 *Class of 2029:* Eligibility check coming next"
                    )
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Apply Now"
                        },
                        "url": apply_url
                    }
                ]
            }
        ]
    }

    response = requests.post(webhook_url, json=message, timeout=30)
    response.raise_for_status()


def main():
    jobs = get_internships()
    seen_jobs = load_seen_jobs()

    print(f"Found {len(jobs)} matching internships.")
    print(f"Already tracking {len(seen_jobs)} internships.")

    current_ids = {get_job_id(job) for job in jobs}

    # FIRST RUN:
    # Don't send 50 alerts for internships that were already open
    # before we created the bot.
    if not seen_jobs:
        print("First run detected.")
        print("Saving current internships without alerting.")

        save_seen_jobs(current_ids)

        print(f"Initialized with {len(current_ids)} internships.")
        return

    new_jobs = [
        job
        for job in jobs
        if get_job_id(job) not in seen_jobs
    ]

    print(f"Found {len(new_jobs)} new internships.")

    for job in new_jobs:
        print(
            f"Sending alert: "
            f"{job.get('company')} — {job.get('title')}"
        )

        send_slack_alert(job)
        seen_jobs.add(get_job_id(job))

    # Also retain every currently-known job ID.
    seen_jobs.update(current_ids)
    save_seen_jobs(seen_jobs)

    print("Done!")


if __name__ == "__main__":
    main()