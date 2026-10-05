from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_INTELLIGENCE_SCORER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    PATTERN_SCORE,
    SCAM_BEHAVIOR_SCORE,
    JOB_CONSISTENCY_SCORE,
    SALARY_CONSISTENCY_SCORE,
    AI_CONTENT_SCORE,
    ANOMALY_SCORE,
    INTELLIGENCE_CLASSIFICATION_SCORE,
    INTELLIGENCE_TRUST_HIGH,
    INTELLIGENCE_TRUST_MEDIUM
)


def calculate_intelligence_score(
    pattern_result,
    behavior_result,
    consistency_result,
    salary_result,
    content_result,
    anomaly_result
):
    """
    Calculates the overall Engine 3 Job Intelligence Score.

    The score combines the results of the Engine 3
    intelligence analyzers into a single score out of 100.

    Parameters:
        pattern_result (dict)
        behavior_result (dict)
        consistency_result (dict)
        salary_result (dict)
        content_result (dict)
        anomaly_result (dict)

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_INTELLIGENCE_SCORER
    )

    try:

        score = 0

        component_scores = {}

        # =================================================
        # PATTERN ANALYSIS
        # =================================================

        pattern_component = 0

        if pattern_result["status"] == STATUS_SUCCESS:

            pattern_count = pattern_result.get(
                "data",
                {}
            ).get(
                "pattern_count",
                0
            )

            if pattern_count == 0:

                pattern_component = PATTERN_SCORE

            elif pattern_count == 1:

                pattern_component = PATTERN_SCORE // 2

            else:

                pattern_component = 0

        score += pattern_component

        component_scores["pattern_score"] = pattern_component

        # =================================================
        # SCAM BEHAVIOR ANALYSIS
        # =================================================

        behavior_component = 0

        if behavior_result["status"] == STATUS_SUCCESS:

            behavior_count = behavior_result.get(
                "data",
                {}
            ).get(
                "behavior_count",
                0
            )

            if behavior_count == 0:

                behavior_component = SCAM_BEHAVIOR_SCORE

            elif behavior_count == 1:

                behavior_component = SCAM_BEHAVIOR_SCORE // 2

            else:

                behavior_component = 0

        score += behavior_component

        component_scores["scam_behavior_score"] = (
            behavior_component
        )

        # =================================================
        # JOB CONSISTENCY ANALYSIS
        # =================================================

        consistency_component = 0

        if consistency_result["status"] == STATUS_SUCCESS:

            issue_count = consistency_result.get(
                "data",
                {}
            ).get(
                "issue_count",
                0
            )

            if issue_count == 0:

                consistency_component = (
                    JOB_CONSISTENCY_SCORE
                )

            elif issue_count <= 2:

                consistency_component = (
                    JOB_CONSISTENCY_SCORE // 2
                )

            else:

                consistency_component = 0

        score += consistency_component

        component_scores["job_consistency_score"] = (
            consistency_component
        )

        # =================================================
        # SALARY CONSISTENCY ANALYSIS
        # =================================================

        salary_component = 0

        if salary_result["status"] == STATUS_SUCCESS:

            salary_status = salary_result.get(
                "data",
                {}
            ).get(
                "salary_status",
                "UNKNOWN"
            )

            if salary_status == "NORMAL":

                salary_component = (
                    SALARY_CONSISTENCY_SCORE
                )

            elif salary_status == "UNUSUAL":

                salary_component = (
                    SALARY_CONSISTENCY_SCORE // 2
                )

            elif salary_status == "UNKNOWN":

                salary_component = (
                    SALARY_CONSISTENCY_SCORE // 2
                )

            else:

                salary_component = 0

        score += salary_component

        component_scores["salary_consistency_score"] = (
            salary_component
        )

        # =================================================
        # AI CONTENT ANALYSIS
        # =================================================

        content_component = 0

        if content_result["status"] == STATUS_SUCCESS:

            characteristic_count = content_result.get(
                "data",
                {}
            ).get(
                "characteristic_count",
                0
            )

            if characteristic_count == 0:

                content_component = (
                    AI_CONTENT_SCORE
                )

            elif characteristic_count <= 2:

                content_component = (
                    AI_CONTENT_SCORE // 2
                )

            else:

                content_component = 0

        score += content_component

        component_scores["ai_content_score"] = (
            content_component
        )

        # =================================================
        # ANOMALY ANALYSIS
        # =================================================

        anomaly_component = 0

        if anomaly_result["status"] == STATUS_SUCCESS:

            anomaly_count = anomaly_result.get(
                "data",
                {}
            ).get(
                "anomaly_count",
                0
            )

            if anomaly_count == 0:

                anomaly_component = (
                    ANOMALY_SCORE
                )

            elif anomaly_count <= 2:

                anomaly_component = (
                    ANOMALY_SCORE // 2
                )

            else:

                anomaly_component = 0

        score += anomaly_component

        component_scores["anomaly_score"] = (
            anomaly_component
        )

        # =================================================
        # BASE CLASSIFICATION SCORE
        # =================================================

        classification_component = (
            INTELLIGENCE_CLASSIFICATION_SCORE
        )

        score += classification_component

        component_scores["classification_score"] = (
            classification_component
        )

        # =================================================
        # STRONG SUSPICIOUS COMBINATION
        # =================================================

        pattern_data = pattern_result.get(
            "data",
            {}
        )

        behavior_data = behavior_result.get(
            "data",
            {}
        )

        detected_patterns = pattern_data.get(
            "detected_patterns",
            []
        )

        strong_pattern = any(
            "Strong suspicious recruitment pattern"
            in pattern
            for pattern in detected_patterns
        )

        payment_request = behavior_data.get(
            "payment_request",
            False
        )

        if (
            strong_pattern
            and payment_request
        ):

            combination_deduction = 15

            score -= combination_deduction

            result["remarks"].append(
                "High-risk combination of suspicious recruitment signals detected."
            )

        # =================================================
        # CLAMP SCORE
        # =================================================

        score = max(
            0,
            min(
                100,
                score
            )
        )

        # =================================================
        # DETERMINE RISK
        # =================================================

        if score >= INTELLIGENCE_TRUST_HIGH:

            risk = RISK_LOW

        elif score >= INTELLIGENCE_TRUST_MEDIUM:

            risk = RISK_MEDIUM

        else:

            risk = RISK_HIGH

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["score"] = score
        result["risk"] = risk

        result["data"] = {
            "intelligence_score": score,
            "component_scores": component_scores
        }

        result["remarks"].append(
            f"Job Intelligence Score calculated: {score}/100."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result