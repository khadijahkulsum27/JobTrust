from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_EMAIL_VERIFICATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    PUBLIC_EMAIL_PROVIDERS
)


def verify_email(email, website):
    """
    Verifies whether the recruiter email is trustworthy.

    Parameters:
        email (str): Recruiter's email address
        website (str): Company's website URL

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_EMAIL_VERIFICATION
    )

    try:

        # Validate email format
        validate_email(
            email,
            check_deliverability=False
        )

        email_domain = email.split("@")[1].lower()

        parsed_url = urlparse(website)

        website_domain = (
            parsed_url.hostname or ""
        ).lower()

        if website_domain.startswith("www."):
            website_domain = website_domain[4:]

        domain_match = (
            email_domain == website_domain
        )

        public_email = (
            email_domain in PUBLIC_EMAIL_PROVIDERS
        )

        result["status"] = STATUS_SUCCESS

        result["data"] = {

            "email": email,

            "email_domain": email_domain,

            "website_domain": website_domain,

            "domain_match": domain_match,

            "public_email": public_email
        }

        result["remarks"].append(
            "Email format is valid."
        )

        if domain_match:

            result["remarks"].append(
                "Email domain matches company website."
            )

        else:

            result["remarks"].append(
                "Email domain does not match company website."
            )

        if public_email:

            result["risk"] = RISK_HIGH

            result["remarks"].append(
                "Public email provider detected."
            )

        elif domain_match:

            result["risk"] = RISK_LOW

        else:

            result["risk"] = RISK_MEDIUM

    except EmailNotValidError as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result