import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_JOB_INTELLIGENCE,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)

from pattern_detector import (
    detect_patterns
)

from scam_behavior_detector import (
    detect_scam_behavior
)

from job_consistency_analyzer import (
    analyze_job_consistency
)

from salary_consistency_analyzer import (
    analyze_salary_consistency
)

from ai_content_analyzer import (
    analyze_ai_content
)

from anomaly_detector import (
    detect_anomalies
)

from intelligence_scorer import (
    calculate_intelligence_score
)

from intelligence_explanation import (
    generate_intelligence_explanation
)


def analyze_job_intelligence(job_data):
    """
    Runs the complete Engine 3 Job Posting Intelligence Engine.

    Parameters:
        job_data (dict): Structured job posting data

    Returns:
        dict: Complete Engine 3 response
    """

    result = create_engine_response(
        ENGINE_JOB_INTELLIGENCE
    )

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if not isinstance(job_data, dict):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job data must be provided as a dictionary."
            )

            return result

        # =================================================
        # STEP 1 - PATTERN DETECTION
        # =================================================

        pattern_result = detect_patterns(
            job_data
        )

        # =================================================
        # STEP 2 - SCAM BEHAVIOR DETECTION
        # =================================================

        behavior_result = detect_scam_behavior(
            job_data
        )

        # =================================================
        # STEP 3 - JOB CONSISTENCY ANALYSIS
        # =================================================

        consistency_result = analyze_job_consistency(
            job_data
        )

        # =================================================
        # STEP 4 - SALARY CONSISTENCY ANALYSIS
        # =================================================

        salary_result = analyze_salary_consistency(
            job_data
        )

        # =================================================
        # STEP 5 - AI CONTENT ANALYSIS
        # =================================================

        content_result = analyze_ai_content(
            job_data
        )

        # =================================================
        # STEP 6 - ANOMALY DETECTION
        # =================================================

        anomaly_result = detect_anomalies(
            job_data
        )

        # =================================================
        # STEP 7 - INTELLIGENCE SCORING
        # =================================================

        score_result = calculate_intelligence_score(
            pattern_result,
            behavior_result,
            consistency_result,
            salary_result,
            content_result,
            anomaly_result
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
            generate_intelligence_explanation(
                pattern_result,
                behavior_result,
                consistency_result,
                salary_result,
                content_result,
                anomaly_result,
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

            "pattern_analysis": (
                pattern_result
            ),

            "scam_behavior_analysis": (
                behavior_result
            ),

            "job_consistency_analysis": (
                consistency_result
            ),

            "salary_consistency_analysis": (
                salary_result
            ),

            "ai_content_analysis": (
                content_result
            ),

            "anomaly_analysis": (
                anomaly_result
            ),

            "intelligence_score": (
                score_result
            ),

            "explanation": (
                explanation_result
            )

        }

        result["remarks"].append(
            "Job Posting Intelligence Engine completed successfully."
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
        """,
        "salary": 800000,
        "experience_level": "fresher"
    }

    result = analyze_job_intelligence(test_job)

    print(result)