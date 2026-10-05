import whois
from datetime import datetime, timezone
from urllib.parse import urlparse

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_WHOIS_VERIFICATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def verify_whois(url):
    """
    Verifies WHOIS information of a company website.

    Parameters:
        url (str): Company website URL

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_WHOIS_VERIFICATION
    )

    try:

        # Extract domain from URL
        parsed_url = urlparse(url)

        domain = parsed_url.hostname

        if domain is None:
            raise ValueError("Invalid website URL.")

        if domain.startswith("www."):
            domain = domain[4:]

        # Fetch WHOIS information
        domain_info = whois.whois(domain)

        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date

        # Some WHOIS servers return a list of dates
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        # Calculate domain age
        domain_age_years = None

        if creation_date:
            domain_age_years = (
                datetime.now(timezone.utc) - creation_date
            ).days // 365

        # Determine risk
        if domain_age_years is None:
            risk = RISK_MEDIUM

        elif domain_age_years >= 5:
            risk = RISK_LOW

        elif domain_age_years >= 1:
            risk = RISK_MEDIUM

        else:
            risk = RISK_HIGH

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {

            "domain": domain,

            "registrar": domain_info.registrar,

            "creation_date": (
                creation_date.strftime("%Y-%m-%d")
                if creation_date
                else None
            ),

            "expiration_date": (
                expiration_date.strftime("%Y-%m-%d")
                if expiration_date
                else None
            ),

            "domain_age_years": domain_age_years
        }

        result["remarks"].append(
            "WHOIS information retrieved successfully."
        )

        if domain_age_years is not None:

            result["remarks"].append(
                f"Domain age: {domain_age_years} years."
            )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result