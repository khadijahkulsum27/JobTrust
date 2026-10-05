# test_two_ads.py - runs one real ad and one fake ad through the full pipeline.
# It does NOT save to the database.

import database
database.save_submission = lambda data: True
database.save_report = lambda processing_id, report: True

from app import app

REAL_AD = {
    "company_name": "Microsoft",
    "website": "https://www.microsoft.com",
    "email": "careers@microsoft.com",
    "job_title": "Software Developer",
    "job_description": (
        "We are looking for a Software Developer to join our engineering team. "
        "Responsibilities: build and test web applications, fix bugs, write clean "
        "code and work with senior engineers. Requirements: a BCA, B.Tech or similar "
        "degree, knowledge of Python and SQL, and good communication skills. "
        "Location: Bengaluru. Salary: Rs. 6,00,000 per year. "
        "Please apply through the official careers page on our company website."
    ),
    "salary": 600000,
    "experience_level": "fresher",
}

FAKE_AD = {
    "company_name": "Global Tech Solutions",
    "website": "https://globaltech-jobs-hiring.example",
    "email": "globaltech.hr2026@gmail.com",
    "job_title": "Data Entry Operator",
    "job_description": (
        "URGENT HIRING!!! Work from home data entry job. No interview required, "
        "direct selection. Earn Rs. 45,000 per month with simple work. "
        "Pay a registration fee of Rs. 999 to confirm your seat. "
        "Send your Aadhaar and bank details on WhatsApp 9876543210 today. "
        "Limited vacancies, apply now!!!"
    ),
    "salary": 540000,
    "experience_level": "fresher",
}


def run(label, ad):
    client = app.test_client()
    response = client.post("/api/analyze", json=ad)
    data = response.get_json()

    print("\n==========", label, "==========")
    print("HTTP status:", response.status_code)
    if response.status_code != 200:
        print(data)
        return

    for n in range(1, 7):
        e = data["engine%d" % n]
        print("Engine", n, "| status:", e.get("status"),
              "| score:", e.get("score"), "| risk:", e.get("risk"),
              "| errors:", e.get("errors"))

    report = data["engine6"].get("data", {})
    print("FINAL:", report.get("trust_assessment"))
    print("Red flags:", report.get("negative_findings"))
    print("Unsure:", report.get("uncertain_findings"))


run("REAL AD", REAL_AD)
run("FAKE AD", FAKE_AD)