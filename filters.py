import re


ELIGIBLE_TERMS = [
    "sophomore",
    "rising sophomore",
    "first-year",
    "freshman",
    "undergraduate students",
    "currently pursuing a bachelor's",
    "currently pursuing a bachelor’s",
]

INELIGIBLE_TERMS = [
    "junior standing",
    "must be a junior",
    "rising junior",
    "senior standing",
    "must be a senior",
    "graduate student",
    "master's student",
    "masters student",
    "phd student",
    "ph.d. student",
]


def classify_2029_eligibility(job):
    """
    green  = clearly eligible
    yellow = unclear / worth checking
    red    = clearly not eligible
    """

    # IMPORTANT:
    # Do NOT use the title here.
    # Titles contain "Summer 2027", which is NOT a graduation year.
    description = job.get("description", "")
    requirements = job.get("requirements", "")

    text = f"{description} {requirements}".lower()

    if any(term in text for term in ELIGIBLE_TERMS):
        return {
            "status": "green",
            "label": "🟢 Class of 2029 eligible",
            "reason": "Sophomore or undergraduate eligibility detected",
        }

    if any(term in text for term in INELIGIBLE_TERMS):
        return {
            "status": "red",
            "label": "🔴 Likely not eligible",
            "reason": "Upperclassman or graduate restriction detected",
        }

    # Look specifically for graduation-related wording,
    # rather than treating every year as a graduation requirement.
    graduation_patterns = [
        r"graduat(?:e|ing|ion).*?(20\d{2}).*?(20\d{2})",
        r"expected graduation.*?(20\d{2}).*?(20\d{2})",
        r"graduation date.*?(20\d{2}).*?(20\d{2})",
    ]

    for pattern in graduation_patterns:
        match = re.search(pattern, text)

        if match:
            year1 = int(match.group(1))
            year2 = int(match.group(2))

            earliest = min(year1, year2)
            latest = max(year1, year2)

            if earliest <= 2029 <= latest:
                return {
                    "status": "green",
                    "label": "🟢 Class of 2029 eligible",
                    "reason": f"2029 falls within graduation range {earliest}-{latest}",
                }

            return {
                "status": "red",
                "label": "🔴 Likely not eligible",
                "reason": f"2029 is outside graduation range {earliest}-{latest}",
            }

    if re.search(
        r"(graduat(?:e|ing|ion)|expected graduation).*?2029",
        text
    ):
        return {
            "status": "green",
            "label": "🟢 Class of 2029 eligible",
            "reason": "2029 is explicitly included in graduation eligibility",
        }

    return {
        "status": "yellow",
        "label": "🟡 Eligibility unclear",
        "reason": "No class-year restriction found — check application",
    }
