import requests
import hashlib


APPLYGUY_URL = (
    "https://raw.githubusercontent.com/"
    "ApplyGuy/2027-Internships/main/data/internships.json"
)

SIMPLIFY_URL = (
    "https://raw.githubusercontent.com/"
    "SimplifyJobs/Summer2027-Internships/dev/"
    ".github/scripts/listings.json"
)


SWE_KEYWORDS = [
    "software engineer",
    "software engineering",
    "software developer",
    "software development",
    "backend",
    "front end",
    "frontend",
    "full stack",
    "full-stack",
    "mobile engineer",
    "platform engineer",
    "systems engineer",
    "machine learning engineer",
    "ml engineer",
]


def make_id(company, title, url):
    """
    Create a stable ID so jobs from different sources
    can still be compared/deduplicated.
    """
    raw = f"{company.lower()}::{title.lower()}::{url}"
    return hashlib.sha256(raw.encode()).hexdigest()


def looks_like_swe(title):
    title = title.lower()

    return any(
        keyword in title
        for keyword in SWE_KEYWORDS
    )


def get_applyguy_jobs():
    response = requests.get(APPLYGUY_URL, timeout=30)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    results = []

    for job in jobs:
        title = job.get("title", "")
        season = job.get("season", "")

        is_summer_2027 = (
            "summer 2027" in season.lower()
            or "summer 2027" in title.lower()
            or season.strip() == "2027"
        )

        if not is_summer_2027:
            continue

        if not looks_like_swe(title):
            continue

        url = (
            job.get("listingUrl")
            or job.get("url")
            or ""
        )

        normalized = {
            "id": job.get("id")
            or make_id(
                job.get("company", ""),
                title,
                url
            ),
            "company": job.get(
                "company",
                "Unknown company"
            ),
            "title": title,
            "location": job.get(
                "location",
                "Location not listed"
            ),
            "posted": job.get(
                "posted",
                "Not listed"
            ),
            "listingUrl": url,
            "description": job.get(
                "description",
                ""
            ),
            "requirements": job.get(
                "requirements",
                ""
            ),
            "source": "ApplyGuy",
        }

        results.append(normalized)

    return results


def get_simplify_jobs():
    response = requests.get(
        SIMPLIFY_URL,
        timeout=30
    )
    response.raise_for_status()

    listings = response.json()

    results = []

    for job in listings:
        if not job.get("active", False):
            continue

        title = job.get("title", "")
        terms = job.get("terms", [])

        terms_text = " ".join(terms).lower()

        if "summer 2027" not in terms_text:
            continue

        if not looks_like_swe(title):
            continue

        company = job.get(
            "company_name",
            "Unknown company"
        )

        locations = job.get("locations", [])

        if isinstance(locations, list):
            location = ", ".join(locations)
        else:
            location = str(locations)

        url = job.get("url", "")

        normalized = {
            "id": make_id(
                company,
                title,
                url
            ),
            "company": company,
            "title": title,
            "location": (
                location
                or "Location not listed"
            ),
            "posted": job.get(
                "date_posted",
                "Not listed"
            ),
            "listingUrl": url,
            "description": "",
            "requirements": "",
            "source": "Simplify",
        }

        results.append(normalized)

    return results


import re


def normalize_text(text):
    text = text.lower()

    text = re.sub(
        r"\b(summer|internship|intern|2027)\b",
        "",
        text
    )

    text = re.sub(r"[^a-z0-9]+", " ", text)

    return " ".join(text.split())


def normalize_company(company):
    company = company.lower()

    replacements = [
        "inc.",
        "inc",
        "llc",
        "corporation",
        "corp.",
        "corp",
        "company",
    ]

    for term in replacements:
        company = company.replace(term, "")

    return " ".join(company.split())


def deduplicate_jobs(jobs):
    unique = {}

    for job in jobs:
        company = normalize_company(
            job.get("company", "")
        )

        title = normalize_text(
            job.get("title", "")
        )

        location = normalize_text(
            job.get("location", "")
        )

        key = (
            company,
            title,
            location,
        )

        if key not in unique:
            unique[key] = job

    return list(unique.values())


def get_internships():
    all_jobs = []

    try:
        applyguy_jobs = get_applyguy_jobs()
        print(
            f"ApplyGuy: "
            f"{len(applyguy_jobs)} matches"
        )
        all_jobs.extend(applyguy_jobs)

    except Exception as e:
        print(
            f"ApplyGuy source failed: {e}"
        )

    try:
        simplify_jobs = get_simplify_jobs()
        print(
            f"Simplify: "
            f"{len(simplify_jobs)} matches"
        )
        all_jobs.extend(simplify_jobs)

    except Exception as e:
        print(
            f"Simplify source failed: {e}"
        )

    jobs = deduplicate_jobs(all_jobs)

    print(
        f"Combined: "
        f"{len(jobs)} unique internships"
    )

    return jobs


if __name__ == "__main__":
    jobs = get_internships()

    print()

    for job in jobs[:20]:
        print(
            job["source"],
            "|",
            job["company"],
            "-",
            job["title"]
        )
