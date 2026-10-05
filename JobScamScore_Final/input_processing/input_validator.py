"""
input_validator.py

Validates standardized job data before
passing it to the AI Content Analysis Engine.
"""

import validators
from email_validator import (
    validate_email,
    EmailNotValidError
)

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_PROCESSING,
    SOURCE_MANUAL
)


def validate_standardized_data(job_data):
    """
    Validates standardized job data.

    Parameters:
        job_data (dict)

    Returns:
        dict
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        # -----------------------------
        # Basic Input Validation
        # -----------------------------

        if not isinstance(job_data, dict):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Standardized job data must be a dictionary."
            )

            return result

        # -----------------------------
        # Source Type Validation
        # -----------------------------

        source_type = job_data.get(
            "source_type",
            ""
        )

        if not str(source_type).strip():

            result["errors"].append(
                "source_type is missing."
            )

        # -----------------------------
        # Required Fields
        # -----------------------------

        if source_type == SOURCE_MANUAL:

            # Manual input already contains
            # structured job information.
            required_fields = [
                "job_title",
                "job_description"
            ]

        else:

            # Extracted inputs such as PDF,
            # image, website and text should
            # contain raw extracted text.
            required_fields = [
                "raw_text"
            ]

        # -----------------------------
        # Required Field Validation
        # -----------------------------

        for field in required_fields:

            if field not in job_data:

                result["errors"].append(
                    f"{field} is missing."
                )

            elif not str(job_data[field]).strip():

                result["errors"].append(
                    f"{field} cannot be empty."
                )

        # -----------------------------
        # Website Validation
        # -----------------------------

        website = job_data.get(
            "website",
            ""
        )

        if website:

            if not validators.url(
                website
            ):

                result["errors"].append(
                    "Invalid website URL."
                )

        # -----------------------------
        # Email Validation
        # -----------------------------

        email = job_data.get(
            "email",
            ""
        )

        if email:

            try:

                validate_email(
                    email,
                    check_deliverability=False
                )

            except EmailNotValidError as e:

                result["errors"].append(
                    str(e)
                )

        # -----------------------------
        # Skills Validation
        # -----------------------------

        skills = job_data.get(
            "skills",
            []
        )

        if not isinstance(
            skills,
            list
        ):

            result["errors"].append(
                "Skills must be a list."
            )

        # -----------------------------
        # Metadata Validation
        # -----------------------------

        metadata = job_data.get(
            "metadata",
            {}
        )

        if not isinstance(
            metadata,
            dict
        ):

            result["errors"].append(
                "Metadata must be a dictionary."
            )

        # -----------------------------
        # Final Result
        # -----------------------------

        if result["errors"]:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

        else:

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_LOW

            result["data"] = job_data

            result["remarks"].append(
                "Input validation completed successfully."
            )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result