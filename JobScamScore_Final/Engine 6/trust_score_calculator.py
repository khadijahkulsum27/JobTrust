"""
Engine 6 - Trust Score Calculator

Calculates the final user-facing trust score
from the Engine 5 Trust Decision result.

Engine 6 does not repeat the analysis performed
by Engines 1-5.
"""


# =====================================================
# INTERNAL CONSTANTS
# =====================================================

MIN_SCORE = 0
MAX_SCORE = 100

TRUSTED = "TRUSTED"
REVIEW = "REVIEW"
HIGH_RISK = "HIGH_RISK"


# =====================================================
# SCORE EXTRACTION
# =====================================================

def _extract_engine5_score(engine5_result):
    """
    Extracts the trust score produced by Engine 5.
    """

    if not isinstance(engine5_result, dict):
        return None

    # Standard Engine 5 response.
    score = engine5_result.get("score")

    if score is not None:
        try:
            return float(score)
        except (TypeError, ValueError):
            pass

    # Fallback for direct Engine 5 scoring output.
    score = engine5_result.get("trust_score")

    if score is not None:
        try:
            return float(score)
        except (TypeError, ValueError):
            pass

    # Fallback if the score is inside Engine 5 data.
    data = engine5_result.get("data", {})

    if isinstance(data, dict):

        score_analysis = data.get(
            "score_analysis",
            {}
        )

        if isinstance(score_analysis, dict):
            score = score_analysis.get(
                "trust_score"
            )

            if score is not None:
                try:
                    return float(score)
                except (TypeError, ValueError):
                    pass

    return None


# =====================================================
# SCORE NORMALIZATION
# =====================================================

def _normalize_score(score):
    """
    Keeps the final trust score within 0-100.
    """

    if score is None:
        return None

    score = max(
        MIN_SCORE,
        min(score, MAX_SCORE)
    )

    return round(score, 2)


# =====================================================
# DECISION EXTRACTION
# =====================================================

def _extract_decision(engine5_result):
    """
    Extracts the decision produced by Engine 5.
    """

    if not isinstance(engine5_result, dict):
        return None

    data = engine5_result.get("data", {})

    if isinstance(data, dict):

        decision = data.get("decision")

        if decision:
            return decision

        score_analysis = data.get(
            "score_analysis",
            {}
        )

        if isinstance(score_analysis, dict):
            decision = score_analysis.get(
                "decision"
            )

            if decision:
                return decision

    return engine5_result.get("decision")


# =====================================================
# MAIN CALCULATOR
# =====================================================

def calculate_trust_score(engine5_result):
    """
    Calculates the final Engine 6 trust score.

    Engine 5 has already combined the evidence.
    Engine 6 simply validates and presents that
    resulting trust score.

    Returns
    -------
    dict
        Final trust score information.
    """

    raw_score = _extract_engine5_score(
        engine5_result
    )

    decision = _extract_decision(
        engine5_result
    )

    # -------------------------------------------------
    # No valid score
    # -------------------------------------------------

    if raw_score is None:

        return {
            "trust_score": None,
            "decision": decision or REVIEW,
            "score_status": "UNAVAILABLE",
            "score_source": "ENGINE_5"
        }

    # -------------------------------------------------
    # Normalize score
    # -------------------------------------------------

    trust_score = _normalize_score(
        raw_score
    )

    # -------------------------------------------------
    # If Engine 5 did not provide a decision,
    # derive one from the score.
    # -------------------------------------------------

    if not decision:

        if trust_score >= 80:
            decision = TRUSTED

        elif trust_score >= 50:
            decision = REVIEW

        else:
            decision = HIGH_RISK

    # -------------------------------------------------
    # Final result
    # -------------------------------------------------

    return {
        "trust_score": trust_score,
        "decision": decision,
        "score_status": "SUCCESS",
        "score_source": "ENGINE_5"
    }