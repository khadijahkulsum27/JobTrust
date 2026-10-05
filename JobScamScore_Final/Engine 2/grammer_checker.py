from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_GRAMMAR_CHECKER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def check_grammar(job_description):
    """
    Performs basic grammar and writing-quality checks
    on a job description.

    Parameters:
        job_description (str): Job description text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_GRAMMAR_CHECKER
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

        text = job_description.strip()

        if not text:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # WRITING-QUALITY CHECKS
        # =================================================

        issues = []

        words = text.split()

        # -------------------------------------------------
        # Excessive punctuation
        # -------------------------------------------------

        if "!!" in text or "??" in text or "..." in text:

            issues.append(
                "Excessive punctuation detected."
            )

        # -------------------------------------------------
        # Excessive uppercase text
        # -------------------------------------------------

        uppercase_words = [
            word
            for word in words
            if word.isalpha() and word.isupper()
        ]

        uppercase_ratio = (
            len(uppercase_words) / len(words)
            if words
            else 0
        )

        if uppercase_ratio > 0.30:

            issues.append(
                "Excessive use of uppercase text detected."
            )

        # -------------------------------------------------
        # Repeated consecutive words
        # -------------------------------------------------

        repeated_words = []

        previous_word = ""

        for word in words:

            cleaned_word = (
                word.lower()
                .strip(".,!?;:()[]{}")
            )

            if (
                cleaned_word
                and cleaned_word == previous_word
            ):

                if cleaned_word not in repeated_words:

                    repeated_words.append(
                        cleaned_word
                    )

            previous_word = cleaned_word

        if repeated_words:

            issues.append(
                "Repeated words were detected."
            )

        # -------------------------------------------------
        # Very short sentences
        # -------------------------------------------------

        sentence_parts = (
            text.replace("!", ".")
            .replace("?", ".")
            .split(".")
        )

        short_sentences = 0

        for sentence in sentence_parts:

            sentence = sentence.strip()

            if sentence:

                sentence_word_count = len(
                    sentence.split()
                )

                if sentence_word_count < 3 and ":" not in sentence:

                    short_sentences += 1

        if short_sentences > 0:

            issues.append(
                "Very short sentence fragments detected."
            )

        # =================================================
        # RISK CLASSIFICATION
        # =================================================

        issue_count = len(issues)

        if issue_count == 0:

            risk = RISK_LOW

            result["remarks"].append(
                "No major writing-quality issues detected."
            )

        elif issue_count <= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Some writing-quality issues were detected."
            )

        else:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple writing-quality issues were detected."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "issue_count": issue_count,
            "issues": issues,
            "uppercase_word_count": len(
                uppercase_words
            ),
            "repeated_words": repeated_words,
            "short_sentence_count": short_sentences
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result