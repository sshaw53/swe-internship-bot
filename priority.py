TIER_1 = [
    "google",
    "meta",
    "microsoft",
    "amazon",
    "nvidia",
    "apple",
    "stripe",
    "databricks",
    "openai",
    "anthropic",
    "figma",
    "airbnb",
]

TIER_2 = [
    "capital one",
    "uber",
    "linkedin",
    "roblox",
    "snowflake",
    "palantir",
    "doordash",
    "coinbase",
    "snap",
    "salesforce",
    "cloudflare",
    "mongodb",
    "atlassian",
    "dropbox",
    "reddit",
    "pinterest",
    "instacart",
    "affirm",
    "brex",
    "ramp",
    "plaid",
    "datadog",
    "twilio",
]

TIER_3 = [
    "jpmorgan",
    "j.p. morgan",
    "goldman sachs",
    "visa",
    "mastercard",
    "american express",
    "bloomberg",
    "adobe",
    "oracle",
    "ibm",
    "intuit",
    "servicenow",
    "deloitte",
    "fidelity",
    "bank of america",
    "wells fargo",
]


SPECIAL_PROGRAMS = [
    "ignite",
    "explore",
    "step",
    "sophomore",
    "first-year",
    "freshman",
    "early career",
]


CORE_SWE_TERMS = [
    "software engineer",
    "software engineering",
    "software developer",
    "software development",
    "sde",
]


AI_ML_TERMS = [
    "machine learning",
    "artificial intelligence",
    "ai engineer",
    "ml engineer",
]


WATCHLIST = [
    "microsoft",
    "capital one",
    "amazon",
    "nvidia",
]


def company_score(company):
    company = company.lower()

    if any(name in company for name in TIER_1):
        return 5, "Top-priority company"

    if any(name in company for name in TIER_2):
        return 4, "High-priority company"

    if any(name in company for name in TIER_3):
        return 3, "Strong company worth applying to"

    return 1, "Other employer"


def score_job(job):
    company = job.get("company", "").lower()
    title = job.get("title", "").lower()

    score = 0
    reasons = []

    # ----------------------------------
    # COMPANY VALUE
    # ----------------------------------

    points, company_reason = company_score(company)

    score += points
    reasons.append(company_reason)

    # ----------------------------------
    # ROLE RELEVANCE
    # ----------------------------------

    if any(term in title for term in AI_ML_TERMS):
        score += 2
        reasons.append("AI/ML engineering role")

    elif any(term in title for term in CORE_SWE_TERMS):
        score += 2
        reasons.append("Core software engineering role")

    else:
        score += 1
        reasons.append("Software-related role")

    # ----------------------------------
    # CLASS OF 2029 ELIGIBILITY
    # ----------------------------------

    eligibility = job.get("eligibility", "")

    if "🟢" in eligibility:
        score += 2
        reasons.append("Class of 2029 appears eligible")

    elif "🟡" in eligibility:
        score += 1
        reasons.append("Eligibility unclear — worth checking")

    # ----------------------------------
    # SOPHOMORE / EARLY-CAREER PROGRAM
    # ----------------------------------

    combined_text = f"{company} {title}"

    if any(term in combined_text for term in SPECIAL_PROGRAMS):
        score += 1
        reasons.append("Sophomore / early-career program")

    # ----------------------------------
    # PERSONAL WATCHLIST
    # ----------------------------------

    if any(name in company for name in WATCHLIST):
        score += 1
        reasons.append("Personal watchlist company")

    # ----------------------------------
    # CAP SCORE AT 10
    # ----------------------------------

    score = min(score, 10)

    # ----------------------------------
    # URGENCY LABEL
    # ----------------------------------

    if score >= 9:
        label = "🔥🔥 APPLY TODAY"

    elif score >= 8:
        label = "🔥 APPLY ASAP"

    elif score >= 6:
        label = "⭐ DEFINITELY APPLY"

    elif score >= 4:
        label = "🚨 CONSIDER APPLYING"

    else:
        label = "📌 LOWER PRIORITY"

    return {
        "score": score,
        "label": label,
        "reasons": reasons,
    }
