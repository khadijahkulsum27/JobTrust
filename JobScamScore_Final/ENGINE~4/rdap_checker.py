"""
Engine 4 - RDAP Checker

Checks domain registration information using RDAP
and estimates the age of the domain.
"""

from datetime import datetime, timezone

import requests

from utils.constants import (
    HTTP_TIMEOUT,
    CHECK_AVAILABLE,
    CHECK_ERROR,
    CHECK_SKIPPED,
    CYBER_INDICATOR_RECENT_DOMAIN,
    CYBER_POSITIVE_ESTABLISHED_DOMAIN,
    RECENT_DOMAIN_DAYS,
    ESTABLISHED_DOMAIN_DAYS,
)


RDAP_BASE_URL = "https://rdap.org/domain/"


def _parse_rdap_date(date_value):
    """
    Convert an RDAP date string into a datetime object.
    """

    if not date_value:
        return None

    try:
        # Handle standard ISO-8601 timestamps.
        return datetime.fromisoformat(
            date_value.replace("Z", "+00:00")
        )

    except (ValueError, TypeError):
        return None


def _extract_event(events, event_action):
    """
    Extract a specific event date from RDAP events.
    """

    for event in events:

        if event.get("eventAction") == event_action:

            event_date = event.get("eventDate")

            parsed_date = _parse_rdap_date(event_date)

            if parsed_date:
                return parsed_date

    return None


def check_rdap(domain):
    """
    Check domain registration information using RDAP.

    Args:
        domain (str): Domain name.

    Returns:
        dict: RDAP analysis result.
    """

    result = {
        "status": CHECK_SKIPPED,
        "domain": domain,
        "registered": False,
        "registration_date": None,
        "expiration_date": None,
        "last_changed": None,
        "domain_age_days": None,
        "domain_age_category": "UNKNOWN",
        "registrar": None,
        "indicators": [],
        "positive_indicators": [],
        "remarks": [],
        "errors": []
    }

    # -----------------------------------------
    # Input validation
    # -----------------------------------------

    if not isinstance(domain, str) or not domain.strip():

        result["remarks"].append(
            "RDAP check skipped because no domain was provided."
        )

        return result

    domain = domain.strip().lower()

    # Remove accidental trailing dot.
    domain = domain.rstrip(".")

    result["domain"] = domain

    # -----------------------------------------
    # RDAP request
    # -----------------------------------------

    try:

        rdap_url = RDAP_BASE_URL + domain

        response = requests.get(
            rdap_url,
            timeout=HTTP_TIMEOUT,
            headers={
                "Accept": "application/rdap+json"
            }
        )

        # -----------------------------------------
        # Domain not found
        # -----------------------------------------

        if response.status_code == 404:

            result["status"] = CHECK_AVAILABLE

            result["remarks"].append(
                "Domain registration information was not found."
            )

            return result

        response.raise_for_status()

        data = response.json()

        result["status"] = CHECK_AVAILABLE
        result["registered"] = True

        # -----------------------------------------
        # Events
        # -----------------------------------------

        events = data.get("events", [])

        registration_date = _extract_event(
            events,
            "registration"
        )

        expiration_date = _extract_event(
            events,
            "expiration"
        )

        last_changed = _extract_event(
            events,
            "last changed"
        )

        result["registration_date"] = (
            registration_date.isoformat()
            if registration_date
            else None
        )

        result["expiration_date"] = (
            expiration_date.isoformat()
            if expiration_date
            else None
        )

        result["last_changed"] = (
            last_changed.isoformat()
            if last_changed
            else None
        )

        # -----------------------------------------
        # Domain age
        # -----------------------------------------

        if registration_date:

            now = datetime.now(timezone.utc)

            # Ensure timezone-aware datetime.
            if registration_date.tzinfo is None:
                registration_date = registration_date.replace(
                    tzinfo=timezone.utc
                )

            domain_age = (
                now - registration_date
            ).days

            result["domain_age_days"] = max(
                0,
                domain_age
            )

            # -------------------------------------
            # Domain age classification
            # -------------------------------------

            if domain_age < RECENT_DOMAIN_DAYS:

                result["domain_age_category"] = "RECENT"

                result["indicators"].append(
                    CYBER_INDICATOR_RECENT_DOMAIN
                )

                result["remarks"].append(
                    "The domain appears to have been "
                    "registered recently."
                )

            elif domain_age >= ESTABLISHED_DOMAIN_DAYS:

                result["domain_age_category"] = "ESTABLISHED"

                result["positive_indicators"].append(
                    CYBER_POSITIVE_ESTABLISHED_DOMAIN
                )

                result["remarks"].append(
                    "The domain appears to be established."
                )

            else:

                result["domain_age_category"] = "MODERATE"

                result["remarks"].append(
                    "The domain has a moderate registration age."
                )

        # -----------------------------------------
        # Registrar
        # -----------------------------------------

        entities = data.get("entities", [])

        for entity in entities:

            roles = entity.get("roles", [])

            if "registrar" in roles:

                vcard_array = entity.get(
                    "vcardArray",
                    []
                )

                if (
                    isinstance(vcard_array, list)
                    and len(vcard_array) > 1
                ):

                    for item in vcard_array[1]:

                        if (
                            isinstance(item, list)
                            and len(item) >= 4
                            and item[0] == "fn"
                        ):

                            result["registrar"] = item[3]

                            break

                break

        # -----------------------------------------
        # Completion
        # -----------------------------------------

        result["remarks"].append(
            "RDAP domain registration check completed."
        )

        return result

    # -----------------------------------------
    # Request error
    # -----------------------------------------

    except requests.exceptions.Timeout:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            "RDAP request timed out."
        )

        return result

    except requests.exceptions.ConnectionError as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"RDAP connection failed: {str(exc)}"
        )

        return result

    except requests.exceptions.RequestException as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"RDAP request failed: {str(exc)}"
        )

        return result

    except ValueError as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"Invalid RDAP response: {str(exc)}"
        )

        return result

    except Exception as exc:

        result["status"] = CHECK_ERROR

        result["errors"].append(
            f"RDAP check failed: {str(exc)}"
        )

        return result