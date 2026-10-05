from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_JOB_VALIDATOR,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH
)


def validate_job(job_data):
    """
    Validates the basic input required by the
    Job Content Analysis Engine.

    Parameters:
        job_data (dict): Job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_JOB_VALIDATOR
    )

    try:

        # =================================================
        # INPUT TYPE VALIDATION
        # =================================================

        if not isinstance(job_data, dict):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job data must be provided as a dictionary."
            )

            return result

        # =================================================
        # REQUIRED FIELDS
        # =================================================

        required_fields = [
            "job_title",
            "job_description"
        ]

        for field in required_fields:

            if field not in job_data:

                result["errors"].append(
                    f"{field} is missing."
                )

            elif not isinstance(
                job_data[field],
                str
            ):

                result["errors"].append(
                    f"{field} must be provided as text."
                )

            elif not job_data[field].strip():

                result["errors"].append(
                    f"{field} cannot be empty."
                )

        # Stop if required fields are invalid
        if result["errors"]:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            return result

        # =================================================
        # JOB TITLE VALIDATION
        # =================================================

        job_title = job_data[
            "job_title"
        ].strip()

        if len(job_title) < 2:

            result["errors"].append(
                "Job title is too short."
            )

        # =================================================
        # JOB DESCRIPTION VALIDATION
        # =================================================

        job_description = job_data[
            "job_description"
        ].strip()

        if len(job_description) < 20:

            result["errors"].append(
                "Job description is too short for analysis."
            )

        # =================================================
        # FINAL VALIDATION
        # =================================================

        if result["errors"]:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            return result

        result["status"] = STATUS_SUCCESS
        result["risk"] = RISK_LOW

        result["data"] = {
            "job_title": job_title,
            "job_description": job_description
        }

        result["remarks"].append(
            "Job input validation completed successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result