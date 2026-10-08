
from utils.response_builder import create_engine_response
from utils.constants import (
    ENGINE_IDENTITY_SCORING,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    WEBSITE_SCORE,
    SSL_SCORE,
    EMAIL_SCORE,
    WHOIS_SCORE,
    DOMAIN_MATCH_SCORE,
    MCA_SCORE,
    TRUST_HIGH,
    TRUST_MEDIUM
)
def _points(check_result, full_points):
    """Full points for LOW risk, half for MEDIUM, none for HIGH or a failed check."""

    if check_result.get("status") != STATUS_SUCCESS:
        return 0

    risk = check_result.get("risk")

    if risk == RISK_LOW:
        return full_points

    if risk == RISK_MEDIUM:
        return full_points // 2

    return 0

def calculate_identity_score(
    website_result,
    ssl_result,
    email_result,
    whois_result,
    domain_result,
    mca_result
):
    """
    Calculates the overall identity trust score.

    Parameters:
        website_result (dict)
        ssl_result (dict)
        email_result (dict)
        whois_result (dict)
        domain_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_IDENTITY_SCORING
    )

    try:

        
        score = 0

        score += _points(website_result, WEBSITE_SCORE)
        score += _points(ssl_result, SSL_SCORE)
        score += _points(email_result, EMAIL_SCORE)
        score += _points(whois_result, WHOIS_SCORE)

        # Domain matching: full points only if the domains match
        if domain_result.get("status") == STATUS_SUCCESS:
            if domain_result.get("data", {}).get("domain_match"):
                score += DOMAIN_MATCH_SCORE

        # MCA verification: full points only if the company was found
        if mca_result.get("status") == STATUS_SUCCESS:
            if mca_result.get("data", {}).get("registered"):
                score += MCA_SCORE
        # Determine Risk Level
        if score >= TRUST_HIGH:
            risk = RISK_LOW

        elif score >= TRUST_MEDIUM:
            risk = RISK_MEDIUM

        else:
            risk = RISK_HIGH

        result["status"] = STATUS_SUCCESS
        result["score"] = score
        result["risk"] = risk

        result["data"] = {
            "identity_score": score,
            "mca_verified": mca_result.get("data", {}).get("registered", False)
}
        

        result["remarks"].append(
        f"Overall identity score including MCA verification calculated: {score}/100."
)
        

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result