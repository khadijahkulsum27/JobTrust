from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_KEYWORD_DETECTOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    SUSPICIOUS_KEYWORDS
)


def detect_keywords(job_description):
    """
    Detects suspicious keywords and phrases in a job description.

    Parameters:
        job_description (str): Job description text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_KEYWORD_DETECTOR
    )

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if not isinstance(job_description, str):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description must be provided as text."
            )

            return result

        text = job_description.strip().lower()

        if not text:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # KEYWORD DETECTION
        # =================================================

        detected_keywords = []

        for keyword in SUSPICIOUS_KEYWORDS:

            normalized_keyword = keyword.lower().strip()

            if normalized_keyword in text:

                detected_keywords.append(
                    keyword
                )

        # Remove duplicates while preserving order
        detected_keywords = list(
            dict.fromkeys(
                detected_keywords
            )
        )

        keyword_count = len(
            detected_keywords
        )

        # =================================================
        # RISK CLASSIFICATION
        # =================================================

        if keyword_count == 0:

            risk = RISK_LOW

            result["remarks"].append(
                "No configured suspicious keywords were detected."
            )

        elif keyword_count <= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "A small number of suspicious keywords were detected."
            )

        else:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple suspicious keywords were detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "detected_keywords": detected_keywords,
            "keyword_count": keyword_count
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result