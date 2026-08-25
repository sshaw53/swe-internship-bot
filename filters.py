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


def extract_years(text):
    """
    Finds graduation years mentioned in text.
    Example:
    'graduating between 2028 and 2030'
    -> [2028, 2030]
    """
    return [
        int(year)
        for year in re.findall(r"\b20\d{2}\b", text)
    ]


def classify_2029_eligibility(job):
    """
    Returns:
    green  = clearly eligible
    yellow = unclear / worth checking
    red    = clearly not eligible
    """

    title = job.get("title", "")
    description = job.get("description", "")
    requirements = job.get("requirements", "")

    text = f"{title} {description} {requirements}".lower()

    # Explicit sophomore-friendly wording
    if any(term in text for term in ELIGIBLE_TERMS):
        return {
            "status": "green",
            "label": "🟢 Class of 2029 eligible",
            "reason": "Sophomore/undergraduate eligibility detected",
        }

    # Explicit junior/senior/graduate restriction
    if any(term in text for term in INELIGIBLE_TERMS):
        return {
            "status": "red",
            "label": "🔴 Likely not eligible",
            "reason": "Upperclassman or graduate restriction detected",
        }

    years = extract_years(text)

    # Explicit mention of 2029 is a strong positive signal
    if 2029 in years:
        return {
            "status": "green",
            "label": "🟢 Class of 2029 eligible",
            "reason": "2029 graduation year explicitly mentioned",
        }

    # Detect graduation ranges such as:
    # "between December 2027 and June 2030"
    if len(years) >= 2:
        earliest = min(years)
        latest = max(years)

        if earliest <= 2029 <= latest:
            return {
                "status": "green",
                "label": "🟢 Class of 2029 eligible",
                "reason": f"2029 falls within stated graduation range {earliest}-{latest}",
            }

        if 2029 < earliest or 2029 > latest:
            return {
                "status": "red",
                "label": "🔴 Likely not eligible",
                "reason": f"2029 is outside stated graduation range {earliest}-{latest}",
            }

    # A single year can sometimes indicate a hard graduation requirement.
    # But without more context, we don't want to incorrectly reject a job.
    if len(years) == 1:
        return {
            "status": "yellow",
            "label": "🟡 Check eligibility",
            "reason": f"Graduation year {years[0]} mentioned, but context is unclear",
        }

    return {
        "status": "yellow",
        "label": "🟡 Check eligibility",
        "reason": "No clear graduation-year restriction detected",
    }
