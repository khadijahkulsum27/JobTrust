from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_URGENCY_DETECTOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    URGENCY_PHRASES
)


def detect_urgency(job_description):
    """
    Detects urgency-based phrases commonly associated
    with suspicious job postings.

    Parameters:
        job_description (str): Job description text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_URGENCY_DETECTOR
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
        # URGENCY PHRASE DETECTION
        # =================================================

        detected_phrases = []

        for phrase in URGENCY_PHRASES:

            normalized_phrase = (
                phrase.lower().strip()
            )

            if normalized_phrase in text:

                detected_phrases.append(
                    phrase
                )

        # Remove duplicates while preserving order
        detected_phrases = list(
            dict.fromkeys(
                detected_phrases
            )
        )

        phrase_count = len(
            detected_phrases
        )

        # =================================================
        # RISK CLASSIFICATION
        # =================================================

        if phrase_count == 0:

            risk = RISK_LOW

            result["remarks"].append(
                "No suspicious urgency phrases detected."
            )

        elif phrase_count <= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Some urgency-based phrases were detected."
            )

        else:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple urgency-based phrases were detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "detected_phrases": detected_phrases,
            "phrase_count": phrase_count
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result