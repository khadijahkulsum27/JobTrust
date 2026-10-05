from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_SALARY_CONSISTENCY_ANALYZER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    SALARY_NORMAL,
    SALARY_UNUSUAL,
    SALARY_HIGHLY_UNUSUAL,
    SALARY_UNKNOWN
)

from salary_reference import SALARY_REFERENCE


def analyze_salary_consistency(job_data):
    """
    Compares the offered salary with the reference salary
    range for the advertised job role.

    Parameters:
        job_data (dict): Complete job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_SALARY_CONSISTENCY_ANALYZER
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
        # EXTRACT JOB INFORMATION
        # =================================================

        job_title = str(
            job_data.get(
                "job_title",
                ""
            )
        ).strip()

        salary = job_data.get(
            "salary"
        )

        experience_level = str(
            job_data.get(
                "experience_level",
                "fresher"
            )
        ).lower().strip()

        # =================================================
        # VALIDATE JOB TITLE
        # =================================================

        if not job_title:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job title cannot be empty."
            )

            return result

        # =================================================
        # HANDLE MISSING SALARY
        # =================================================

        if salary is None:

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_MEDIUM

            result["data"] = {
                "job_title": job_title,
                "salary": None,
                "experience_level": experience_level,
                "salary_status": SALARY_UNKNOWN,
                "reference_range": None
            }

            result["remarks"].append(
                "No explicit salary value was available for salary consistency analysis."
            )

            return result

        # =================================================
        # VALIDATE SALARY
        # =================================================

        if not isinstance(salary, (int, float)):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Salary must be provided as a numeric value."
            )

            return result

        if salary <= 0:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Salary must be greater than zero."
            )

            return result

        # =================================================
        # NORMALIZE JOB TITLE
        # =================================================

        normalized_title = (
            job_title
            .lower()
            .strip()
        )

        # =================================================
        # FIND JOB ROLE
        # =================================================

        if normalized_title not in SALARY_REFERENCE:

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_MEDIUM

            result["data"] = {
                "job_title": job_title,
                "salary": salary,
                "experience_level": experience_level,
                "salary_status": SALARY_UNKNOWN,
                "reference_range": None
            }

            result["remarks"].append(
                "No salary reference data was found for this job role."
            )

            return result

        role_reference = SALARY_REFERENCE[
            normalized_title
        ]

        # =================================================
        # FIND EXPERIENCE LEVEL
        # =================================================

        if experience_level not in role_reference:

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_MEDIUM

            result["data"] = {
                "job_title": job_title,
                "salary": salary,
                "experience_level": experience_level,
                "salary_status": SALARY_UNKNOWN,
                "reference_range": None
            }

            result["remarks"].append(
                "No salary reference data was found for the specified experience level."
            )

            return result

        # =================================================
        # GET REFERENCE RANGE
        # =================================================

        minimum_salary, maximum_salary = (
            role_reference[
                experience_level
            ]
        )

        reference_range = {
            "minimum": minimum_salary,
            "maximum": maximum_salary
        }

        # =================================================
        # COMPARE SALARY
        # =================================================

        if minimum_salary <= salary <= maximum_salary:

            salary_status = SALARY_NORMAL
            risk = RISK_LOW

            result["remarks"].append(
                "Offered salary is within the configured reference range."
            )

        elif salary <= maximum_salary * 1.5:

            salary_status = SALARY_UNUSUAL
            risk = RISK_MEDIUM

            result["remarks"].append(
                "Offered salary is above the configured reference range."
            )

        else:

            salary_status = SALARY_HIGHLY_UNUSUAL
            risk = RISK_HIGH

            result["remarks"].append(
                "Offered salary is significantly above the configured reference range."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "job_title": job_title,
            "salary": salary,
            "experience_level": experience_level,
            "salary_status": salary_status,
            "reference_range": reference_range
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result