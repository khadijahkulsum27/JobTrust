"""
Engine 6 - Explanation Generator

Creates the final human-readable explanation
from Engine 5 and Engine 6 results.

This module does not perform new threat or scam
analysis. It explains the results already produced.
"""


# =====================================================
# DECISION LABELS
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

def generate_explanation(
    engine5_result,
    trust_score_result,
    risk_result
):
    """
    Generates the final explainable report content.

    Parameters
    ----------
    engine5_result : dict
        Complete result from Engine 5.

    trust_score_result : dict
        Result from trust_score_calculator.py.

    risk_result : dict
        Result from risk_classifier.py.

    Returns
    -------
    dict
        Explainable report information.
    """

    if not isinstance(engine5_result, dict):
        engine5_result = {}

    if not isinstance(trust_score_result, dict):
        trust_score_result = {}

    if not isinstance(risk_result, dict):
        risk_result = {}

    # =================================================
    # BASIC VALUES
    # =================================================

    trust_score = trust_score_result.get(
        "trust_score"
    )

    decision = trust_score_result.get(
        "decision",
        REVIEW
    )

    risk = risk_result.get(
        "risk",
        "UNKNOWN"
    )

    confidence = _extract_confidence(
        engine5_result
    )

    # =================================================
    # SUMMARY
    # =================================================

    summary = _build_summary(
        trust_score,
        decision,
        risk
    )

    # =================================================
    # ENGINE FINDINGS
    # =================================================

    engine_findings = _build_engine_findings(
        engine5_result
    )

    # =================================================
    # POSITIVE FINDINGS
    # =================================================

    positive_findings = _extract_findings(
        engine5_result,
        "positive_findings"
    )

    # =================================================
    # NEGATIVE FINDINGS
    # =================================================

    negative_findings = _extract_findings(
        engine5_result,
        "negative_findings"
    )

    # =================================================
    # UNCERTAIN FINDINGS
    # =================================================

    uncertain_findings = _extract_findings(
        engine5_result,
        "uncertain_findings"
    )

    # =================================================
    # CONFLICT FINDINGS
    # =================================================

    conflict_findings = _build_conflict_findings(
        engine5_result
    )

    # =================================================
    # RECOMMENDATION
    # =================================================

    recommendation = _build_recommendation(
        decision,
        risk
    )

    # =================================================
    # CONFIDENCE EXPLANATION
    # =================================================

    confidence_explanation = (
        _build_confidence_explanation(
            confidence
        )
    )

    # =================================================
    # FINAL EXPLANATION
    # =================================================

    return {
        "summary": summary,
        "trust_score": trust_score,
        "decision": decision,
        "risk": risk,
        "confidence": confidence,
        "confidence_explanation": confidence_explanation,
        "engine_findings": engine_findings,
        "positive_findings": positive_findings,
        "negative_findings": negative_findings,
        "uncertain_findings": uncertain_findings,
        "conflict_findings": conflict_findings,
        "recommendation": recommendation
    }


# =====================================================
# SUMMARY BUILDER
# =====================================================

def _build_summary(
    trust_score,
    decision,
    risk
):
    """
    Creates a short overall explanation.
    """

    if trust_score is None:

        return (
            "A final trust score could not be "
            "calculated because sufficient scoring "
            "evidence was unavailable."
        )

    if decision == TRUSTED:

        return (
            f"The job posting received a trust score "
            f"of {trust_score}/100 and is assessed as "
            f"generally trustworthy based on the "
            f"available verification evidence."
        )

    if decision == HIGH_RISK:

        return (
            f"The job posting received a trust score "
            f"of {trust_score}/100 and is assessed as "
            f"high risk based on the available "
            f"verification evidence."
        )

    return (
        f"The job posting received a trust score "
        f"of {trust_score}/100 and requires further "
        f"review because the available evidence is "
        f"mixed, incomplete, or uncertain."
    )


# =====================================================
# ENGINE FINDINGS
# =====================================================

def _build_engine_findings(engine5_result):
    """
    Converts Engine 5's engine explanations into
    a clean Engine 6 format.
    """

    data = engine5_result.get(
        "data",
        {}
    )

    if not isinstance(data, dict):
        return []

    explanation = data.get(
        "explanation",
        {}
    )

    if not isinstance(explanation, dict):
        return []

    findings = explanation.get(
        "engine_explanations",
        []
    )

    if not isinstance(findings, list):
        return []

    formatted_findings = []

    for finding in findings:

        if not isinstance(finding, dict):
            continue

        engine = finding.get(
            "engine",
            "unknown"
        )

        formatted_findings.append({
            "engine": engine,
            "name": finding.get(
                "name",
                ENGINE_NAMES.get(
                    engine,
                    engine
                )
            ),
            "trust_score": finding.get(
                "trust_score"
            ),
            "explanation": finding.get(
                "explanation",
                ""
            )
        })

    return formatted_findings


# =====================================================
# FINDING EXTRACTION
# =====================================================

def _extract_findings(
    engine5_result,
    finding_type
):
    """
    Extracts positive, negative, or uncertain
    findings from Engine 5.
    """

    data = engine5_result.get(
        "data",
        {}
    )

    if not isinstance(data, dict):
        return []

    explanation = data.get(
        "explanation",
        {}
    )

    if not isinstance(explanation, dict):
        return []

    findings = explanation.get(
        finding_type,
        []
    )

    if not isinstance(findings, list):
        return []

    return [
        str(finding)
        for finding in findings
        if finding is not None
    ]


# =====================================================
# CONFLICT FINDINGS
# =====================================================

def _build_conflict_findings(engine5_result):
    """
    Extracts conflict information from Engine 5.
    """

    data = engine5_result.get(
        "data",
        {}
    )

    if not isinstance(data, dict):
        return []

    conflict_data = data.get(
        "conflict_resolution",
        {}
    )

    if not isinstance(conflict_data, dict):
        return []

    findings = []

    if conflict_data.get(
        "conflict_detected",
        False
    ):
        findings.append(
            "The verification engines produced "
            "different risk assessments."
        )

    for reason in conflict_data.get(
        "resolution_reasons",
        []
    ):
        if reason:
            findings.append(
                str(reason)
            )

    return findings


# =====================================================
# RECOMMENDATION
# =====================================================

def _build_recommendation(
    decision,
    risk
):
    """
    Produces a simple user-facing recommendation.
    """

    if decision == TRUSTED and risk == "LOW":

        return (
            "The available evidence does not indicate "
            "significant risk. Normal verification "
            "checks should still be followed before "
            "taking action."
        )

    if decision == HIGH_RISK or risk == "HIGH":

        return (
            "The posting shows significant risk "
            "indicators. Additional verification "
            "should be completed before relying on "
            "the posting."
        )

    return (
        "The evidence is not conclusive. Review the "
        "identified findings and obtain additional "
        "verification before making a decision."
    )


# =====================================================
# CONFIDENCE EXTRACTION
# =====================================================

def _extract_confidence(engine5_result):
    """
    Extracts evidence confidence from Engine 5.
    """

    data = engine5_result.get(
        "data",
        {}
    )

    if not isinstance(data, dict):
        return 0

    confidence = data.get(
        "confidence"
    )

    if confidence is None:
        score_analysis = data.get(
            "score_analysis",
            {}
        )

        if isinstance(score_analysis, dict):
            confidence = score_analysis.get(
                "confidence",
                0
            )

    try:
        confidence = float(confidence)

    except (TypeError, ValueError):
        return 0

    return round(
        max(0, min(confidence, 100)),
        2
    )


# =====================================================
# CONFIDENCE EXPLANATION
# =====================================================

def _build_confidence_explanation(
    confidence
):
    """
    Converts evidence coverage into a simple
    explanation.
    """

    if confidence >= 75:

        return (
            "Most verification engines provided "
            "usable evidence."
        )

    if confidence >= 50:

        return (
            "Some verification evidence is available, "
            "but additional evidence would improve "
            "confidence."
        )

    return (
        "Limited verification evidence is available; "
        "the result should be interpreted cautiously."
    )