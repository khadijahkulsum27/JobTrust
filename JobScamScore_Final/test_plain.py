from app import app

c = app.test_client()


def run(data):
    return c.post("/api/analyze", json=data).get_json()["plain_explanation"]


scam = run({
    "company_name": "Fast Hire Solutions",
    "website": "https://example.com",
    "email": "fasthire.jobs@gmail.com",
    "job_title": "Data Entry Operator",
    "job_description": "URGENT HIRING!!! Work from home and earn money fast. No interview, guaranteed job. Pay a registration fee of Rs 2000 to confirm your joining. Apply now, limited vacancies. Contact us on WhatsApp today.",
    "experience_level": "fresher",
})

genuine = run({
    "company_name": "Microsoft",
    "website": "https://www.microsoft.com",
    "email": "careers@microsoft.com",
    "job_title": "Software Developer",
    "job_description": "We are looking for a Software Developer to join our team. The candidate should have experience with Python and web development. Please apply through our official company website.",
    "experience_level": "fresher",
})

for name, result in (("SCAM", scam), ("GENUINE", genuine)):
    print()
    print(name + ":", result["headline"])
    print(result["summary"])
    for item in result["why"]:
        print("  ", item["level"], "-", item["text"][:100])