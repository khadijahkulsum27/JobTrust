import re

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_SALARY_ANALYZER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    MAX_REASONABLE_MONTHLY_SALARY
)


def analyze_salary(job_description):
    """
    Analyzes salary information in a job description.

    Parameters:
        job_description (str): Job description text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_SALARY_ANALYZER
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
        # SALARY DETECTION
        # =================================================

        salary_patterns = [

            r"(?:rs\.?|₹)\s?(\d[\d,]*)",

            r"(\d[\d,]*)\s*(?:rs\.?|₹)",

            r"(?:salary|pay|package|ctc)"
            r"\s*(?:of|:|-)?\s*"
            r"(?:rs\.?|₹)?\s?"
            r"(\d[\d,]*)"
        ]

        salaries = []

        for pattern in salary_patterns:

            matches = re.findall(
                pattern,
                text
            )

            for match in matches:

                try:

                    value = int(
                        match.replace(",", "")
                    )

                    if value > 0:

                        salaries.append(
                            value
                        )

                except ValueError:

                    continue

        # Remove duplicate values
        salaries = list(
            dict.fromkeys(
                salaries
            )
        )

        # =================================================
        # NO SALARY DETECTED
        # =================================================

        if not salaries:

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_MEDIUM

            result["data"] = {
                "salary_found": False,
                "salary_values": [],
                "excessive_salary": False
            }

            result["remarks"].append(
                "No explicit salary information was detected."
            )

            return result

        # =================================================
        # SALARY RISK ANALYSIS
        # =================================================

        excessive_salary = any(
            salary > MAX_REASONABLE_MONTHLY_SALARY
            for salary in salaries
        )

        if excessive_salary:

            risk = RISK_HIGH

            result["remarks"].append(
                "Unusually high salary information detected."
            )

        else:

            risk = RISK_LOW

            result["remarks"].append(
                "Salary information appears within "
                "the configured threshold."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "salary_found": True,
            "salary_values": salaries,
            "excessive_salary": excessive_salary
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result