"""
Engine 4 - Cyber Risk Scorer

Combines the results from the Engine 4 security checks
and produces a normalized cyber-risk score from 0 to 100.

0   = Lowest cyber risk
100 = Highest cyber risk
"""

from utils.constants import (
    CYBER_URL_SCORE,
    CYBER_HTTPS_SCORE,
    CYBER_RDAP_SCORE,
    CYBER_PHISHING_SCORE,
    CYBER_THREAT_INTELLIGENCE_SCORE,
    CYBER_RISK_LOW,
    CYBER_RISK_MEDIUM,
    CYBER_RISK_HIGH,
)


def _calculate_url_risk(url_result):
    """
    Calculate the URL component risk.
    """

    if not url_result.get("valid", False):
        return 50

    indicators = url_result.get("indicators", [])

    risk = 0

    # Each suspicious URL characteristic contributes
    # a limited amount to the component risk.
    risk += min(len(indicators) * 25, 100)

    return min(risk, 100)


def _calculate_https_risk(https_result):
    """
    Calculate the HTTPS component risk.
    """

    if not https_result:
        return 50

    if https_result.get("status") == "SKIPPED":
        return 50

    if (
        https_result.get("https")
        and https_result.get("certificate_valid")
    ):
        return 0

    if (
        https_result.get("https")
        and not https_result.get("certificate_valid")
    ):
        return 100

    return 75


def _calculate_rdap_risk(rdap_result):
    """
    Calculate domain-registration component risk.
    """

    if not rdap_result:
        return 50

    if not rdap_result.get("registered", False):
        return 60

    age_category = rdap_result.get(
        "domain_age_category",
        "UNKNOWN"
    )

    if age_category == "RECENT":
        return 75

    if age_category == "MODERATE":
        return 25

    if age_category == "ESTABLISHED":
        return 0

    return 50


def _calculate_phishing_risk(phishing_result):
    """
    Calculate phishing-pattern component risk.
    """

    if not phishing_result:
        return 50

    if not phishing_result.get("available", False):
        return 50

    indicator_count = phishing_result.get(
        "indicator_count",
        0
    )

    if indicator_count >= 2:
        return 100

    if indicator_count == 1:
        return 50

    return 0


def _calculate_threat_intelligence_risk(
    threat_result
):
    """
    Calculate threat-intelligence component risk.
    """

    if not threat_result:
        return 50

    if not threat_result.get("available", False):
        return 50

    if threat_result.get("threat_detected", False):

        malicious = threat_result.get(
            "malicious",
            0
        )

        suspicious = threat_result.get(
            "suspicious",
            0
        )

        # Malicious detections are stronger evidence
        # than suspicious detections.
        if malicious > 0:
            return 100

        if suspicious > 0:
            return 75

        return 60

    return 0


def calculate_cyber_risk(
    url_result,
    https_result,
    rdap_result,
    phishing_result,
    threat_result
):
    """
    Calculate the final Engine 4 cyber-risk score.

    Args:
        url_result (dict): URL analyzer result.
        https_result (dict): HTTPS checker result.
        rdap_result (dict): RDAP checker result.
        phishing_result (dict): Phishing detector result.
        threat_result (dict): Threat intelligence result.

    Returns:
        dict: Cyber risk score and component scores.
    """

    # -----------------------------------------
    # Component risks
    # -----------------------------------------

    url_risk = _calculate_url_risk(
        url_result
    )

    https_risk = _calculate_https_risk(
        https_result
    )

    rdap_risk = _calculate_rdap_risk(
        rdap_result
    )

    phishing_risk = _calculate_phishing_risk(
        phishing_result
    )

    threat_risk = _calculate_threat_intelligence_risk(
        threat_result
    )

    # -----------------------------------------
    # Weighted score
    # -----------------------------------------

    weighted_score = (
        (url_risk * CYBER_URL_SCORE)
        + (https_risk * CYBER_HTTPS_SCORE)
        + (rdap_risk * CYBER_RDAP_SCORE)
        + (phishing_risk * CYBER_PHISHING_SCORE)
        + (
            threat_risk
            * CYBER_THREAT_INTELLIGENCE_SCORE
        )
    ) / 100

    score = round(
        max(0, min(weighted_score, 100))
    )

    # -----------------------------------------
    # Risk classification
    # -----------------------------------------

    if score <= CYBER_RISK_LOW:

        risk = "LOW"

    elif score <= CYBER_RISK_MEDIUM:

        risk = "MEDIUM"

    else:

        risk = "HIGH"

    # -----------------------------------------
    # Component results
    # -----------------------------------------

    components = {
        "url_risk": url_risk,
        "https_risk": https_risk,
        "rdap_risk": rdap_risk,
        "phishing_risk": phishing_risk,
        "threat_intelligence_risk": threat_risk
    }

    return {
        "score": score,
        "risk": risk,
        "components": components
    }