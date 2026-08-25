import requests

INTERNSHIP_FEED_URL = (
    "https://raw.githubusercontent.com/"
    "ApplyGuy/2027-Internships/main/data/internships.json"
)


def get_internships():
    response = requests.get(INTERNSHIP_FEED_URL, timeout=30)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    filtered_jobs = []

    for job in jobs:
        category = job.get("category", "").lower()
        title = job.get("title", "").lower()
        season = job.get("season", "").lower()

        # Keep software engineering roles
        is_software = (
            "software engineering" in category
            or "software engineer" in title
            or "software developer" in title
            or "software development" in title
        )

        # Keep Summer 2027 roles.
        # Some listings don't specify the season in the structured field,
        # so we also check the title.
        is_summer_2027 = (
            "summer 2027" in season
            or "summer 2027" in title
        )

        # Avoid graduate-only internships
        is_grad_role = any(
            term in title
            for term in ["phd", "ph.d", "masters", "master's"]
        )

        if is_software and is_summer_2027 and not is_grad_role:
            filtered_jobs.append(job)

    return filtered_jobs


if __name__ == "__main__":
    jobs = get_internships()

    print(f"Found {len(jobs)} Summer 2027 SWE internships.\n")

    for job in jobs[:10]:
        print(job["company"], "-", job["title"])
