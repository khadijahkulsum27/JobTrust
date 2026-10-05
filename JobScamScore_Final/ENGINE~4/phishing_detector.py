"""
Engine 4 - Phishing Detector

Detects common suspicious patterns in website URLs
that may indicate phishing or deceptive websites.
"""

import re
from urllib.parse import urlparse

from utils.constants import (
    CYBER_INDICATOR_SUSPICIOUS_URL,
    CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN,
)


# Common words frequently seen in deceptive URLs.
SUSPICIOUS_URL_TERMS = [
    "login",
    "signin",
    "verify",
    "verification",
    "account",
    "secure",
    "update",
    "confirm",
    "authentication",
    "password",
    "credential",
    "wallet",
    "bank",
    "payment",
    "support"
]


# Words commonly associated with urgency or impersonation.
SUSPICIOUS_DOMAIN_TERMS = [
    "verify",
    "secure",
    "account",
    "support",
    "official",
    "career",
    "job",
    "recruitment"
]


def detect_phishing(url):
    """
    Analyze a URL for common phishing indicators.

    Args:
        url (str): Website URL.

    Returns:
        dict: Phishing detection result.
    """

    result = {
        "available": False,
        "phishing_suspected": False,
        "indicator_count": 0,
        "indicators": [],
        "matched_terms": [],
        "remarks": [],
        "errors": []
    }

    # -----------------------------------------
    # Input validation
    # -----------------------------------------

    if not isinstance(url, str) or not url.strip():

        result["remarks"].append(
            "Phishing detection skipped because no URL was provided."
        )

        return result

    url = url.strip()

    result["available"] = True

    # -----------------------------------------
    # Parse URL
    # -----------------------------------------

    try:

        parsed = urlparse(url)

        hostname = parsed.hostname

        if not hostname:

            result["errors"].append(
                "Hostname could not be determined."
            )

            return result

        hostname = hostname.lower()
        full_url = url.lower()

        # -----------------------------------------
        # Suspicious URL terms
        # -----------------------------------------

        for term in SUSPICIOUS_URL_TERMS:

            if term in full_url:

                result["matched_terms"].append(term)

        # -----------------------------------------
        # Multiple suspicious terms
        # -----------------------------------------

        if len(result["matched_terms"]) >= 2:

            result["indicators"].append(
                CYBER_INDICATOR_SUSPICIOUS_URL
            )

        # -----------------------------------------
        # Suspicious subdomain patterns
        # -----------------------------------------

        hostname_parts = hostname.split(".")

        if len(hostname_parts) > 3:

            subdomain = ".".join(
                hostname_parts[:-2]
            )

            for term in SUSPICIOUS_DOMAIN_TERMS:

                if term in subdomain:

                    result["indicators"].append(
                        CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN
                    )

                    break

        # -----------------------------------------
        # Hyphen-heavy domain detection
        # -----------------------------------------

        domain = ".".join(hostname_parts[-2:])

        if domain.count("-") >= 3:

            result["indicators"].append(
                CYBER_INDICATOR_SUSPICIOUS_URL
            )

        # -----------------------------------------
        # Numeric-heavy hostname
        # -----------------------------------------

        alphanumeric_characters = [
            character
            for character in hostname
            if character.isalnum()
        ]

        if alphanumeric_characters:

            digit_count = sum(
                character.isdigit()
                for character in alphanumeric_characters
            )

            digit_ratio = (
                digit_count
                / len(alphanumeric_characters)
            )

            if digit_ratio > 0.40:

                result["indicators"].append(
                    CYBER_INDICATOR_SUSPICIOUS_URL
                )

        # -----------------------------------------
        # Excessive special characters
        # -----------------------------------------

        special_character_count = len(
            re.findall(
                r"[@_%]",
                full_url
            )
        )

        if special_character_count >= 5:

            result["indicators"].append(
                CYBER_INDICATOR_SUSPICIOUS_URL
            )

        # -----------------------------------------
        # Remove duplicate indicators
        # -----------------------------------------

        result["indicators"] = list(
            dict.fromkeys(
                result["indicators"]
            )
        )

        result["indicator_count"] = len(
            result["indicators"]
        )

        # -----------------------------------------
        # Final phishing classification
        # -----------------------------------------

        if result["indicator_count"] >= 2:

            result["phishing_suspected"] = True

            result["remarks"].append(
                "Multiple suspicious URL characteristics "
                "were detected."
            )

        elif result["indicator_count"] == 1:

            result["remarks"].append(
                "A suspicious URL characteristic was detected, "
                "but this alone does not confirm phishing."
            )

        else:

            result["remarks"].append(
                "No major phishing URL patterns were detected."
            )

        return result

    # -----------------------------------------
    # Error handling
    # -----------------------------------------

    except ValueError as exc:

        result["errors"].append(
            f"URL parsing error: {str(exc)}"
        )

        return result

    except Exception as exc:

        result["errors"].append(
            f"Phishing detection failed: {str(exc)}"
        )

        return result