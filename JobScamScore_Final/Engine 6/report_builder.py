"""
Engine 6 - Report Builder

Builds the final structured report from the results
already produced by Engine 5 and Engine 6 components.

This module does not perform new analysis.
"""


# =====================================================
# REPORT STATUS
# =====================================================

REPORT_COMPLETE = "COMPLETE"
REPORT_PARTIAL = "PARTIAL"
REPORT_UNAVAILABLE = "UNAVAILABLE"


# =====================================================
# MAIN REPORT BUILDER
# =====================================================

def build_trust_report(
    engine5_result,
    trust_score_result,
    risk_result,
    explanation_result
):
    """
    Builds the final Engine 6 report.

    Parameters
    ----------
    engine5_result : dict
        Complete result from Engine 5.

    trust_score_result : dict
        Result from trust_score_calculator.py.

    risk_result : dict
        Result from risk_classifier.py.

    explanation_result : dict
        Result from explanation_generator.py.

    Returns
    -------
    dict
        Final structured trust report.
    """

    if not isinstance(engine5_result, dict):
        engine5_result = {}

    if not isinstance(trust_score_result, dict):
        trust_score_result = {}

    if not isinstance(risk_result, dict):
        risk_result = {}

    if not isinstance(explanation_result, dict):
        explanation_result = {}

    # =================================================
    # BASIC VALUES
    # =================================================

    trust_score = trust_score_result.get(
        "trust_score"
    )

    decision = trust_score_result.get(
        "decision",
        "REVIEW"
    )

    risk = risk_result.get(
        "risk",
        "UNKNOWN"
    )

    confidence = trust_score_result.get(
        "confidence"
    )

    if confidence is None:
        confidence = explanation_result.get(
            "confidence",
            0
        )

    # =================================================
    # REPORT STATUS
    # =================================================

    report_status = _determine_report_status(
        trust_score,
        risk,
        engine5_result
    )

    # =================================================
    # FINAL REPORT
    # =================================================

    report = {
        "report_status": report_status,

        "trust_assessment": {
            "trust_score": trust_score,
            "decision": decision,
            "risk": risk,
            "confidence": confidence
        },

        "summary": explanation_result.get(
            "summary",
            ""
        ),

        "confidence_explanation": (
            explanation_result.get(
                "confidence_explanation",
                ""
            )
        ),

        "engine_findings": (
            explanation_result.get(
                "engine_findings",
                []
            )
        ),

        "positive_findings": (
            explanation_result.get(
                "positive_findings",
                []
            )
        ),

        "negative_findings": (
            explanation_result.get(
                "negative_findings",
                []
            )
        ),

        "uncertain_findings": (
            explanation_result.get(
                "uncertain_findings",
                []
            )
        ),

        "conflict_findings": (
            explanation_result.get(
                "conflict_findings",
                []
            )
        ),

        "recommendation": (
            explanation_result.get(
                "recommendation",
                ""
            )
        )
    }

    return report


# =====================================================
# REPORT STATUS
# =====================================================

def _determine_report_status(
    trust_score,
    risk,
    engine5_result
):
    """
    Determines whether the final report is complete,
    partial, or unavailable.
    """

    # No final score means a complete assessment
    # could not be produced.
    if trust_score is None:
        return REPORT_UNAVAILABLE

    # Check Engine 5 evidence coverage.
    data = engine5_result.get(
        "data",
        {}
    )

    if isinstance(data, dict):

        evidence = data.get(
            "evidence",
            {}
        )

        if isinstance(evidence, dict):

            summary = evidence.get(
                "summary",
                {}
            )

            if isinstance(summary, dict):

                available_count = summary.get(
                    "available_engine_count",
                    0
                )

                if available_count < 4:
                    return REPORT_PARTIAL

    # Unknown risk also indicates incomplete
    # classification.
    if risk == "UNKNOWN":
        return REPORT_PARTIAL

    return REPORT_COMPLETE