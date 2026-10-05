"""
Engine 5 - Trust Decision Explanation

Generates human-readable explanations for the
final trust decision produced by Engine 5.
"""


# =====================================================
# INTERNAL CONSTANTS
# =====================================================

TRUSTED = "TRUSTED"
REVIEW = "REVIEW"
HIGH_RISK = "HIGH_RISK"


# =====================================================
# ENGINE DISPLAY NAMES
# =====================================================

ENGINE_NAMES = {
    "engine_1": "Digital Identity Verification",
    "engine_2": "AI Content Intelligence",
    "engine_3": "Job Posting Intelligence",
    "engine_4": "Cyber Threat Intelligence"
}


# =====================================================
# MAIN EXPLANATION FUNCTION
# =====================================================

def generate_trust_decision_explanation(
    evidence,
    rule_result,
    conflict_result,
    score_result
):
    """
    Generates an explainable summary of the final
    Engine 5 trust decision.

    Parameters
    ----------
    evidence : dict
        Evidence collected from Engines 1-4.

    rule_result : dict
        Results produced by trust_rule_engine.py.

    conflict_result : dict
        Results produced by conflict_resolver.py.

    score_result : dict
        Results produced by trust_decision_scorer.py.

    Returns
    -------
    dict
        Human-readable explanation data.
    """

    if not isinstance(evidence, dict):
        evidence = {}

    if not isinstance(rule_result, dict):
        rule_result = {}

    if not isinstance(conflict_result, dict):
        conflict_result = {}

    if not isinstance(score_result, dict):
        score_result = {}

    trust_score = score_result.get("trust_score")
    decision = score_result.get(
        "decision",
        REVIEW
    )

    confidence = score_result.get(
        "confidence",
        0
    )

    # =================================================
    # SUMMARY
    # =================================================

    if decision == TRUSTED:
        summary = (
            "The job posting received a high overall "
            "trust assessment based on the available "
            "evidence."
        )

    elif decision == HIGH_RISK:
        summary = (
            "The job posting contains significant "
            "risk indicators and should be treated "
            "with caution."
        )

    else:
        summary = (
            "The job posting has mixed or incomplete "
            "evidence and requires further review."
        )

    # =================================================
    # ENGINE EXPLANATIONS
    # =================================================

    engine_explanations = []

    normalized_scores = score_result.get(
        "normalized_scores",
        {}
    )

    for engine_name, trust_score_value in normalized_scores.items():

        display_name = ENGINE_NAMES.get(
            engine_name,
            engine_name
        )

        if trust_score_value >= 80:
            explanation = (
                f"{display_name} provided strong "
                f"positive evidence."
            )

        elif trust_score_value >= 50:
            explanation = (
                f"{display_name} provided mixed or "
                f"moderate evidence."
            )

        else:
            explanation = (
                f"{display_name} provided negative "
                f"evidence."
            )

        engine_explanations.append({
            "engine": engine_name,
            "name": display_name,
            "trust_score": trust_score_value,
            "explanation": explanation
        })

    # =================================================
    # POSITIVE FINDINGS
    # =================================================

    positive_findings = []

    for signal in rule_result.get(
        "positive_signals",
        []
    ):
        positive_findings.append(signal)

    # =================================================
    # NEGATIVE FINDINGS
    # =================================================

    negative_findings = []

    for signal in rule_result.get(
        "negative_signals",
        []
    ):
        negative_findings.append(signal)

    # =================================================
    # UNCERTAIN FINDINGS
    # =================================================

    uncertain_findings = []

    for signal in rule_result.get(
        "uncertain_signals",
        []
    ):
        uncertain_findings.append(signal)

    # =================================================
    # CONFLICT INFORMATION
    # =================================================

    conflict_detected = conflict_result.get(
        "conflict_detected",
        False
    )

    conflicts = conflict_result.get(
        "conflicts",
        []
    )

    resolution_reasons = conflict_result.get(
        "resolution_reasons",
        []
    )

    # =================================================
    # RISK FINDINGS
    # =================================================

    risk_findings = []

    if decision == HIGH_RISK:
        risk_findings.append(
            "The overall trust assessment indicates "
            "high risk."
        )

    if conflict_detected:
        risk_findings.append(
            "The engines produced conflicting "
            "risk assessments."
        )

    for reason in resolution_reasons:
        risk_findings.append(reason)

    # =================================================
    # EVIDENCE COVERAGE
    # =================================================

    available_engine_count = score_result.get(
        "available_engine_count",
        0
    )

    if available_engine_count < 4:
        uncertain_findings.append(
            f"Only {available_engine_count} of "
            f"4 engines provided usable score evidence."
        )

    # =================================================
    # CONFIDENCE EXPLANATION
    # =================================================

    if confidence >= 75:
        confidence_explanation = (
            "High evidence coverage is available "
            "from the verification engines."
        )

    elif confidence >= 50:
        confidence_explanation = (
            "Moderate evidence coverage is available; "
            "some verification evidence is missing."
        )

    else:
        confidence_explanation = (
            "Limited evidence is available, so the "
            "decision should be interpreted cautiously."
        )

    # =================================================
    # FINAL RESULT
    # =================================================

    return {
        "summary": summary,
        "decision": decision,
        "trust_score": trust_score,
        "confidence": confidence,
        "confidence_explanation": confidence_explanation,
        "engine_explanations": engine_explanations,
        "positive_findings": positive_findings,
        "negative_findings": negative_findings,
        "uncertain_findings": uncertain_findings,
        "risk_findings": risk_findings,
        "conflict_detected": conflict_detected,
        "conflicts": conflicts,
        "resolution_reasons": resolution_reasons
    }