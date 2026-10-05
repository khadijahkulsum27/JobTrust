"""
Engine 4 - Threat Intelligence

Uses VirusTotal URL intelligence when an API key is available.
The module fails gracefully when the service is unavailable
or no API key has been configured.
"""

import base64
import os

import requests

from utils.constants import (
    VIRUSTOTAL_API_URL,
    VIRUSTOTAL_URL_ENDPOINT,
    VIRUSTOTAL_TIMEOUT,
    CHECK_AVAILABLE,
    CHECK_UNAVAILABLE,
    CHECK_ERROR,
    CHECK_SKIPPED,
    CYBER_INDICATOR_THREAT_DETECTED,
    CYBER_POSITIVE_CLEAN_THREAT_CHECK,
)


def _create_url_id(url):
    """
    Create the URL identifier required by the
    VirusTotal URL report endpoint.
    """

    encoded_url = base64.urlsafe_b64encode(
        url.encode()
    ).decode()

    return encoded_url.rstrip("=")


def check_threat_intelligence(url):
    """
    Check a URL against VirusTotal threat intelligence.

    Args:
        url (str): Website URL.

    Returns:
        dict: Threat intelligence result.
    """

    result = {
        "status": CHECK_SKIPPED,
        "available": False,
        "threat_detected": False,
        "malicious": 0,
        "suspicious": 0,
        "harmless": 0,
        "undetected": 0,
        "reputation": None,
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
            "Threat intelligence check skipped because "
            "no URL was provided."
        )

        return result

    url = url.strip()

    # -----------------------------------------
    # API key
    # -----------------------------------------

    api_key = os.getenv(
        "VIRUSTOTAL_API_KEY"
    )

    if not api_key:

        result["status"] = CHECK_UNAVAILABLE

        result["remarks"].append(
            "VirusTotal API key is not configured. "
            "Threat intelligence check was skipped."
        )

        return result

    # -----------------------------------------
    # Create VirusTotal URL
    # -----------------------------------------

    try:

        url_id = _create_url_id(url)

        endpoint = (
            VIRUSTOTAL_API_URL
            + VIRUSTOTAL_URL_ENDPOINT
            + "/"
            + url_id
        )

        headers = {
            "x-apikey": api_key,
            "Accept": "application/json"
        }

        # -----------------------------------------
        # Request URL report
        # -----------------------------------------

        response = requests.get(
            endpoint,
            headers=headers,
            timeout=VIRUSTOTAL_TIMEOUT
        )

        # -----------------------------------------
        # Rate limit
        # -----------------------------------------

        if response.status_code == 429:

            result["status"] = CHECK_UNAVAILABLE

            result["remarks"].append(
                "VirusTotal rate limit was reached."
            )

            return result

        # -----------------------------------------
        # Not previously analyzed
        # -----------------------------------------

        if response.status_code == 404:

            result["status"] = CHECK_AVAILABLE
            result["available"] = True

            result["remarks"].append(
                "No existing VirusTotal URL report was found."
            )

            return result

        response.raise_for_status()

        data = response.json()

        result["status"] = CHECK_AVAILABLE
        result["available"] = True

        # -----------------------------------------
        # Extract analysis statistics
        # -----------------------------------------

        attributes = (
            data.get("data", {})
                .get("attributes", {})
        )

        stats = attributes.get(
            "last_analysis_stats",
            {}
        )

        result["malicious"] = int(
            stats.get("malicious", 0) or 0
        )

        result["suspicious"] = int(
            stats.get("suspicious", 0) or 0
        )

        result["harmless"] = int(
            stats.get("harmless", 0) or 0
        )

        result["undetected"] = int(
            stats.get("undetected", 0) or 0
        )

        result["reputation"] = attributes.get(
            "reputation"
        )

        # -----------------------------------------
        # Threat classification
        # -----------------------------------------

        if (
            result["malicious"] > 0
            or result["suspicious"] > 0
        ):

            result["threat_detected"] = True

            result["indicators"].append(
                CYBER_INDICATOR_THREAT_DETECTED
            )

            result["remarks"].append(
                "VirusTotal reported suspicious or "
                "malicious detections for the URL."
            )

        else:

            result["positive_indicators"].append(
                CYBER_POSITIVE_CLEAN_THREAT_CHECK
            )

            result["remarks"].append(
                "VirusTotal did not report malicious or "
                "suspicious detections in the available report."
            )

        return result

    # -----------------------------------------
    # Timeout
    # -----------------------------------------

    except requests.exceptions.Timeout:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            "VirusTotal request timed out."
        )

        return result

    # -----------------------------------------
    # Connection error
    # -----------------------------------------

    except requests.exceptions.ConnectionError as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"VirusTotal connection failed: {str(exc)}"
        )

        return result

    # -----------------------------------------
    # HTTP/request error
    # -----------------------------------------

    except requests.exceptions.RequestException as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"VirusTotal request failed: {str(exc)}"
        )

        return result

    # -----------------------------------------
    # Invalid JSON
    # -----------------------------------------

    except ValueError as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"Invalid VirusTotal response: {str(exc)}"
        )

        return result

    # -----------------------------------------
    # Unexpected error
    # -----------------------------------------

    except Exception as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"Threat intelligence check failed: {str(exc)}"
        )

        return result