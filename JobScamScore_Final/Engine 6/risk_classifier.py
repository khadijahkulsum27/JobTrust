"""
Engine 6 - Risk Classifier

Converts the final trust score and Engine 5 decision
into a clear risk classification.
"""

from utils.constants import (
    TRUST_HIGH,
    TRUST_MEDIUM,
    TRUST_LOW
)


# =====================================================
# RISK LABELS
# =====================================================

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_UNKNOWN = "UNKNOWN"


# =====================================================
# MAIN CLASSIFIER
# =====================================================

def classify_risk(trust_score, decision=None):
    """
    Classifies the final result into LOW, MEDIUM,
    HIGH, or UNKNOWN risk.

    Parameters
    ----------
    trust_score : int or float
        Final trust score from Engine 6.

    decision : str, optional
        Decision produced by Engine 5.

    Returns
    -------
    dict
        Risk classification result.
    """

    # -------------------------------------------------
    # Validate score
    # -------------------------------------------------

    if trust_score is None:

        return {
            "risk": RISK_UNKNOWN,
            "risk_level": None,
            "classification_basis": "NO_SCORE"
        }

    try:
        trust_score = float(trust_score)

    except (TypeError, ValueError):

        return {
            "risk": RISK_UNKNOWN,
            "risk_level": None,
            "classification_basis": "INVALID_SCORE"
        }

    # Keep score within valid range.
    trust_score = max(
        TRUST_LOW,
        min(trust_score, 100)
    )

    # -------------------------------------------------
    # Score-based classification
    #
    # 80-100 = LOW risk
    # 50-79  = MEDIUM risk
    # 0-49   = HIGH risk
    # -------------------------------------------------

    if trust_score >= TRUST_HIGH:

        risk = RISK_LOW
        risk_level = 1

    elif trust_score >= TRUST_MEDIUM:

        risk = RISK_MEDIUM
        risk_level = 2

    else:

        risk = RISK_HIGH
        risk_level = 3

    # -------------------------------------------------
    # Engine 5 decision consistency
    #
    # Engine 5 can conservatively classify a result
    # as HIGH_RISK because of a serious conflict even
    # when the numerical average is higher.
    # -------------------------------------------------

    if decision == "HIGH_RISK":

        risk = RISK_HIGH
        risk_level = 3
        classification_basis = (
            "ENGINE_5_HIGH_RISK_DECISION"
        )

    elif decision == "REVIEW":

        # Do not downgrade a numerical HIGH risk.
        if risk != RISK_HIGH:
            risk = RISK_MEDIUM
            risk_level = 2

        classification_basis = (
            "SCORE_AND_ENGINE_5_REVIEW"
        )

    elif decision == "TRUSTED":

        # Do not override a numerical HIGH risk.
        if risk != RISK_HIGH:
            risk = RISK_LOW
            risk_level = 1

        classification_basis = (
            "SCORE_AND_ENGINE_5_TRUSTED"
        )

    else:

        classification_basis = (
            "SCORE_ONLY"
        )

    # -------------------------------------------------
    # Final result
    # -------------------------------------------------

    return {
        "risk": risk,
        "risk_level": risk_level,
        "classification_basis": classification_basis
    }