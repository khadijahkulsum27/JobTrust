import re
from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_SCAM_BEHAVIOR_DETECTOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def detect_scam_behavior(job_data):
    """
    Detects recruitment behaviors commonly associated
    with fraudulent or suspicious job postings.

    Parameters:
        job_data (dict): Job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_SCAM_BEHAVIOR_DETECTOR
    )

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if not isinstance(job_data, dict):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job data must be provided as a dictionary."
            )

            return result

        job_description = str(
            job_data.get(
                "job_description",
                ""
            )
        ).lower().strip()

        if not job_description:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # BEHAVIOR DETECTION
        # =================================================

        detected_behaviors = []

        # -------------------------------------------------
        # Payment request
        # -------------------------------------------------

        payment_request = any(
            phrase in job_description
            for phrase in [
                "registration fee",
                "processing fee",
                "application fee",
                "joining fee",
                "security deposit",
                "training fee",
                "pay a fee",
                "pay fee",
                "send money"
            ]
        )

        if payment_request:

            detected_behaviors.append(
                "Payment or fee requirement"
            )

        # -------------------------------------------------
        # Guaranteed employment
        # -------------------------------------------------

        guaranteed_employment = any(
            phrase in job_description
            for phrase in [
                "guaranteed job",
                "guaranteed employment",
                "100% placement",
                "100% selection",
                "guaranteed selection",
                "job guaranteed"
            ]
        )

        if guaranteed_employment:

            detected_behaviors.append(
                "Guaranteed employment claim"
            )

        # -------------------------------------------------
        # No interview / instant selection
        # -------------------------------------------------

        no_interview = any(
            phrase in job_description
            for phrase in [
                "no interview",
                "without interview",
                "no interview required",
                "direct selection",
                "instant selection"
            ]
        )

        if no_interview:

            detected_behaviors.append(
                "No-interview or instant-selection claim"
            )

        # -------------------------------------------------
        # Personal information request
        # -------------------------------------------------

        sensitive_information_request = any(
            re.search(r"\b" + re.escape(phrase) + r"\b", job_description)
            for phrase in [
                "send your aadhaar",
                "send aadhaar",
                "send your pan",
                "send pan card",
                "bank account details",
                "bank details",
                "credit card details",
                "otp",
                "one time password"
            ]
        )
        if sensitive_information_request:

            detected_behaviors.append(
                "Request for sensitive personal information"
            )

        # -------------------------------------------------
        # Messaging-platform recruitment
        # -------------------------------------------------

        messaging_recruitment = any(
            platform in job_description
            for platform in [
                "whatsapp",
                "telegram",
                "signal"
            ]
        )

        if messaging_recruitment:

            detected_behaviors.append(
                "Messaging-platform recruitment"
            )

        # -------------------------------------------------
        # Pressure tactics
        # -------------------------------------------------

        pressure_tactics = any(
            phrase in job_description
            for phrase in [
                "apply now",
                "hurry",
                "last chance",
                "only today",
                "act immediately",
                "limited vacancies",
                "join immediately"
            ]
        )

        if pressure_tactics:

            detected_behaviors.append(
                "Pressure or urgency tactics"
            )

        # -------------------------------------------------
        # Unrealistic income
        # -------------------------------------------------

        unrealistic_income = any(
            phrase in job_description
            for phrase in [
                "earn money fast",
                "easy money",
                "guaranteed income",
                "earn thousands daily",
                "earn lakhs",
                "high income with no experience"
            ]
        )

        if unrealistic_income:

            detected_behaviors.append(
                "Unrealistic income claim"
            )

        # =================================================
        # BEHAVIOR COUNT
        # =================================================

        behavior_count = len(
            detected_behaviors
        )

        # =================================================
        # RISK ASSESSMENT
        # =================================================

        # Payment + sensitive information is particularly
        # concerning and receives the highest risk.

        if (
            payment_request
            and sensitive_information_request
        ):

            risk = RISK_HIGH

            result["remarks"].append(
                "Payment requirements and sensitive-information requests "
                "were detected together."
            )

        elif behavior_count >= 4:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple suspicious recruitment behaviors were detected."
            )

        elif behavior_count >= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Several suspicious recruitment behaviors were detected."
            )

        elif behavior_count == 1:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "A suspicious recruitment behavior was detected."
            )

        else:

            risk = RISK_LOW

            result["remarks"].append(
                "No major suspicious recruitment behavior was detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "detected_behaviors": detected_behaviors,
            "behavior_count": behavior_count,
            "payment_request": payment_request,
            "guaranteed_employment": guaranteed_employment,
            "no_interview": no_interview,
            "sensitive_information_request": (
                sensitive_information_request
            ),
            "messaging_recruitment": messaging_recruitment,
            "pressure_tactics": pressure_tactics,
            "unrealistic_income": unrealistic_income
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result