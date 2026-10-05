"""
Engine 4 - URL Analyzer

Analyzes the structure of a website URL and identifies
potentially suspicious URL characteristics.
"""

import ipaddress
from urllib.parse import urlparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import (
    MAX_URL_LENGTH,
    MAX_SUBDOMAIN_COUNT,
    CYBER_INDICATOR_IP_ADDRESS,
    CYBER_INDICATOR_LONG_URL,
    CYBER_INDICATOR_HTTP_ONLY,
    CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN,
    CYBER_INDICATOR_SUSPICIOUS_ENCODING,
)


def analyze_url(url):
    """
    Analyze a website URL.

    Args:
        url (str): Website URL.

    Returns:
        dict: URL analysis result.
    """

    result = {
        "available": False,
        "valid": False,
        "scheme": None,
        "hostname": None,
        "domain": None,
        "is_https": False,
        "is_ip_address": False,
        "url_length": 0,
        "subdomain_count": 0,
        "indicators": [],
        "remarks": [],
        "errors": []
    }

    # -----------------------------------------
    # Input validation
    # -----------------------------------------

    if not isinstance(url, str) or not url.strip():
        result["remarks"].append(
            "No website URL was provided."
        )
        return result

    url = url.strip()

    result["available"] = True
    result["url_length"] = len(url)

    # -----------------------------------------
    # Parse URL
    # -----------------------------------------

    try:
        parsed = urlparse(url)

        if not parsed.scheme or not parsed.netloc:
            result["remarks"].append(
                "Invalid URL format."
            )
            return result

        hostname = parsed.hostname

        if not hostname:
            result["remarks"].append(
                "Hostname could not be determined."
            )
            return result

        hostname = hostname.lower()

        result["valid"] = True
        result["scheme"] = parsed.scheme.lower()
        result["hostname"] = hostname
        result["is_https"] = parsed.scheme.lower() == "https"

        # -----------------------------------------
        # IP address detection
        # -----------------------------------------

        try:
            ipaddress.ip_address(hostname)

            result["is_ip_address"] = True

            result["indicators"].append(
                CYBER_INDICATOR_IP_ADDRESS
            )

        except ValueError:
            # Hostname is not an IP address.
            pass

        # -----------------------------------------
        # Domain extraction
        # -----------------------------------------

        if not result["is_ip_address"]:
            hostname_parts = hostname.split(".")

            if len(hostname_parts) >= 2:
                result["domain"] = ".".join(
                    hostname_parts[-2:]
                )

                result["subdomain_count"] = max(
                    0,
                    len(hostname_parts) - 2
                )

        # -----------------------------------------
        # HTTPS / HTTP check
        # -----------------------------------------

        if parsed.scheme.lower() == "http":

            result["indicators"].append(
                CYBER_INDICATOR_HTTP_ONLY
            )

        # -----------------------------------------
        # URL length
        # -----------------------------------------

        if result["url_length"] > MAX_URL_LENGTH:

            result["indicators"].append(
                CYBER_INDICATOR_LONG_URL
            )

        # -----------------------------------------
        # Subdomain analysis
        # -----------------------------------------

        if (
            result["subdomain_count"]
            > MAX_SUBDOMAIN_COUNT
        ):

            result["indicators"].append(
                CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN
            )

        # -----------------------------------------
        # Suspicious URL encoding
        # -----------------------------------------

        suspicious_encoding_patterns = [
            "%40",
            "%2f",
            "%3f",
            "%3d",
            "%26"
        ]

        lower_url = url.lower()

        if any(
            pattern in lower_url
            for pattern in suspicious_encoding_patterns
        ):

            result["indicators"].append(
                CYBER_INDICATOR_SUSPICIOUS_ENCODING
            )

        # -----------------------------------------
        # Completion
        # -----------------------------------------

        result["remarks"].append(
            "URL analysis completed successfully."
        )

        return result

    except ValueError as exc:

        result["errors"].append(
            f"URL parsing error: {str(exc)}"
        )

        return result

    except Exception as exc:

        result["errors"].append(
            f"URL analysis failed: {str(exc)}"
        )

        return result