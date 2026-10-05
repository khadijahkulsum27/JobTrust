from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_MCA_VERIFICATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    MCA_ACTIVE,
    MCA_NOT_FOUND,
    MCA_SCORE
)


def verify_mca(company_name):
    """
    Demo MCA Verification.

    Simulates verification of a company against the
    Ministry of Corporate Affairs (MCA) database.

    Parameters:
        company_name (str)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_MCA_VERIFICATION
    )

    try:

        company = company_name.strip().lower()

        # -------------------------------------------------
        # Demo MCA Database
        # -------------------------------------------------

        registered_companies = [
            "infosys",
            "tcs",
            "tata consultancy services",
            "wipro",
            "accenture",
            "ibm",
            "google",
            "microsoft",
            "amazon",
            "flipkart",
            "zoho",
            "hcl",
            "tech mahindra",
            "cognizant",
            "oracle"
        ]

        # -------------------------------------------------
        # Company Found
        # -------------------------------------------------

        if company in registered_companies:

            result["status"] = STATUS_SUCCESS
            result["score"] = MCA_SCORE
            result["risk"] = RISK_LOW

            result["data"] = {
                "company_name": company_name,
                "mca_status": MCA_ACTIVE,
                "registered": True
            }

            result["remarks"].append(
                "Company found in MCA records."
            )

        # -------------------------------------------------
        # Company Not Found
        # -------------------------------------------------

        else:

            result["status"] = STATUS_FAILED
            result["score"] = 0
            result["risk"] = RISK_MEDIUM

            result["data"] = {
                "company_name": company_name,
                "mca_status": MCA_NOT_FOUND,
                "registered": False
            }

            result["remarks"].append(
                "Company not found in demo MCA database."
            )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result