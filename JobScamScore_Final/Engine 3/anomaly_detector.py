from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_ANOMALY_DETECTOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def detect_anomalies(job_data):
    """
    Detects unusual characteristics in a job posting.

    Parameters:
        job_data (dict): Job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_ANOMALY_DETECTOR
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

        job_title = str(
            job_data.get(
                "job_title",
                ""
            )
        ).strip()

        job_description = str(
            job_data.get(
                "job_description",
                ""
            )
        ).strip()

        if not job_description:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # NORMALIZE DATA
        # =================================================

        text = job_description.lower()

        words = text.split()

        word_count = len(words)

        anomalies = []

        # =================================================
        # ANOMALY 1 - VERY SHORT DESCRIPTION
        # =================================================

        if word_count < 20:

            anomalies.append(
                "Very short job description"
            )

        # =================================================
        # ANOMALY 2 - EXCESSIVE REPETITION
        # =================================================

        word_frequency = {}

        for word in words:

            cleaned_word = (
                word
                .strip(".,!?;:()[]{}")
                .lower()
            )

            if cleaned_word:

                word_frequency[cleaned_word] = (
                    word_frequency.get(
                        cleaned_word,
                        0
                    ) + 1
                )

        repeated_words = [
            word
            for word, count in word_frequency.items()
            if count >= 5
        ]

        if len(repeated_words) >= 2:

            anomalies.append(
                "Unusually repetitive wording"
            )

        # =================================================
        # ANOMALY 3 - EXCESSIVE UPPERCASE
        # =================================================

        uppercase_words = [
            word
            for word in job_description.split()
            if word.isalpha() and word.isupper()
        ]

        uppercase_ratio = 0

        if word_count > 0:

            uppercase_ratio = (
                len(uppercase_words)
                / word_count
            )

        if uppercase_ratio > 0.30:

            anomalies.append(
                "Unusually high uppercase usage"
            )

        # =================================================
        # ANOMALY 4 - EXCESSIVE PUNCTUATION
        # =================================================

        punctuation_count = sum(
            1
            for character in job_description
            if character in "!?"
        )

        if punctuation_count >= 6:

            anomalies.append(
                "Unusually high punctuation usage"
            )

        # =================================================
        # ANOMALY 5 - EXCESSIVE MONEY LANGUAGE
        # =================================================

        money_terms = [
            "earn",
            "income",
            "salary",
            "cash",
            "money",
            "profit",
            "payment"
        ]

        money_term_count = sum(
            text.count(term)
            for term in money_terms
        )

        if (
            word_count >= 20
            and money_term_count >= 5
        ):

            anomalies.append(
                "Unusually high concentration of money-related language"
            )

        # =================================================
        # ANOMALY 6 - VERY HIGH PROMOTIONAL LANGUAGE
        # =================================================

        promotional_terms = [
            "amazing",
            "excellent",
            "guaranteed",
            "easy",
            "instant",
            "unlimited",
            "perfect",
            "dream",
            "best",
            "exciting"
        ]

        promotional_count = sum(
            text.count(term)
            for term in promotional_terms
        )

        if (
            word_count >= 20
            and promotional_count >= 5
        ):

            anomalies.append(
                "Unusually high promotional language"
            )

        # =================================================
        # ANOMALY 7 - MISSING BASIC JOB INFORMATION
        # =================================================

        basic_information = [
            "responsibilities",
            "requirements",
            "skills",
            "qualification",
            "experience",
            "location"
        ]

        information_present = sum(
            1
            for term in basic_information
            if term in text
        )

        if (
            word_count >= 40
            and information_present == 0
        ):

            anomalies.append(
                "Basic job information appears to be missing"
            )

        # =================================================
        # ANOMALY 8 - EXCESSIVE CONTACT METHODS
        # =================================================

        contact_methods = 0

        if "whatsapp" in text:
            contact_methods += 1

        if "telegram" in text:
            contact_methods += 1

        if "signal" in text:
            contact_methods += 1

        if "email" in text:
            contact_methods += 1

        if "call us" in text:
            contact_methods += 1

        if contact_methods >= 4:

            anomalies.append(
                "Unusually high number of contact methods"
            )

        # =================================================
        # DETERMINE RISK
        # =================================================

        anomaly_count = len(
            anomalies
        )

        if anomaly_count == 0:

            risk = RISK_LOW

            result["remarks"].append(
                "No significant posting anomalies were detected."
            )

        elif anomaly_count <= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Some unusual characteristics were detected."
            )

        else:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple unusual characteristics were detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "job_title": job_title,
            "anomalies": anomalies,
            "anomaly_count": anomaly_count,
            "word_count": word_count,
            "repeated_words": repeated_words,
            "uppercase_ratio": round(
                uppercase_ratio,
                2
            ),
            "money_term_count": money_term_count,
            "promotional_count": promotional_count,
            "information_present": information_present,
            "contact_method_count": contact_methods
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result