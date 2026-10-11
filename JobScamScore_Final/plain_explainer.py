"""
plain_explainer.py

Turns the engines' raw results into short sentences an ordinary person can read.
It only says things the engines really returned. It never changes any score.
"""


def _get(data, *path, default=None):
    for key in path:
        if not isinstance(data, dict):
            return default
        data = data.get(key)
        if data is None:
            return default
    return data


def _count(n, one, many):
    return str(n) + " " + (one if n == 1 else many)


def build_plain_explanation(e1, e2, e3, e4, ml, decision, confidence, score):
    items = []

    def add(level, text):
        items.append({"level": level, "text": text})

    try:
        ssl_said = False
        age_said = False
        salary_said = False
        pressure_said = False

        # ---------------- Company identity (Engine 1) ----------------
        if _get(e1, "data", "website_verification"):
            site_status = _get(e1, "data", "website_verification", "status")
            site_risk = _get(e1, "data", "website_verification", "risk")
            if site_status == "SUCCESS" and site_risk != "HIGH":
                add("good", "The company website opens normally.")
            elif site_status == "SUCCESS":
                add("bad", "The company website shows a 'page not found' error.")
            else:
                add("warn", "We could not open the website you entered.")

            ssl_status = _get(e1, "data", "ssl_verification", "status")
            if ssl_status == "SUCCESS":
                add("good", "The website uses a valid security certificate (the padlock in the browser).")
                ssl_said = True
            elif ssl_status == "FAILED":
                add("bad", "The website's security certificate is missing, invalid or expired.")
                ssl_said = True

            public_email = _get(e1, "data", "email_verification", "data", "public_email")
            domain_match = _get(e1, "data", "domain_matching", "data", "domain_match")
            if public_email:
                add("bad", "The recruiter's email is a free address (like Gmail or Yahoo), not an email from the company itself.")
            elif domain_match is True:
                add("good", "The recruiter's email ends with the same name as the company's website.")
            elif domain_match is False:
                add("warn", "The recruiter's email does not match the company's website name.")

            years = _get(e1, "data", "whois_verification", "data", "domain_age_years")
            if isinstance(years, int):
                age_said = True
                if years >= 2:
                    add("good", "The website name was registered about " + _count(years, "year", "years") + " ago, so it is well established.")
                elif years >= 1:
                    add("warn", "The website name was registered only about 1 year ago.")
                else:
                    add("bad", "The website name was registered less than a year ago. Scam websites are often brand new.")

            registered = _get(e1, "data", "mca_verification", "data", "registered")
            if registered is True:
                add("good", "The company name was found in our small sample list of registered companies.")
            elif registered is False:
                add("warn", "The company name is not in our small sample list of registered companies. That does not mean it is fake, only that we could not confirm it.")
        else:
            add("warn", "The company identity checks could not run, because the company website or the recruiter's email was not provided.")

        # ---------------- Website safety (Engine 4) ----------------
        d4 = _get(e4, "data", default={})
        if isinstance(d4, dict) and d4:
            https = d4.get("https_check") or {}
            if not ssl_said:
                if https.get("https") and https.get("certificate_valid"):
                    add("good", "The website uses a valid security certificate (the padlock in the browser).")
                elif "INVALID_CERTIFICATE" in (https.get("indicators") or []):
                    add("bad", "The website's security certificate is invalid or expired.")
                elif https.get("status") == "AVAILABLE" and not https.get("https"):
                    add("bad", "The website does not use a secure connection (https).")

            if not age_said:
                category = _get(d4, "rdap_check", "domain_age_category")
                if category == "RECENT":
                    add("bad", "The website name was registered only recently (less than 6 months ago). Scam websites are often brand new.")
                elif category == "ESTABLISHED":
                    add("good", "The website name was registered more than 2 years ago.")

            phish = d4.get("phishing_detection") or {}
            safe = phish.get("safe_browsing") or {}
            if safe.get("threat_found"):
                add("bad", "Google Safe Browsing lists this website as unsafe.")
            else:
                if (phish.get("indicator_count") or 0) >= 1:
                    add("warn", "The website address has patterns that are sometimes seen in fake websites.")
                if safe.get("available"):
                    add("good", "Google Safe Browsing has no warning about this website.")

            threat = d4.get("threat_intelligence") or {}
            if threat.get("available"):
                if threat.get("threat_detected"):
                    add("bad", "VirusTotal, a service that combines many virus scanners, flagged this website.")
                else:
                    add("good", "VirusTotal, a service that combines many virus scanners, has no warnings about this website.")
        else:
            add("warn", "The website safety checks could not run, because no company website was provided.")

        # ---------------- What the ad says (Engines 2 and 3) ----------------
        b = _get(e3, "data", "scam_behavior_analysis", "data", default={}) or {}

        if b.get("payment_request"):
            add("bad", "The ad asks for money (a fee or deposit). Real employers do not charge you to get a job.")
        if b.get("sensitive_information_request"):
            add("bad", "The ad asks for private details such as Aadhaar, PAN, bank details or an OTP.")
        if b.get("guaranteed_employment"):
            add("bad", "The ad promises a guaranteed job, which no honest employer can do.")
        if b.get("no_interview"):
            add("bad", "The ad says you will be selected without an interview.")
        if b.get("unrealistic_income"):
            add("bad", "The ad promises unrealistically high earnings.")
        if b.get("messaging_recruitment"):
            add("warn", "The ad asks you to contact the recruiter through WhatsApp, Telegram or Signal, which many scams do.")
        if b.get("pressure_tactics"):
            add("warn", "The ad pushes you to act fast (for example 'hurry' or 'only today'), a common pressure trick.")
            pressure_said = True

        phrases = _get(e2, "data", "urgency_analysis", "data", "detected_phrases", default=[]) or []
        if phrases and not pressure_said:
            add("warn", "The ad uses pressure words such as '" + "', '".join(phrases[:3]) + "'.")

        salary_status = _get(e3, "data", "salary_consistency_analysis", "data", "salary_status")
        if salary_status == "NORMAL":
            add("good", "The pay offered is within the usual range in our small reference table for this job.")
            salary_said = True
        elif salary_status == "UNUSUAL":
            add("warn", "The pay offered is higher than usual for this kind of job.")
            salary_said = True
        elif salary_status == "HIGHLY_UNUSUAL":
            add("bad", "The pay offered is far higher than normal for this kind of job, a common trick to attract people.")
            salary_said = True

        if not salary_said and _get(e2, "data", "salary_analysis", "data", "excessive_salary"):
            add("warn", "The pay mentioned in the ad is unusually high.")

        keywords = _get(e2, "data", "keyword_analysis", "data", "detected_keywords", default=[]) or []
        if keywords:
            add("warn", "The ad contains words often used in scam ads: '" + "', '".join(keywords[:4]) + "'.")

        if (_get(e2, "data", "grammar_analysis", "data", "issue_count", default=0) or 0) >= 2:
            add("warn", "The writing has several problems (for example shouting in capital letters or too many exclamation marks).")

        for issue in (_get(e3, "data", "job_consistency_analysis", "data", "consistency_issues", default=[]) or []):
            add("warn", "Something does not add up in the ad: " + str(issue))

        # ---------------- Our text-reading model (second opinion) ----------------
        if isinstance(ml, dict) and ml.get("available"):
            label = ml.get("label")
            if label == "LIKELY_FAKE":
                add("warn", "Our text-reading model thinks the wording looks like fake job ads it learned from.")
            elif label == "LIKELY_GENUINE":
                add("good", "Our text-reading model thinks the wording looks like normal job ads.")
            elif label == "UNSURE":
                add("warn", "Our text-reading model is not sure about the wording of this ad.")

    except Exception:
        pass

    order = {"bad": 0, "warn": 1, "good": 2}
    items.sort(key=lambda i: order[i["level"]])

    bad = sum(1 for i in items if i["level"] == "bad")
    warn = sum(1 for i in items if i["level"] == "warn")
    good = sum(1 for i in items if i["level"] == "good")

    if decision == "TRUSTED":
        headline = "This job looks safe based on our checks."
    elif decision == "HIGH_RISK":
        headline = "This job looks risky. Do not pay money or send personal documents until you have verified it yourself."
    else:
        headline = "Be careful. Some of our checks found warning signs or could not be completed."

    summary = (
        "We found " + _count(bad, "serious warning sign", "serious warning signs") + ", "
        + _count(warn, "thing to be careful about", "things to be careful about") + " and "
        + _count(good, "good sign", "good signs") + "."
    )

    incomplete_note = ""
    try:
        ran = round(float(confidence) / 25)
        if ran < 4:
            incomplete_note = (
                "Only " + str(ran) + " of our 4 checks could run, because the company website or the recruiter's "
                "email was missing. A check that could not run counts against the score. This does not mean the job "
                "is fake. Add the website and the email, then scan again."
            )
    except (TypeError, ValueError):
        pass

    advice = [
        "Never pay money to get a job. Real employers do not charge fees for hiring, training or joining.",
        "Do not share Aadhaar, PAN, bank details or OTPs before you have met the employer and verified the company.",
        "Check the company's own website, and search for the recruiter's name, before you reply.",
    ]
    if decision == "HIGH_RISK":
        advice.append(
            "If you have already paid money or shared documents, tell your bank and report it at cybercrime.gov.in "
            "or call the helpline 1930."
        )

    return {
        "headline": headline,
        "summary": summary,
        "why": items,
        "incomplete_note": incomplete_note,
        "advice": advice,
    }