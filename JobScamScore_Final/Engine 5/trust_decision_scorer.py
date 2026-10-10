"""
Engine 5 - Trust Decision Scorer

Combines the normalized trust evidence from Engines 1-4
into one overall trust score and decision.

Important:
Engines 1-3 use a TRUST score:
    Higher score = more trustworthy

Engine 4 uses a CYBER RISK score:
    Higher score = more risky

Therefore Engine 4 is inverted before combining:
    trust_score = 100 - cyber_risk_score
"""

from utils.constants import (
    TRUST_HIGH,
    TRUST_MEDIUM,
    TRUST_LOW
)


# =====================================================
# INTERNAL CONSTANTS
# =====================================================

TOTAL_ENGINES = 4

ENGINE_1 = "engine_1"
ENGINE_2 = "engine_2"
ENGINE_3 = "engine_3"
ENGINE_4 = "engine_4"

TRUSTED = "TRUSTED"
REVIEW = "REVIEW"
HIGH_RISK = "HIGH_RISK"

UNKNOWN = "UNKNOWN"


# =====================================================
# SCORE NORMALIZATION
# =====================================================

def _normalize_score(engine_name, score):
    """
    Converts every engine score into a TRUST score
    where:

        0   = very low trust
        100 = very high trust

    Engine 4 is different because it produces a
    cyber RISK score where a higher value means
    greater risk.

    Therefore Engine 4 is inverted.
    """

    if score is None:
        return None

    try:
        score = float(score)
    except (TypeError, ValueError):
        return None

    # Keep score safely within 0-100.
    score = max(0.0, min(score, 100.0))

    # Engine 4 = cyber risk score.
    # Convert risk into trust.
    if engine_name == ENGINE_4:
        return round(100.0 - score, 2)

    # Engines 1-3 = trust scores.
    return round(score, 2)


# =====================================================
# DECISION CLASSIFICATION
# =====================================================

def _classify_score(trust_score):
    """
    Converts an overall trust score into a basic
    trust classification.
    """

    if trust_score is None:
        return REVIEW

    if trust_score >= TRUST_HIGH:
        return TRUSTED

    if trust_score >= TRUST_MEDIUM:
        return REVIEW

    if trust_score >= TRUST_LOW:
        return HIGH_RISK

    return HIGH_RISK


# =====================================================
# MAIN SCORING FUNCTION
# =====================================================

def calculate_trust_decision_score(
    evidence,
    conflict_result=None
):
    """
    Calculates the final Engine 5 trust score.

    Parameters
    ----------
    evidence : dict
        Evidence collected from Engines 1-4.

    conflict_result : dict, optional
        Result from conflict_resolver.py.

    Returns
    -------
    dict
        Standardized Engine 5 scoring result.
    """

    if not isinstance(evidence, dict):
        return {
            "trust_score": None,
            "decision": REVIEW,
            "confidence": 0,
            "engine_scores": {},
            "normalized_scores": {},
            "available_engine_count": 0,
            "scoring_status": "NO_EVIDENCE"
        }

    normalized_scores = {}
    engine_scores = {}

    # -------------------------------------------------
    # Normalize Engines 1-4
    # -------------------------------------------------

    for engine_name in (
        ENGINE_1,
        ENGINE_2,
        ENGINE_3,
        ENGINE_4
    ):
        engine_data = evidence.get(engine_name, {})

        if not isinstance(engine_data, dict):
            continue

        original_score = engine_data.get("score")

        if original_score is None:
            continue

        normalized_score = _normalize_score(
            engine_name,
            original_score
        )

        if normalized_score is None:
            continue

        engine_scores[engine_name] = original_score
        normalized_scores[engine_name] = normalized_score

    # -------------------------------------------------
    # No usable evidence
    # -------------------------------------------------

    if not normalized_scores:
        return {
            "trust_score": None,
            "decision": REVIEW,
            "confidence": 0,
            "engine_scores": {},
            "normalized_scores": {},
            "available_engine_count": 0,
            "scoring_status": "NO_EVIDENCE"
        }

    # -------------------------------------------------
    # Calculate average trust score
    # -------------------------------------------------

    total_score = sum(normalized_scores.values())
    available_count = len(normalized_scores)

        # Engines that did not run count as 0, so the score is always out of all 4 engines.
    trust_score = total_score / TOTAL_ENGINES
    trust_score = round(
        max(0.0, min(trust_score, 100.0)),
        2
    )

    # -------------------------------------------------
    # Evidence confidence
    #
    # 4 available engines = 100% evidence coverage
    # 2 available engines = 50% evidence coverage
    # -------------------------------------------------

    confidence = round(
        (available_count / TOTAL_ENGINES) * 100,
        2
    )

    # -------------------------------------------------
    # Basic decision from score
    # -------------------------------------------------

    decision = _classify_score(trust_score)

    # -------------------------------------------------
    # Apply conflict resolution
    #
    # Engine 5 is deliberately conservative.
    # A HIGH resolved risk must not be labelled
    # TRUSTED merely because the average score is high.
    # -------------------------------------------------

    resolved_risk = UNKNOWN

    if isinstance(conflict_result, dict):
        resolved_risk = conflict_result.get(
            "resolved_risk",
            UNKNOWN
        )

    if resolved_risk == "HIGH":
        decision = HIGH_RISK

    elif resolved_risk == "MEDIUM":
        if decision == TRUSTED:
            decision = REVIEW

    # Evidence coverage rule: TRUSTED needs all 4 engines to have scored.
    if available_count < TOTAL_ENGINES and decision == TRUSTED:
        decision = REVIEW
        
    # -------------------------------------------------
    # Final result
    # -------------------------------------------------

    return {
        "trust_score": trust_score,
        "decision": decision,
        "confidence": confidence,
        "engine_scores": engine_scores,
        "normalized_scores": normalized_scores,
        "available_engine_count": available_count,
        "scoring_status": "SUCCESS"
    }