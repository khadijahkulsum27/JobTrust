from urllib.parse import urlparse

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_DOMAIN_MATCHING,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH
)


def match_domains(email, website):
    """
    Compares the email domain with the website domain.

    Parameters:
        email (str): Recruiter's email
        website (str): Company website

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_DOMAIN_MATCHING
    )

    try:

        email_domain = email.split("@")[1].lower()

        parsed_url = urlparse(website)

        website_domain = (
            parsed_url.hostname or ""
        ).lower()

        if website_domain.startswith("www."):
            website_domain = website_domain[4:]

        is_match = (
            email_domain == website_domain
        )

        result["status"] = STATUS_SUCCESS

        result["risk"] = (
            RISK_LOW if is_match
            else RISK_HIGH
        )

        result["data"] = {

            "website_domain": website_domain,

            "email_domain": email_domain,

            "domain_match": is_match
        }

        if is_match:

            result["remarks"].append(
                "Website and email domains match."
            )

        else:

            result["remarks"].append(
                "Website and email domains do not match."
            )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result