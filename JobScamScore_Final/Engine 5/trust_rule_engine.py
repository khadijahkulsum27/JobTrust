"""
Engine 5 - Trust Rule Engine

Applies rule-based logic to the evidence collected
from Engines 1-4.

This module identifies positive, negative, and
uncertain trust signals. It does not calculate the
final trust score.
"""


def evaluate_trust_rules(evidence):
    """
    Evaluate trust-related rules using Engine 1-4 evidence.

    Args:
        evidence (dict): Standardized evidence from
                         evidence_collector.py.

    Returns:
        dict: Rule evaluation results.
    """

    result = {
        "positive_signals": [],
        "negative_signals": [],
        "uncertain_signals": [],
        "engine_assessments": {},
        "rule_count": 0
    }

    if not isinstance(evidence, dict):
        result["uncertain_signals"].append(
            "No valid evidence was provided."
        )
        return result

    # =========================================
    # ENGINE 1 — DIGITAL IDENTITY
    # =========================================

    engine1 = evidence.get(
        "engine_1",
        {}
    )

    engine1_score = engine1.get("score")
    engine1_risk = engine1.get("risk")
    engine1_status = engine1.get("status")

    if engine1_score is not None:

        if engine1_risk == "HIGH":

            result["negative_signals"].append(
                "Engine 1 identified a high identity risk."
            )

        elif engine1_risk == "MEDIUM":

            result["uncertain_signals"].append(
                "Engine 1 identified a medium identity risk."
            )

        elif engine1_risk == "LOW":

            result["positive_signals"].append(
                "Engine 1 indicates relatively low identity risk."
            )

        result["engine_assessments"]["engine_1"] = {
            "score": engine1_score,
            "risk": engine1_risk,
            "status": engine1_status
        }

    else:

        result["uncertain_signals"].append(
            "Engine 1 did not provide a usable score."
        )

    # =========================================
    # ENGINE 2 — JOB CONTENT
    # =========================================

    engine2 = evidence.get(
        "engine_2",
        {}
    )

    engine2_score = engine2.get("score")
    engine2_risk = engine2.get("risk")
    engine2_status = engine2.get("status")

    if engine2_score is not None:

        if engine2_risk == "HIGH":

            result["negative_signals"].append(
                "Engine 2 identified a high job-content risk."
            )

        elif engine2_risk == "MEDIUM":

            result["uncertain_signals"].append(
                "Engine 2 identified a medium job-content risk."
            )

        elif engine2_risk == "LOW":

            result["positive_signals"].append(
                "Engine 2 indicates relatively low job-content risk."
            )

        result["engine_assessments"]["engine_2"] = {
            "score": engine2_score,
            "risk": engine2_risk,
            "status": engine2_status
        }

    else:

        result["uncertain_signals"].append(
            "Engine 2 did not provide a usable score."
        )

    # =========================================
    # ENGINE 3 — JOB POSTING INTELLIGENCE
    # =========================================

    engine3 = evidence.get(
        "engine_3",
        {}
    )

    engine3_score = engine3.get("score")
    engine3_risk = engine3.get("risk")
    engine3_status = engine3.get("status")

    if engine3_score is not None:

        if engine3_risk == "HIGH":

            result["negative_signals"].append(
                "Engine 3 identified a high job-posting intelligence risk."
            )

        elif engine3_risk == "MEDIUM":

            result["uncertain_signals"].append(
                "Engine 3 identified a medium job-posting intelligence risk."
            )

        elif engine3_risk == "LOW":

            result["positive_signals"].append(
                "Engine 3 indicates relatively low job-posting intelligence risk."
            )

        result["engine_assessments"]["engine_3"] = {
            "score": engine3_score,
            "risk": engine3_risk,
            "status": engine3_status
        }

    else:

        result["uncertain_signals"].append(
            "Engine 3 did not provide a usable score."
        )

    # =========================================
    # ENGINE 4 — CYBER THREAT
    # =========================================

    engine4 = evidence.get(
        "engine_4",
        {}
    )

    engine4_score = engine4.get("score")
    engine4_risk = engine4.get("risk")
    engine4_status = engine4.get("status")

    if engine4_score is not None:

        if engine4_risk == "HIGH":

            result["negative_signals"].append(
                "Engine 4 identified a high cyber risk."
            )

        elif engine4_risk == "MEDIUM":

            result["uncertain_signals"].append(
                "Engine 4 identified a medium cyber risk."
            )

        elif engine4_risk == "LOW":

            result["positive_signals"].append(
                "Engine 4 indicates relatively low cyber risk."
            )

        result["engine_assessments"]["engine_4"] = {
            "score": engine4_score,
            "risk": engine4_risk,
            "status": engine4_status
        }

    else:

        result["uncertain_signals"].append(
            "Engine 4 did not provide a usable score."
        )

    # =========================================
    # COUNT RULES
    # =========================================

    result["rule_count"] = (
        len(result["positive_signals"])
        + len(result["negative_signals"])
        + len(result["uncertain_signals"])
    )

    return result