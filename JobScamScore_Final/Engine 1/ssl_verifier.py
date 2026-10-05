import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_SSL_VERIFICATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    HTTP_TIMEOUT,
    HTTPS_PORT
)


def verify_ssl(url):
    """
    Verifies the SSL certificate of a website.

    Parameters:
        url (str): Website URL

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_SSL_VERIFICATION
    )

    try:

        # Extract hostname from URL
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname is None:
            raise ValueError("Invalid website URL.")

        # Create SSL context
        context = ssl.create_default_context()

        # Establish secure connection
        with socket.create_connection(
            (hostname, HTTPS_PORT),
            timeout=HTTP_TIMEOUT
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname
            ) as secure_socket:

                certificate = secure_socket.getpeercert()

        # Certificate expiry date
        expiry_date = datetime.strptime(
            certificate["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        days_remaining = (
            expiry_date - datetime.utcnow()
        ).days

        # Certificate issuer
        issuer = dict(
            item
            for sublist in certificate["issuer"]
            for item in sublist
        )

        result["status"] = STATUS_SUCCESS
        result["risk"] = RISK_LOW

        result["data"] = {

            "ssl_enabled": True,

            "issuer": issuer.get(
                "organizationName",
                "Unknown"
            ),

            "expiry_date": expiry_date.strftime(
                "%Y-%m-%d"
            ),

            "days_remaining": days_remaining
        }

        result["remarks"].append(
            "SSL certificate is valid."
        )

    except ssl.SSLError:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "Invalid or expired SSL certificate."
        )

    except socket.timeout:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "SSL connection timed out."
        )

    except socket.gaierror:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "Unable to resolve website hostname."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result