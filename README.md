# SWE Internship Bot

A Slack bot that watches for new Summer 2027 software engineering internships and alerts you the moment one worth applying to shows up — instead of manually refreshing internship trackers.

## How it works

Every 15 minutes, a scheduled GitHub Action:

1. **Pulls listings** from two public internship-tracking feeds (ApplyGuy and SimplifyJobs), filters to Summer 2027 software-related roles, and deduplicates jobs that appear in both.
2. **Classifies class-year eligibility** — parses each posting's description/requirements for graduation-year ranges and eligibility language, so it can flag whether a Class of 2029 sophomore is actually eligible, versus a listing restricted to juniors/seniors/grad students.
3. **Scores and prioritizes** each new listing (0–10) based on company tier, role relevance (SWE vs. AI/ML vs. general), eligibility confidence, whether it's a sophomore/early-career program, and a personal company watchlist — producing an urgency label from "📌 Lower priority" to "🔥🔥 Apply today."
4. **Posts to Slack** with company, title, location, eligibility reasoning, priority score, and an "Apply Now" button linking straight to the listing.
5. **Tracks what's already been seen** in `seen_jobs.json`, committed back to the repo each run, so the same listing never triggers two alerts.

## Structure

- `main.py` — orchestrates a run: loads seen-job state, fetches and classifies new listings, sends Slack alerts, persists updated state
- `sources.py` — fetches, normalizes, and deduplicates listings from the two source feeds
- `filters.py` — classifies Class of 2029 eligibility (green/yellow/red) from listing text
- `priority.py` — scores and labels each listing by company tier, role relevance, and eligibility
- `.github/workflows/test-slack.yml` — runs the bot on a schedule via GitHub Actions and commits the updated seen-job state

## Tech stack

Python · GitHub Actions (scheduled workflow) · Slack Incoming Webhooks

## Setup

1. Create a [Slack Incoming Webhook](https://api.slack.com/messaging/webhooks) for the channel you want alerts in.
2. In this repo's Settings → Secrets and variables → Actions, add it as `SLACK_WEBHOOK_URL`.
3. The workflow runs automatically every 15 minutes, or trigger it manually from the Actions tab.

---
*Built with Claude as a coding assistant — the prioritization logic, eligibility heuristics, source selection, and overall design are mine.*
