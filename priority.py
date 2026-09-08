PRIORITY_COMPANIES = {
    "nvidia": 10,
    "microsoft": 10,
    "capital one": 10,
    "amazon": 10,
    "google": 10,
    "meta": 10,
    "apple": 9,
    "stripe": 9,
    "databricks": 9,
    "figma": 9,
    "airbnb": 9,
    "uber": 9,
    "linkedin": 9,
    "snowflake": 9,
    "palantir": 9,
    "roblox": 9,
    "doordash": 8,
    "salesforce": 8,
    "snap": 8,
    "coinbase": 8,
}

SPECIAL_PROGRAMS = {
    "ignite": 3,
    "explore": 3,
    "step": 3,
    "sophomore": 2,
    "first-year": 2,
    "freshman": 2,
    "early career": 1,
    "university": 1,
}


def score_job(job):
    company = job.get("company", "").lower()
    title = job.get("title", "").lower()

    score = 5
    reasons = []

    for name, company_score in PRIORITY_COMPANIES.items():
        if name in company:
            score = max(score, company_score)
            reasons.append(f"Watchlist company: {name.title()}")
            break

    for term, bonus in SPECIAL_PROGRAMS.items():
        if term in title:
            score += bonus
            reasons.append(f"Special program match: {term}")
    
    eligibility = job.get("eligibility", "")

    if "🟢" in eligibility:
        score += 1
        reasons.append("Class of 2029 appears eligible")

    score = min(score, 10)

    if score >= 9:
        label = "🔥🔥 HIGH PRIORITY — APPLY ASAP"
    elif score >= 7:
        label = "🔥 PRIORITY INTERNSHIP"
    else:
        label = "🚨 NEW SWE APPLICATION"

    return {
        "score": score,
        "label": label,
        "reasons": reasons,
    }
