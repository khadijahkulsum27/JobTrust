"""
Engine 5 - Conflict Resolver

Resolves conflicting risk assessments between Engines 1-4.

The resolver gives higher importance to severe risk signals,
while still preserving information about disagreements
between engines.
"""


def resolve_conflicts(evidence, rule_result):
    """
    Resolve conflicts between Engine 1-4 assessments.

    Args:
        evidence (dict): Standardized evidence from
                         evidence_collector.py.

        rule_result (dict): Results from trust_rule_engine.py.

    Returns:
        dict: Conflict resolution result.
    """

    result = {
        "conflict_detected": False,
        "conflict_count": 0,
        "highest_risk": "UNKNOWN",
        "lowest_risk": "UNKNOWN",
        "resolved_risk": "UNKNOWN",
        "conflicts": [],
        "resolution_reasons": []
    }

    if not isinstance(evidence, dict):
        result["resolution_reasons"].append(
            "Valid evidence was not available for conflict resolution."
        )
        return result

    # -----------------------------------------
    # Collect available engine risks
    # -----------------------------------------

    risks = []

    for engine_number in range(1, 5):

        engine_key = f"engine_{engine_number}"

        engine_data = evidence.get(
            engine_key,
            {}
        )

        risk = engine_data.get("risk")

        # Only count engines that actually produced a score.
        if engine_data.get("score") is not None and risk in ("LOW", "MEDIUM", "HIGH"):

            risks.append({
                "engine": engine_key,
                "risk": risk
            })

    # -----------------------------------------
    # No usable risk information
    # -----------------------------------------

    if not risks:

        result["resolution_reasons"].append(
            "No usable engine risk classifications were available."
        )

        return result

    # -----------------------------------------
    # Risk ordering
    # -----------------------------------------

    risk_values = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    risk_names = [
        item["risk"]
        for item in risks
    ]

    highest_value = max(
        risk_values[risk]
        for risk in risk_names
    )

    lowest_value = min(
        risk_values[risk]
        for risk in risk_names
    )

    result["highest_risk"] = next(
        risk
        for risk, value in risk_values.items()
        if value == highest_value
    )

    result["lowest_risk"] = next(
        risk
        for risk, value in risk_values.items()
        if value == lowest_value
    )

    # -----------------------------------------
    # Detect conflict
    # -----------------------------------------

    unique_risks = set(risk_names)

    if len(unique_risks) > 1:

        result["conflict_detected"] = True

        result["conflict_count"] = (
            len(unique_risks) - 1
        )

        result["conflicts"].append(
            "Engine assessments do not agree on "
            "the same risk level."
        )

    # -----------------------------------------
    # Resolve risk
    # -----------------------------------------

    if "HIGH" in unique_risks:

        result["resolved_risk"] = "HIGH"

        result["resolution_reasons"].append(
            "A high-risk assessment was detected, "
            "so the overall risk cannot be classified "
            "as low while that evidence remains unresolved."
        )

    elif "MEDIUM" in unique_risks:

        result["resolved_risk"] = "MEDIUM"

        result["resolution_reasons"].append(
            "No high-risk assessment was detected, "
            "but at least one engine reported medium risk."
        )

    else:

        result["resolved_risk"] = "LOW"

        result["resolution_reasons"].append(
            "All available engine assessments indicate low risk."
        )

    # -----------------------------------------
    # Explain conflict
    # -----------------------------------------

    if result["conflict_detected"]:

        result["resolution_reasons"].append(
            f"Risk levels ranged from "
            f"{result['lowest_risk']} to "
            f"{result['highest_risk']} across the "
            f"available engines."
        )

    return result