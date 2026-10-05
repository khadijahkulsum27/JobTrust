from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_INTELLIGENCE_EXPLANATION,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH
)


def generate_intelligence_explanation(
    pattern_result,
    behavior_result,
    consistency_result,
    salary_result,
    content_result,
    anomaly_result,
    score_result
):
    """
    Generates a human-readable explanation of the
    Engine 3 Job Posting Intelligence analysis.

    Parameters:
        pattern_result (dict)
        behavior_result (dict)
        consistency_result (dict)
        salary_result (dict)
        content_result (dict)
        anomaly_result (dict)
        score_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_INTELLIGENCE_EXPLANATION
    )

    try:

        report = []
        risk_factors = []
        positive_factors = []

        # =================================================
        # PATTERN ANALYSIS
        # =================================================

        pattern_data = pattern_result.get(
            "data",
            {}
        )

        detected_patterns = pattern_data.get(
            "detected_patterns",
            []
        )

        if detected_patterns:

            risk_factors.extend(
                detected_patterns
            )

        else:

            positive_factors.append(
                "No major suspicious recruitment patterns were detected."
            )

        # =================================================
        # SCAM BEHAVIOR ANALYSIS
        # =================================================

        behavior_data = behavior_result.get(
            "data",
            {}
        )

        detected_behaviors = behavior_data.get(
            "detected_behaviors",
            []
        )

        if detected_behaviors:

            risk_factors.extend(
                detected_behaviors
            )

        else:

            positive_factors.append(
                "No major suspicious recruitment behaviors were detected."
            )

        # =================================================
        # JOB CONSISTENCY ANALYSIS
        # =================================================

        consistency_data = consistency_result.get(
            "data",
            {}
        )

        consistency_issues = consistency_data.get(
            "consistency_issues",
            []
        )

        consistency_checks = consistency_data.get(
            "consistency_checks",
            []
        )

        if consistency_issues:

            risk_factors.extend(
                consistency_issues
            )

        else:

            positive_factors.extend(
                consistency_checks
            )

        # =================================================
        # SALARY ANALYSIS
        # =================================================

        salary_data = salary_result.get(
            "data",
            {}
        )

        salary_status = salary_data.get(
            "salary_status",
            "UNKNOWN"
        )

        if salary_status == "HIGHLY_UNUSUAL":

            risk_factors.append(
                "Salary appears highly unusual compared with the available reference information."
            )

        elif salary_status == "UNUSUAL":

            risk_factors.append(
                "Salary appears unusual compared with the available reference information."
            )

        elif salary_status == "NORMAL":

            positive_factors.append(
                "Salary appears reasonably consistent with the available reference information."
            )

        else:

            report.append(
                "Salary could not be confidently benchmarked."
            )

        # =================================================
        # AI CONTENT ANALYSIS
        # =================================================

        content_data = content_result.get(
            "data",
            {}
        )

        content_characteristics = (
            content_data.get(
                "detected_characteristics",
                []
            )
        )

        if content_characteristics:

            risk_factors.extend(
                content_characteristics
            )

        else:

            positive_factors.append(
                "No significant suspicious content characteristics were detected."
            )

        # =================================================
        # ANOMALY ANALYSIS
        # =================================================

        anomaly_data = anomaly_result.get(
            "data",
            {}
        )

        anomalies = anomaly_data.get(
            "anomalies",
            []
        )

        if anomalies:

            risk_factors.extend(
                anomalies
            )

        else:

            positive_factors.append(
                "No significant posting anomalies were detected."
            )

        # =================================================
        # FINAL SCORE
        # =================================================

        intelligence_score = score_result.get(
            "score",
            0
        )

        intelligence_risk = score_result.get(
            "risk",
            RISK_HIGH
        )

        report.append(
            f"Overall Job Intelligence Score: "
            f"{intelligence_score}/100."
        )

        report.append(
            f"Overall Job Intelligence Risk Level: "
            f"{intelligence_risk}."
        )

        # =================================================
        # SUMMARY
        # =================================================

        if intelligence_risk == "LOW":

            summary = (
                "The available job-posting evidence does not "
                "show major suspicious characteristics."
            )

        elif intelligence_risk == "MEDIUM":

            summary = (
                "The job posting contains some characteristics "
                "that require additional verification."
            )

        else:

            summary = (
                "The job posting contains multiple suspicious "
                "characteristics and should be treated cautiously."
            )

        report.insert(
            0,
            summary
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["score"] = intelligence_score
        result["risk"] = intelligence_risk

        result["data"] = {
            "summary": summary,
            "risk_factors": risk_factors,
            "positive_factors": positive_factors,
            "report": report
        }

        result["remarks"].append(
            "Job Intelligence explanation generated successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result