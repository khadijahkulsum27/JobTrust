import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_validator import validate_input
from website_verifier import verify_website
from ssl_verifier import verify_ssl
from email_verifier import verify_email 
from whois_verifier import verify_whois
from domain_matcher import match_domains
from identity_scorer import calculate_identity_score
from explanation_generator import generate_explanation
from mca_verifier import verify_mca

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_DIGITAL_IDENTITY,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)


def digital_identity_engine(job_data):
    """
    Executes the complete Digital Identity Verification Engine.

    Parameters:
        job_data (dict): Job information containing:
            - company_name
            - website
            - email
            - job_title

    Returns:
        dict: Final engine response
    """

    result = create_engine_response(
        ENGINE_DIGITAL_IDENTITY
    )

    try:

        # -------------------------------
        # Step 1: Input Validation
        # -------------------------------
        validation_result = validate_input(job_data)

        if validation_result["status"] != STATUS_SUCCESS:
            return validation_result

        website = validation_result["data"]["website"]
        email = validation_result["data"]["email"]

        # -------------------------------
        # Step 2: Website Verification
        # -------------------------------
        website_result = verify_website(website)

        # -------------------------------
        # Step 3: SSL Verification
        # -------------------------------
        ssl_result = verify_ssl(website)

        # -------------------------------
        # Step 4: Email Verification
        # -------------------------------
        email_result = verify_email(
            email,
            website
        )

        # -------------------------------
        # Step 5: WHOIS Verification
        # -------------------------------
        whois_result = verify_whois(website)

        # -------------------------------
        # Step 6: Domain Matching
        # -------------------------------
        domain_result = match_domains(
            email,
            website
        )
        # -------------------------------
        # Step 7: MCA Verification
        # -------------------------------
        mca_result = verify_mca(
        job_data.get("company_name", "")
        )
        
        # -------------------------------
        # Step 8: Identity Score
        # -------------------------------
        score_result = calculate_identity_score(
            website_result,
            ssl_result,
            email_result,
            whois_result,
            domain_result,
            mca_result
        )

        # -------------------------------
        # Step 9: Explanation Generator
        # -------------------------------
        explanation_result = generate_explanation(
            website_result,
            ssl_result,
            email_result,
            whois_result,
            domain_result,
            mca_result,
            score_result
        )

        # -------------------------------
        # Final Response
        # -------------------------------
        result["status"] = STATUS_SUCCESS
        result["score"] = score_result["score"]
        result["risk"] = score_result["risk"]

        result["data"] = {

            "input_validation": validation_result,

            "website_verification": website_result,

            "ssl_verification": ssl_result,

            "email_verification": email_result,

            "whois_verification": whois_result,

            "domain_matching": domain_result,
            
            "mca_verification": mca_result,

            "identity_score": score_result,

            "explanation": explanation_result
        }

        result["remarks"].append(
            "Digital Identity Verification completed successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result
if __name__ == "__main__":
    test_job = {
        "company_name": "Microsoft",
        "website": "https://www.microsoft.com",
        "email": "careers@microsoft.com",
        "job_title": "Software Developer"
    }

    result = digital_identity_engine(test_job)

    print(result)