from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_PATTERN_DETECTOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def detect_patterns(job_data):
    """
    Detects combinations of suspicious signals in a job posting.

    Parameters:
        job_data (dict): Complete job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_PATTERN_DETECTOR
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

        # =================================================
        # EXTRACT JOB CONTENT
        # =================================================

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
        # SIGNAL DETECTION
        # =================================================

        registration_fee = any(
            phrase in job_description
            for phrase in [
                "registration fee",
                "processing fee",
                "security deposit",
                "pay to apply",
                "application fee"
            ]
        )

        extreme_urgency = any(
            phrase in job_description
            for phrase in [
                "apply now",
                "urgent hiring",
                "join immediately",
                "instant joining",
                "only today",
                "last chance"
            ]
        )

        unrealistic_hiring_claim = any(
            phrase in job_description
            for phrase in [
                "guaranteed job",
                "100% selection",
                "100% placement",
                "no interview",
                "guaranteed selection"
            ]
        )

        unrealistic_income_claim = any(
            phrase in job_description
            for phrase in [
                "earn money fast",
                "daily income",
                "easy money",
                "quick money"
            ]
        )

        messaging_contact = any(
            platform in job_description
            for platform in [
                "whatsapp",
                "telegram",
                "signal"
            ]
        )

        # =================================================
        # BUILD DETECTED SIGNALS
        # =================================================

        detected_signals = []

        if registration_fee:

            detected_signals.append(
                "Registration or payment requirement"
            )

        if extreme_urgency:

            detected_signals.append(
                "Extreme urgency"
            )

        if unrealistic_hiring_claim:

            detected_signals.append(
                "Unrealistic hiring claim"
            )

        if unrealistic_income_claim:

            detected_signals.append(
                "Unrealistic income claim"
            )

        if messaging_contact:

            detected_signals.append(
                "Messaging-platform recruitment"
            )

        signal_count = len(
            detected_signals
        )

        # =================================================
        # COMBINATION PATTERNS
        # =================================================

        patterns = []

        # Pattern 1
        if (
            registration_fee
            and extreme_urgency
        ):

            patterns.append(
                "Payment requirement combined with urgent recruitment."
            )

        # Pattern 2
        if (
            registration_fee
            and unrealistic_hiring_claim
        ):

            patterns.append(
                "Payment requirement combined with guaranteed hiring claims."
            )

        # Pattern 3
        if (
            extreme_urgency
            and unrealistic_hiring_claim
        ):

            patterns.append(
                "Extreme urgency combined with unrealistic hiring claims."
            )

        # Pattern 4
        if (
            unrealistic_income_claim
            and extreme_urgency
        ):

            patterns.append(
                "Unrealistic income claims combined with urgency."
            )

        # Pattern 5
        if (
            messaging_contact
            and extreme_urgency
        ):

            patterns.append(
                "Messaging-platform recruitment combined with urgency."
            )

        # Strong multi-signal pattern
        if (
            registration_fee
            and extreme_urgency
            and unrealistic_hiring_claim
        ):

            patterns.append(
                "Strong suspicious recruitment pattern detected: "
                "payment requirement, extreme urgency and unrealistic hiring claim."
            )

        pattern_count = len(
            patterns
        )

        # =================================================
        # DETERMINE RISK
        # =================================================

        if (
            registration_fee
            and extreme_urgency
            and unrealistic_hiring_claim
        ):

            risk = RISK_HIGH

            result["remarks"].append(
                "A strong combination of suspicious recruitment signals was detected."
            )

        elif pattern_count >= 2:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple suspicious recruitment patterns were detected."
            )

        elif pattern_count == 1:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "A suspicious combination of recruitment signals was detected."
            )

        elif signal_count >= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Multiple suspicious signals were detected, but no strong pattern was confirmed."
            )

        else:

            risk = RISK_LOW

            result["remarks"].append(
                "No significant suspicious recruitment pattern was detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "detected_signals": detected_signals,
            "signal_count": signal_count,
            "detected_patterns": patterns,
            "pattern_count": pattern_count
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result