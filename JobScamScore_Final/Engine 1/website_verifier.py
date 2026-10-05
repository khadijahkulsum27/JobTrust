import time
import requests

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_WEBSITE_VERIFICATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    HTTP_OK,
    HTTP_MOVED_PERMANENTLY,
    HTTP_FOUND,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
    HTTP_TIMEOUT,
    USER_AGENT
)


def verify_website(url):
    """
    Verifies whether the company website is reachable.
    """

    result = create_engine_response(
        ENGINE_WEBSITE_VERIFICATION
    )

    try:

        start = time.time()

        response = requests.get(
            url,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
            headers=USER_AGENT
        )

        end = time.time()

        result["status"] = STATUS_SUCCESS
        result["risk"] = RISK_LOW

        result["data"] = {

            "status_code": response.status_code,

            "response_time": round(
                end - start,
                2
            ),

            "final_url": response.url
        }

        if response.status_code == HTTP_OK:

            result["remarks"].append(
                "Website is reachable."
            )

        elif response.status_code in (
            HTTP_MOVED_PERMANENTLY,
            HTTP_FOUND
        ):

            result["remarks"].append(
                "Website redirected successfully."
            )

        elif response.status_code == HTTP_FORBIDDEN:

            result["risk"] = RISK_MEDIUM

            result["remarks"].append(
                "Website denied access."
            )

        elif response.status_code == HTTP_NOT_FOUND:

            result["risk"] = RISK_HIGH

            result["remarks"].append(
                "Website not found."
            )

        else:

            result["remarks"].append(
                f"Website returned status code {response.status_code}."
            )

    except requests.exceptions.Timeout:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "Website request timed out."
        )

    except requests.exceptions.ConnectionError:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "Unable to connect to website."
        )

    except requests.exceptions.RequestException as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(str(e))

    return result