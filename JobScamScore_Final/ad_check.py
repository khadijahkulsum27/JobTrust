import re

# Words normally found in a job advertisement, scam ads included.
JOB_WORDS = {
    "job", "role", "position", "hiring", "vacancy", "vacancies", "candidate",
    "candidates", "responsibilities", "requirements", "qualification",
    "skills", "experience", "salary", "team", "apply", "application", "work",
    "working", "develop", "developer", "engineer", "manager", "executive",
    "intern", "internship", "company", "duties", "degree", "looking", "join",
    "joining", "opportunity", "knowledge", "ability", "testing", "analyst",
    "support", "sales", "design", "designer", "accountant", "interview",
    "fee", "earn", "income", "money", "payment", "deposit", "registration",
    "offer", "income", "weekly", "monthly", "bonus", "training",
}


def check_job_ad(text):
    """Returns (True, "") if the text looks like a job ad, else (False, reason)."""
    words = re.findall(r"[a-zA-Z]+", str(text).lower())

    if len(words) < 8:
        return False, "The text is too short to be a job advertisement."

    hits = {w for w in words if w in JOB_WORDS}

    if len(hits) < 2:
        return False, "This does not look like a job advertisement. Please paste the full job ad."

    return True, ""