import validators
from email_validator import validate_email, EmailNotValidError

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_VALIDATION,
    MCA_PENDING
)


def validate_input(job_data):
    """
    Validates the input data for the Digital Identity Engine.
    """

    result = create_engine_response(
        ENGINE_INPUT_VALIDATION
    )

    required_fields = [
        "company_name",
        "website",
        "email",
        "job_title"
    ]

    # Check required fields
    for field in required_fields:

        if field not in job_data:
            result["errors"].append(
                f"{field} is missing."
            )

        elif not str(job_data[field]).strip():
            result["errors"].append(
                f"{field} cannot be empty."
            )

    # Stop if required fields are missing
    if result["errors"]:
        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH
        return result

    # Validate website
    if not validators.url(job_data["website"]):
        result["errors"].append(
            "Invalid website URL."
        )

    # Validate email
    try:

        validate_email(
            job_data["email"],
            check_deliverability=False
        )

    except EmailNotValidError as e:

        result["errors"].append(str(e))

    # Final Result
    if result["errors"]:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

    else:

        result["status"] = STATUS_SUCCESS
        result["risk"] = RISK_LOW

        result["remarks"].append(
            "Input validation completed successfully."
        )

        result["data"] = {
            "company_name": job_data["company_name"].strip(),
            "website": job_data["website"],
            "email": job_data["email"],
            "job_title": job_data["job_title"],
            "mca_verification": MCA_PENDING
        }

    return result


