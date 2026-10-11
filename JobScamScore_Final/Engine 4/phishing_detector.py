"""
Engine 4 - Phishing Detector

Detects common suspicious patterns in website URLs
that may indicate phishing or deceptive websites.
"""

import os
import re
from urllib.parse import urlparse

import requests

from utils.constants import (
    CYBER_INDICATOR_SUSPICIOUS_URL,
    CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN,
    CYBER_INDICATOR_THREAT_DETECTED,
    CYBER_INDICATOR_RISKY_DOMAIN,
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
def check_safe_browsing(url):
    """Asks Google Safe Browsing if the URL is listed as unsafe. Never crashes."""

    unavailable = {"available": False, "threat_found": False, "threat_types": []}

    key = os.environ.get("GOOGLE_SAFE_BROWSING_KEY")

    if not key:
        return unavailable

    body = {
        "client": {"clientId": "jobtrust", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(
            "https://safebrowsing.googleapis.com/v4/threatMatches:find",
            params={"key": key},
            json=body,
            timeout=5,
        )

        if response.status_code != 200:
            return unavailable

        matches = response.json().get("matches", [])

        return {
            "available": True,
            "threat_found": bool(matches),
            "threat_types": sorted({m.get("threatType") for m in matches}),
        }

    except Exception:
        return unavailable

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

        # Endings like ".co.in" count as one part, so the main domain is 3 parts long.
        if (
            len(hostname_parts) >= 3
            and len(hostname_parts[-1]) == 2
            and hostname_parts[-2] in ("co", "com", "org", "net", "gov", "ac", "edu", "nic", "res", "ltd", "plc")
        ):
            main_length = 3
        else:
            main_length = 2

        if len(hostname_parts) > main_length + 1:

            subdomain = ".".join(
                hostname_parts[:-main_length]
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

        domain = ".".join(hostname_parts[-main_length:])

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
        # Google Safe Browsing (extra evidence; skipped quietly if unavailable)
        # -----------------------------------------

        safe_browsing = check_safe_browsing(url)
        result["safe_browsing"] = safe_browsing

        if safe_browsing["threat_found"]:
            # A Google listing is strong evidence, so it counts as two indicators.
            result["indicators"].append(CYBER_INDICATOR_THREAT_DETECTED)
            result["indicators"].append(CYBER_INDICATOR_RISKY_DOMAIN)
            result["remarks"].append(
                "Google Safe Browsing lists this website as unsafe."
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