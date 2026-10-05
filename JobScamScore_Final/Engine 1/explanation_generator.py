from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_EXPLANATION_GENERATOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)


def generate_explanation(
    website_result,
    ssl_result,
    email_result,
    whois_result,
    domain_result,
    mca_result,
    score_result
):
    """
    Generates a human-readable explanation report.

    Parameters:
        website_result (dict)
        ssl_result (dict)
        email_result (dict)
        whois_result (dict)
        domain_result (dict)
        score_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_EXPLANATION_GENERATOR
    )

    try:

        report = []

        report.extend(website_result["remarks"])
        report.extend(ssl_result["remarks"])
        report.extend(email_result["remarks"])
        report.extend(whois_result["remarks"])
        report.extend(domain_result["remarks"])
        report.extend(mca_result["remarks"])

        report.append(
            f"Overall Identity Score: {score_result['score']}/100."
        )
        report.append(
              "MCA company verification included in identity assessment."
        )

        report.append(
            f"Overall Risk Level: {score_result['risk']}."
        )

        result["status"] = STATUS_SUCCESS
        result["score"] = score_result["score"]
        result["risk"] = score_result["risk"]

        result["data"] = {
            "report": report
        }

        result["remarks"].append(
            "Explanation report generated successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result