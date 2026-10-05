import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_JOB_CONTENT,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)

from job_validator import validate_job
from keyword_detector import detect_keywords
from salary_analyzer import analyze_salary
from grammer_checker import check_grammar
from urgency_detector import detect_urgency
from contact_analyser import analyze_contact
from content_scorer import calculate_content_score
from content_explanation import (
    generate_content_explanation
)


def analyze_job_content(job_data):
    """
    Runs the complete Job Content Analysis Engine.

    Parameters:
        job_data (dict): Job posting data

    Returns:
        dict: Complete Engine 2 response
    """

    result = create_engine_response(
        ENGINE_JOB_CONTENT
    )

    try:

        # =================================================
        # STEP 1 - JOB VALIDATION
        # =================================================

        validation_result = validate_job(
            job_data
        )

        if validation_result["status"] != STATUS_SUCCESS:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].extend(
                validation_result["errors"]
            )

            return result

        job_description = (
            validation_result["data"]["job_description"]
        )

        # =================================================
        # STEP 2 - KEYWORD DETECTION
        # =================================================

        keyword_result = detect_keywords(
            job_description
        )

        # =================================================
        # STEP 3 - SALARY ANALYSIS
        # =================================================

        salary_result = analyze_salary(
            job_description
        )

        # =================================================
        # STEP 4 - GRAMMAR CHECK
        # =================================================

        grammar_result = check_grammar(
            job_description
        )

        # =================================================
        # STEP 5 - URGENCY DETECTION
        # =================================================

        urgency_result = detect_urgency(
            job_description
        )

        # =================================================
        # STEP 6 - CONTACT ANALYSIS
        # =================================================

        contact_result = analyze_contact(
            job_description
        )

        # =================================================
        # STEP 7 - CONTENT SCORING
        # =================================================

        score_result = calculate_content_score(
            keyword_result,
            salary_result,
            grammar_result,
            urgency_result,
            contact_result
        )

        if score_result["status"] != STATUS_SUCCESS:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].extend(
                score_result["errors"]
            )

            return result

        # =================================================
        # STEP 8 - EXPLANATION GENERATION
        # =================================================

        explanation_result = (
            generate_content_explanation(
                keyword_result,
                salary_result,
                grammar_result,
                urgency_result,
                contact_result,
                score_result
            )
        )

        # =================================================
        # FINAL ENGINE RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["score"] = score_result["score"]
        result["risk"] = score_result["risk"]

        result["data"] = {

            "validation": validation_result,

            "keyword_analysis": keyword_result,

            "salary_analysis": salary_result,

            "grammar_analysis": grammar_result,

            "urgency_analysis": urgency_result,

            "contact_analysis": contact_result,

            "score": score_result,

            "explanation": explanation_result

        }

        result["remarks"].append(
            "Job Content Analysis Engine "
            "completed successfully."
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
        "job_title": "Software Developer",
        "company_name": "Microsoft",
        "job_description": """
        We are looking for a Software Developer to join our team.
        The candidate should have experience with Python and web development.
        Salary: ₹8,00,000 per year.
        Please apply through our official company website.
        """
    }

    result = analyze_job_content(test_job)

    print(result)