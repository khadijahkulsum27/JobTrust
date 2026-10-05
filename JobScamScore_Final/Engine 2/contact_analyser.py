import re

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_CONTACT_ANALYZER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def analyze_contact(job_description):
    """
    Analyzes contact information present in a job description.

    Parameters:
        job_description (str): Job description text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_CONTACT_ANALYZER
    )

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if not isinstance(job_description, str):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description must be provided as text."
            )

            return result

        text = job_description.strip()

        if not text:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # EMAIL DETECTION
        # =================================================

        email_pattern = (
            r"[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}"
        )

        emails = re.findall(
            email_pattern,
            text
        )

        # =================================================
        # PHONE NUMBER DETECTION
        # =================================================

        phone_pattern = (
            r"(?:\+?\d{1,3}[\s.-]?)?"
            r"(?:\(?\d{3,5}\)?[\s.-]?)"
            r"\d{3,5}[\s.-]?\d{3,5}"
        )

        phone_numbers = re.findall(
            phone_pattern,
            text
        )

        # =================================================
        # MESSAGING PLATFORM DETECTION
        # =================================================

        messaging_platforms = []

        messaging_keywords = [
            "whatsapp",
            "telegram",
            "signal"
        ]

        text_lower = text.lower()

        for platform in messaging_keywords:

            if platform in text_lower:

                messaging_platforms.append(
                    platform
                )

        # Remove duplicates
        messaging_platforms = list(
            dict.fromkeys(
                messaging_platforms
            )
        )

        # =================================================
        # CONTACT ANALYSIS
        # =================================================

        contact_found = bool(
            emails
            or phone_numbers
            or messaging_platforms
        )

        # Messaging platforms receive additional caution
        if messaging_platforms:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Messaging-platform contact information detected."
            )

        elif contact_found:

            risk = RISK_LOW

            result["remarks"].append(
                "Contact information detected in the job posting."
            )

        else:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "No direct contact information detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "contact_found": contact_found,
            "email_count": len(emails),
            "phone_count": len(phone_numbers),
            "messaging_platforms": messaging_platforms
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result