
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

        # Website Verification
        if website_result["status"] == STATUS_SUCCESS:
            score += WEBSITE_SCORE

        # SSL Verification
        if ssl_result["status"] == STATUS_SUCCESS:
            score += SSL_SCORE

        # Email Verification
        if email_result["status"] == STATUS_SUCCESS:
            score += EMAIL_SCORE

        # WHOIS Verification
        if whois_result["status"] == STATUS_SUCCESS:
            score += WHOIS_SCORE

        # Domain Matching
        if domain_result["status"] == STATUS_SUCCESS:
            if domain_result["data"]["domain_match"]:
                score += DOMAIN_MATCH_SCORE
        # MCA Verification
        if mca_result["status"] == STATUS_SUCCESS:
            if mca_result["data"]["registered"]:
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
            "mca_verified": mca_result["data"]["registered"]
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