"""
Engine 4 - Cyber Threat Explanation

Generates human-readable explanations for the
cyber-risk findings produced by Engine 4.
"""


def generate_cyber_explanation(
    url_result,
    https_result,
    rdap_result,
    phishing_result,
    threat_result,
    score,
    risk
):
    """
    Generate an explainable summary of Engine 4 findings.

    Args:
        url_result (dict): URL analyzer result.
        https_result (dict): HTTPS checker result.
        rdap_result (dict): RDAP checker result.
        phishing_result (dict): Phishing detector result.
        threat_result (dict): Threat intelligence result.
        score (int): Final cyber-risk score.
        risk (str): Final cyber-risk classification.

    Returns:
        dict: Explanation and supporting findings.
    """

    explanations = []
    positive_findings = []
    risk_findings = []

    # -----------------------------------------
    # URL analysis
    # -----------------------------------------

    url_indicators = url_result.get(
        "indicators",
        []
    )

    if url_indicators:

        risk_findings.append(
            "The website URL contains one or more "
            "potentially suspicious characteristics."
        )

    else:

        positive_findings.append(
            "No major structural URL warning "
            "indicators were detected."
        )

    # -----------------------------------------
    # HTTPS analysis
    # -----------------------------------------

    if (
        https_result.get("https")
        and https_result.get("certificate_valid")
    ):

        positive_findings.append(
            "The website uses HTTPS with a "
            "successfully validated certificate."
        )

    elif (
        https_result.get("https")
        and not https_result.get("certificate_valid")
    ):

        risk_findings.append(
            "The website uses HTTPS, but its "
            "certificate could not be validated."
        )

    else:

        risk_findings.append(
            "The website does not provide a "
            "validated HTTPS connection."
        )

    # -----------------------------------------
    # RDAP analysis
    # -----------------------------------------

    domain_age_category = rdap_result.get(
        "domain_age_category",
        "UNKNOWN"
    )

    if domain_age_category == "RECENT":

        risk_findings.append(
            "The domain appears to have been "
            "registered recently."
        )

    elif domain_age_category == "ESTABLISHED":

        positive_findings.append(
            "The domain appears to be established "
            "based on its registration age."
        )

    elif domain_age_category == "MODERATE":

        positive_findings.append(
            "The domain has a moderate registration age."
        )

    else:

        explanations.append(
            "Domain registration age could not "
            "be confidently determined."
        )

    # -----------------------------------------
    # Phishing analysis
    # -----------------------------------------

    if phishing_result.get(
        "phishing_suspected",
        False
    ):

        risk_findings.append(
            "Multiple URL characteristics associated "
            "with phishing patterns were detected."
        )

    elif phishing_result.get(
        "indicator_count",
        0
    ) == 1:

        explanations.append(
            "One suspicious URL characteristic was "
            "detected, but this alone does not "
            "confirm phishing."
        )

    else:

        positive_findings.append(
            "No major phishing URL patterns were detected."
        )

    # -----------------------------------------
    # Threat intelligence
    # -----------------------------------------

    if threat_result.get(
        "threat_detected",
        False
    ):

        risk_findings.append(
            "Threat-intelligence analysis reported "
            "suspicious or malicious detections."
        )

    elif threat_result.get(
        "available",
        False
    ):

        positive_findings.append(
            "Available threat-intelligence data did "
            "not report malicious or suspicious detections."
        )

    else:

        explanations.append(
            "External threat-intelligence information "
            "was unavailable, so this factor was treated "
            "as unknown rather than automatically risky."
        )

    # -----------------------------------------
    # Overall explanation
    # -----------------------------------------

    if risk == "LOW":

        overall = (
            f"Engine 4 calculated a cyber-risk score "
            f"of {score}/100. The available evidence "
            f"indicates a relatively low cyber risk."
        )

    elif risk == "MEDIUM":

        overall = (
            f"Engine 4 calculated a cyber-risk score "
            f"of {score}/100. Some cyber-risk indicators "
            f"were identified and should be reviewed."
        )

    else:

        overall = (
            f"Engine 4 calculated a cyber-risk score "
            f"of {score}/100. Multiple cyber-risk "
            f"indicators require attention."
        )

    explanations.insert(
        0,
        overall
    )

    # -----------------------------------------
    # Return explanation
    # -----------------------------------------

    return {
        "summary": overall,
        "explanations": explanations,
        "risk_findings": risk_findings,
        "positive_findings": positive_findings
    }