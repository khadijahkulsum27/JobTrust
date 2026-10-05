from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_CONTENT_SCORER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    KEYWORD_SCORE,
    SALARY_SCORE,
    GRAMMAR_SCORE,
    URGENCY_SCORE,
    CONTACT_SCORE,
    CONTENT_TRUST_HIGH,
    CONTENT_TRUST_MEDIUM
)


def calculate_content_score(
    keyword_result,
    salary_result,
    grammar_result,
    urgency_result,
    contact_result
):
    """
    Calculates the overall trust score of the job content.

    Each analysis contributes up to 20 points,
    giving a maximum possible score of 100.

    Parameters:
        keyword_result (dict)
        salary_result (dict)
        grammar_result (dict)
        urgency_result (dict)
        contact_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_CONTENT_SCORER
    )

    try:

        score = 0

        # =================================================
        # KEYWORD ANALYSIS
        # =================================================

        if keyword_result["status"] == STATUS_SUCCESS:

            if keyword_result["risk"] == RISK_LOW:

                score += KEYWORD_SCORE

            elif keyword_result["risk"] == RISK_MEDIUM:

                score += KEYWORD_SCORE // 2

        # =================================================
        # SALARY ANALYSIS
        # =================================================

        if salary_result["status"] == STATUS_SUCCESS:

            if salary_result["risk"] == RISK_LOW:

                score += SALARY_SCORE

            elif salary_result["risk"] == RISK_MEDIUM:

                score += SALARY_SCORE // 2

        # =================================================
        # GRAMMAR ANALYSIS
        # =================================================

        if grammar_result["status"] == STATUS_SUCCESS:

            if grammar_result["risk"] == RISK_LOW:

                score += GRAMMAR_SCORE

            elif grammar_result["risk"] == RISK_MEDIUM:

                score += GRAMMAR_SCORE // 2

        # =================================================
        # URGENCY ANALYSIS
        # =================================================

        if urgency_result["status"] == STATUS_SUCCESS:

            if urgency_result["risk"] == RISK_LOW:

                score += URGENCY_SCORE

            elif urgency_result["risk"] == RISK_MEDIUM:

                score += URGENCY_SCORE // 2

        # =================================================
        # CONTACT ANALYSIS
        # =================================================

        if contact_result["status"] == STATUS_SUCCESS:

            if contact_result["risk"] == RISK_LOW:

                score += CONTACT_SCORE

            elif contact_result["risk"] == RISK_MEDIUM:

                score += CONTACT_SCORE // 2

        # =================================================
        # RISK CLASSIFICATION
        # =================================================

        if score >= CONTENT_TRUST_HIGH:

            risk = RISK_LOW

        elif score >= CONTENT_TRUST_MEDIUM:

            risk = RISK_MEDIUM

        else:

            risk = RISK_HIGH

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["score"] = score
        result["risk"] = risk

        result["data"] = {
            "content_score": score
        }

        result["remarks"].append(
            f"Overall content trust score calculated: "
            f"{score}/100."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result