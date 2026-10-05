"""
test_postings.py

Sanity check for the JobTrust backend.

Sends 14 HAND-WRITTEN sample job postings (8 genuine-style, 6 scam-style)
to the running Flask API and prints what the system decided for each.

IMPORTANT
- These are made-up examples, NOT real postings and NOT a dataset.
- The result is a sanity check, NOT an accuracy figure.
- Flask must be running at http://127.0.0.1:5000 before you start.
- Every posting is saved to jobscamscore.db (it will appear in History).
  Copy jobscamscore.db first if you want to keep a clean copy.

How to run (from the JobScamScore_Final folder):
    .\\.venv\\Scripts\\python.exe test_postings.py
"""

import json
import time

import requests

API_URL = "http://127.0.0.1:5000/api/analyze"
TIMEOUT_SECONDS = 180

# Pass rules
#   genuine: must NEVER be HIGH_RISK. TRUSTED is ideal, REVIEW is acceptable.
#   scam:    must NEVER be TRUSTED.   HIGH_RISK is ideal, REVIEW is acceptable.

POSTINGS = [
    # ------------------------------------------------------------------
    # GENUINE-STYLE (with website and email)
    # ------------------------------------------------------------------
    {
        "kind": "genuine",
        "label": "Infosys - Software Engineer",
        "data": {
            "company_name": "Infosys",
            "job_title": "Software Engineer",
            "job_description": (
                "We are hiring Software Engineers for our development centres. "
                "Responsibilities include writing and testing code in Java or Python, "
                "fixing defects and taking part in code reviews. Requirements: a "
                "Bachelor's degree in engineering or computer science, good knowledge "
                "of data structures and SQL, and clear communication skills. Location: "
                "Bengaluru. Selected candidates go through an online test and two "
                "technical interviews. Please apply through the careers page."
            ),
            "website": "https://www.infosys.com",
            "email": "careers@infosys.com",
            "salary": 600000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "genuine",
        "label": "TCS - Data Analyst",
        "data": {
            "company_name": "TCS",
            "job_title": "Data Analyst",
            "job_description": (
                "The Data Analyst will collect, clean and analyse business data and "
                "prepare weekly dashboards for project managers. Skills: SQL, Excel, "
                "basic Python and a good understanding of statistics. Qualification: "
                "Bachelor's degree in any quantitative subject. The role is based in "
                "Chennai and includes mentoring by a senior analyst during the first "
                "six months. The hiring process has an aptitude test and an interview."
            ),
            "website": "https://www.tcs.com",
            "email": "careers@tcs.com",
            "salary": 500000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "genuine",
        "label": "Wipro - Web Developer",
        "data": {
            "company_name": "Wipro",
            "job_title": "Web Developer",
            "job_description": (
                "We are looking for a Web Developer with one to two years of "
                "experience in JavaScript, HTML and CSS. You will build user "
                "interfaces for client applications, work with the design team and "
                "write unit tests. Experience with a modern framework such as React "
                "is an advantage. Location: Hyderabad. Hybrid working is available. "
                "Apply now through our official careers portal."
            ),
            "website": "https://www.wipro.com",
            "email": "careers@wipro.com",
            "salary": 700000,
            "experience_level": "junior",
        },
    },
    {
        "kind": "genuine",
        "label": "Accenture - Financial Analyst",
        "data": {
            "company_name": "Accenture",
            "job_title": "Financial Analyst",
            "job_description": (
                "Join our finance operations team as a Financial Analyst. You will "
                "prepare monthly reports, reconcile accounts and support budgeting "
                "for client engagements. Requirements: a degree in commerce or "
                "finance, strong Excel skills and attention to detail. Location: "
                "Pune. Interviews are held on video call with the hiring manager and "
                "a member of the HR team."
            ),
            "website": "https://www.accenture.com",
            "email": "careers@accenture.com",
            "salary": 500000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "genuine",
        "label": "IBM - Software Developer",
        "data": {
            "company_name": "IBM",
            "job_title": "Software Developer",
            "job_description": (
                "IBM is hiring a Software Developer for its cloud services team. "
                "You will design and develop microservices using Python or Java, "
                "write API documentation and take part in on-call rotation. We "
                "expect two to four years of experience, a good understanding of "
                "databases and experience with version control. Location: "
                "Bengaluru. The process includes a coding exercise and technical "
                "interviews."
            ),
            "website": "https://www.ibm.com",
            "email": "careers@ibm.com",
            "salary": 900000,
            "experience_level": "junior",
        },
    },
    {
        "kind": "genuine",
        "label": "Zoho - Customer Support",
        "data": {
            "company_name": "Zoho",
            "job_title": "Customer Support",
            "job_description": (
                "We need Customer Support executives to answer customer questions "
                "by email and chat, solve product issues and document common "
                "problems. Requirements: good written English, patience and "
                "willingness to learn our products. Freshers are welcome. Training "
                "is provided for the first month. Location: Chennai. Working hours "
                "are nine to six with weekends off."
            ),
            "website": "https://www.zoho.com",
            "email": "careers@zoho.com",
            "salary": 300000,
            "experience_level": "fresher",
        },
    },
    # ------------------------------------------------------------------
    # GENUINE-STYLE (website and email NOT provided: REVIEW is expected)
    # ------------------------------------------------------------------
    {
        "kind": "genuine",
        "label": "Local firm - Accountant (no website or email)",
        "data": {
            "company_name": "Greenfield Accounts LLP",
            "job_title": "Accountant",
            "job_description": (
                "Greenfield Accounts LLP is looking for an Accountant to maintain "
                "books of accounts, prepare GST returns and assist with audits. "
                "Requirements: B.Com degree, working knowledge of Tally and Excel, "
                "and one year of experience preferred. Location: Mysuru. "
                "Interviews will be held at our office on weekdays."
            ),
            "salary": 300000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "genuine",
        "label": "Local firm - Marketing Executive (no website or email)",
        "data": {
            "company_name": "Sunrise Digital Studio",
            "job_title": "Marketing Executive",
            "job_description": (
                "We are a small digital agency hiring a Marketing Executive to "
                "manage social media calendars, write blog posts and track campaign "
                "results. Requirements: good writing skills, familiarity with "
                "common social platforms and basic analytics. Freshers can apply. "
                "Location: Bengaluru. We will contact shortlisted candidates for "
                "an interview."
            ),
            "salary": 350000,
            "experience_level": "fresher",
        },
    },
    # ------------------------------------------------------------------
    # SCAM-STYLE
    # ------------------------------------------------------------------
    {
        "kind": "scam",
        "label": "Scam 1 - fee + WhatsApp + guaranteed job",
        "data": {
            "company_name": "Dream Careers Hub",
            "job_title": "Data Entry Operator",
            "job_description": (
                "URGENT HIRING!! Work from home data entry job. Earn Rs 5000 daily, "
                "easy money, no experience needed. 100% placement and guaranteed job "
                "with no interview required. Pay Rs 1500 registration fee to confirm "
                "your seat. Contact us on WhatsApp 9876543210. Limited vacancies, "
                "apply now, last chance, only today!!"
            ),
            "email": "dreamcareershub@gmail.com",
            "experience_level": "fresher",
        },
    },
    {
        "kind": "scam",
        "label": "Scam 2 - Aadhaar, bank details, processing fee",
        "data": {
            "company_name": "Global Hiring Desk",
            "job_title": "Customer Support",
            "job_description": (
                "Congratulations, you are selected without interview for our "
                "customer support team. To receive your offer letter send your "
                "Aadhaar, PAN card and bank account details on Telegram. A refundable "
                "processing fee of Rs 2000 must be paid today. Direct selection, "
                "join immediately, hurry as vacancies are limited."
            ),
            "website": "https://www.global-hiring-desk.example",
            "email": "hr.globalhiring@gmail.com",
            "experience_level": "fresher",
        },
    },
    {
        "kind": "scam",
        "label": "Scam 3 - impersonating a big company",
        "data": {
            "company_name": "Infosys Recruitment Cell",
            "job_title": "Software Engineer",
            "job_description": (
                "Infosys direct recruitment for freshers. Instant selection, no "
                "interview, guaranteed employment and 100% selection. Pay a joining "
                "fee of Rs 3500 and a security deposit to receive your appointment "
                "letter. Salary Rs 25,00,000 per year for freshers. Contact our "
                "recruiter on WhatsApp. Act immediately, only today."
            ),
            "website": "https://www.infosys-recruitment-india.example",
            "email": "infosys.hr.recruit@gmail.com",
            "salary": 2500000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "scam",
        "label": "Scam 4 - task scam, earn money fast",
        "data": {
            "company_name": "Smart Earn Solutions",
            "job_title": "Online Task Executive",
            "job_description": (
                "Earn money fast from your phone. Easy money, guaranteed income and "
                "earn thousands daily by completing simple tasks like liking videos. "
                "Join our Telegram group, send money to unlock your first task and "
                "share the OTP you receive to verify your account. High income with "
                "no experience. Hurry, limited vacancies."
            ),
            "email": "smartearn.solutions@gmail.com",
            "experience_level": "fresher",
        },
    },
    {
        "kind": "scam",
        "label": "Scam 5 - unrealistic pay + training fee",
        "data": {
            "company_name": "Alpha Worldwide Services",
            "job_title": "Office Administrator",
            "job_description": (
                "Only today! Join immediately as an Office Administrator. Salary "
                "Rs 90,000 per month for freshers, high income with no experience. "
                "A training fee must be paid before the first day and you must share "
                "your bank details for salary setup. Last chance, limited vacancies, "
                "apply now."
            ),
            "email": "alpha.worldwide@yahoo.com",
            "salary": 1080000,
            "experience_level": "fresher",
        },
    },
    {
        "kind": "scam",
        "label": "Scam 6 - overseas job + visa fee",
        "data": {
            "company_name": "Prime Overseas Jobs",
            "job_title": "Accountant",
            "job_description": (
                "Overseas accountant jobs with guaranteed job and instant selection. "
                "No interview required. Pay an application fee and a visa processing "
                "fee to book your placement. Send money through the link we share on "
                "WhatsApp. Earn lakhs every month. Hurry, act immediately."
            ),
            "email": "primeoverseas.jobs@gmail.com",
            "experience_level": "senior",
        },
    },
]


def judge(kind, decision):
    """Return PASS / OK / FAIL for one result."""
    if decision is None:
        return "ERROR"
    if kind == "genuine":
        if decision == "HIGH_RISK":
            return "FAIL"
        return "PASS" if decision == "TRUSTED" else "OK"
    # scam
    if decision == "TRUSTED":
        return "FAIL"
    return "PASS" if decision == "HIGH_RISK" else "OK"


def main():
    results = []
    print("Sending %d sample postings to %s" % (len(POSTINGS), API_URL))
    print("(each one can take 5-20 seconds because the engines check live websites)\n")

    header = "%-52s %-8s %6s %-10s %-7s %4s %5s  %s" % (
        "Posting", "Kind", "Score", "Decision", "Risk", "Conf", "Eng", "Result")
    print(header)
    print("-" * len(header))

    for posting in POSTINGS:
        started = time.time()
        decision = risk = None
        score = confidence = engines = None
        error = ""

        try:
            response = requests.post(API_URL, json=posting["data"], timeout=TIMEOUT_SECONDS)
            if response.status_code != 200:
                error = "HTTP %s: %s" % (response.status_code, response.text[:120])
            else:
                body = response.json()
                report = (body.get("engine6") or {}).get("data") or {}
                assessment = report.get("trust_assessment") or {}
                decision = assessment.get("decision")
                risk = assessment.get("risk")
                score = assessment.get("trust_score")
                confidence = assessment.get("confidence")
                engines = len(report.get("engine_findings") or [])
        except Exception as exc:  # network error, timeout, bad JSON ...
            error = str(exc)[:120]

        verdict = judge(posting["kind"], decision)
        results.append({
            "label": posting["label"],
            "kind": posting["kind"],
            "score": score,
            "decision": decision,
            "risk": risk,
            "confidence": confidence,
            "engines_scored": engines,
            "result": verdict,
            "error": error,
            "seconds": round(time.time() - started, 1),
        })

        print("%-52s %-8s %6s %-10s %-7s %4s %5s  %s" % (
            posting["label"][:52],
            posting["kind"],
            "-" if score is None else round(score, 1),
            decision or "-",
            risk or "-",
            "-" if confidence is None else int(confidence),
            "-" if engines is None else engines,
            verdict + (("  <- " + error) if error else ""),
        ))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    genuine = [r for r in results if r["kind"] == "genuine"]
    scams = [r for r in results if r["kind"] == "scam"]

    def count(rows, verdict):
        return sum(1 for r in rows if r["result"] == verdict)

    print("GENUINE-STYLE (%d): TRUSTED=%d  REVIEW=%d  HIGH_RISK(wrong)=%d  errors=%d" % (
        len(genuine),
        sum(1 for r in genuine if r["decision"] == "TRUSTED"),
        sum(1 for r in genuine if r["decision"] == "REVIEW"),
        count(genuine, "FAIL"),
        count(genuine, "ERROR"),
    ))
    print("SCAM-STYLE    (%d): HIGH_RISK=%d  REVIEW=%d  TRUSTED(wrong)=%d  errors=%d" % (
        len(scams),
        sum(1 for r in scams if r["decision"] == "HIGH_RISK"),
        sum(1 for r in scams if r["decision"] == "REVIEW"),
        count(scams, "FAIL"),
        count(scams, "ERROR"),
    ))
    print("\nPASS = ideal answer, OK = acceptable (REVIEW), FAIL = dangerous mistake.")
    print("This is a sanity check on 14 made-up examples, not an accuracy measurement.")

    with open("test_postings_results.json", "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    print("Full results saved to test_postings_results.json")


if __name__ == "__main__":
    main()
