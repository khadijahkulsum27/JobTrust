"""
Engine 4 - HTTPS Checker

Checks whether a website uses HTTPS and whether
its TLS/SSL certificate can be validated.
"""

import requests

from utils.constants import (
    HTTP_TIMEOUT,
    CHECK_AVAILABLE,
    CHECK_ERROR,
    CHECK_SKIPPED,
    CYBER_POSITIVE_HTTPS,
    CYBER_INDICATOR_HTTP_ONLY,
    CYBER_INDICATOR_INVALID_CERTIFICATE,
)


def check_https(url):
    """
    Check HTTPS availability and certificate validity.

    Args:
        url (str): Website URL.

    Returns:
        dict: HTTPS check result.
    """

    result = {
        "status": CHECK_SKIPPED,
        "https": False,
        "certificate_valid": False,
        "final_url": None,
        "indicators": [],
        "positive_indicators": [],
        "remarks": [],
        "errors": []
    }

    # -----------------------------------------
    # Input validation
    # -----------------------------------------

    if not isinstance(url, str) or not url.strip():
        result["remarks"].append(
            "HTTPS check skipped because no URL was provided."
        )
        return result

    url = url.strip()

    # -----------------------------------------
    # HTTP websites
    # -----------------------------------------

    if url.lower().startswith("http://"):

        result["status"] = CHECK_AVAILABLE

        result["indicators"].append(
            CYBER_INDICATOR_HTTP_ONLY
        )

        result["remarks"].append(
            "Website is using HTTP instead of HTTPS."
        )

        return result

    # -----------------------------------------
    # HTTPS websites
    # -----------------------------------------

    if not url.lower().startswith("https://"):

        result["status"] = CHECK_SKIPPED

        result["remarks"].append(
            "URL does not use HTTP or HTTPS."
        )

        return result

    # -----------------------------------------
    # HTTPS request
    # -----------------------------------------

    try:

        response = requests.get(
            url,
            timeout=HTTP_TIMEOUT,
            verify=True,
            allow_redirects=True
        )

        result["status"] = CHECK_AVAILABLE
        result["https"] = True
        result["certificate_valid"] = True
        result["final_url"] = response.url

        result["positive_indicators"].append(
            CYBER_POSITIVE_HTTPS
        )

        result["remarks"].append(
            "HTTPS connection and TLS certificate "
            "validation completed successfully."
        )

        return result

    # -----------------------------------------
    # Invalid SSL certificate
    # -----------------------------------------

    except requests.exceptions.SSLError as exc:

        result["status"] = CHECK_ERROR
        result["https"] = True
        result["certificate_valid"] = False

        result["indicators"].append(
            CYBER_INDICATOR_INVALID_CERTIFICATE
        )

        result["errors"].append(
            f"SSL certificate validation failed: {str(exc)}"
        )

        result["remarks"].append(
            "The website uses HTTPS, but its certificate "
            "could not be validated."
        )

        return result

    # -----------------------------------------
    # Timeout
    # -----------------------------------------

    except requests.exceptions.Timeout:

        result["status"] = CHECK_ERROR
        result["https"] = True

        result["errors"].append(
            "HTTPS connection timed out."
        )

        result["remarks"].append(
            "The website did not respond within the "
            "configured timeout period."
        )

        return result

    # -----------------------------------------
    # Connection error
    # -----------------------------------------

    except requests.exceptions.ConnectionError as exc:

        result["status"] = CHECK_ERROR
        result["https"] = True

        result["errors"].append(
            f"HTTPS connection failed: {str(exc)}"
        )

        result["remarks"].append(
            "Could not establish a connection with the website."
        )

        return result

    # -----------------------------------------
    # Other request errors
    # -----------------------------------------

    except requests.exceptions.RequestException as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"HTTPS request failed: {str(exc)}"
        )

        return result

    # -----------------------------------------
    # Unexpected error
    # -----------------------------------------

    except Exception as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"HTTPS check failed: {str(exc)}"
        )

        return result