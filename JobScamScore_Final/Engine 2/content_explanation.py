from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_CONTENT_EXPLANATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)


def generate_content_explanation(
    keyword_result,
    salary_result,
    grammar_result,
    urgency_result,
    contact_result,
    score_result
):
    """
    Generates a human-readable explanation of the
    Engine 2 job-content analysis.

    Parameters:
        keyword_result (dict)
        salary_result (dict)
        grammar_result (dict)
        urgency_result (dict)
        contact_result (dict)
        score_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_CONTENT_EXPLANATION
    )

    try:

        # =================================================
        # COLLECT ANALYSIS FINDINGS
        # =================================================

        report = []

        report.extend(
            keyword_result.get("remarks", [])
        )

        report.extend(
            salary_result.get("remarks", [])
        )

        report.extend(
            grammar_result.get("remarks", [])
        )

        report.extend(
            urgency_result.get("remarks", [])
        )

        report.extend(
            contact_result.get("remarks", [])
        )

        # =================================================
        # FINAL SCORE INFORMATION
        # =================================================

        score = score_result["score"]
        risk = score_result["risk"]

        report.append(
            f"Overall Content Trust Score: {score}/100."
        )

        report.append(
            f"Overall Content Risk Level: {risk}."
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["score"] = score
        result["risk"] = risk

        result["data"] = {
            "report": report
        }

        result["remarks"].append(
            "Content explanation generated successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result