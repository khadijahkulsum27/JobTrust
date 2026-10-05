"""
Engine 5 - AI Trust Decision Engine

Main orchestrator for Engine 5.

This engine combines the outputs of Engines 1-4
and produces one overall trust decision.
"""
import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from utils.constants import (
    ENGINE_TRUST_DECISION,
    STATUS_SUCCESS,
    STATUS_FAILED
)

from utils.response_builder import create_engine_response

from evidence_collector import (
    collect_evidence
)

from trust_rule_engine import (
    evaluate_trust_rules
)

from conflict_resolver import (
    resolve_conflicts
)

from trust_decision_scorer import (
    calculate_trust_decision_score
)

from trust_decision_explanation import (
    generate_trust_decision_explanation
)


# =====================================================
# MAIN ENGINE FUNCTION
# =====================================================

def run_trust_decision_engine(
    engine1_result=None,
    engine2_result=None,
    engine3_result=None,
    engine4_result=None
):
    """
    Runs the complete Engine 5 Trust Decision process.

    Parameters
    ----------
    engine1_result : dict
        Result from Engine 1.

    engine2_result : dict
        Result from Engine 2.

    engine3_result : dict
        Result from Engine 3.

    engine4_result : dict
        Result from Engine 4.

    Returns
    -------
    dict
        Standardized Engine 5 response.
    """

    response = create_engine_response(
        ENGINE_TRUST_DECISION
    )

    try:

        # =================================================
        # STEP 1 - COLLECT EVIDENCE
        # =================================================

        evidence = collect_evidence(
            engine1_result=engine1_result,
            engine2_result=engine2_result,
            engine3_result=engine3_result,
            engine4_result=engine4_result
        )

        # =================================================
        # STEP 2 - EVALUATE TRUST RULES
        # =================================================

        rule_result = evaluate_trust_rules(
            evidence
        )

        # =================================================
        # STEP 3 - RESOLVE CONFLICTS
        # =================================================

        conflict_result = resolve_conflicts(
            evidence,
            rule_result
        )

        # =================================================
        # STEP 4 - CALCULATE TRUST SCORE
        # =================================================

        score_result = calculate_trust_decision_score(
            evidence,
            conflict_result
        )

        # =================================================
        # STEP 5 - GENERATE EXPLANATION
        # =================================================

        explanation_result = (
            generate_trust_decision_explanation(
                evidence,
                rule_result,
                conflict_result,
                score_result
            )
        )

        # =================================================
        # STANDARD RESPONSE
        # =================================================

        response["status"] = STATUS_SUCCESS

        response["score"] = score_result.get(
            "trust_score"
        )

        response["risk"] = _decision_to_risk(
            score_result.get("decision")
        )

        response["data"] = {
            "decision": score_result.get(
                "decision"
            ),
            "confidence": score_result.get(
                "confidence"
            ),
            "evidence": evidence,
            "rule_analysis": rule_result,
            "conflict_resolution": conflict_result,
            "score_analysis": score_result,
            "explanation": explanation_result
        }

        # =================================================
        # REMARKS
        # =================================================

        response["remarks"] = (
            explanation_result.get(
                "risk_findings",
                []
            )
            + explanation_result.get(
                "positive_findings",
                []
            )
            + explanation_result.get(
                "uncertain_findings",
                []
            )
        )

        return response

    except Exception as exc:

        response["status"] = STATUS_FAILED

        response["errors"].append(
            f"Trust decision engine error: {str(exc)}"
        )

        return response


# =====================================================
# DECISION → STANDARD RISK
# =====================================================

def _decision_to_risk(decision):
    """
    Converts Engine 5 decision labels into the
    standard risk labels used by the project.
    """

    if decision == "TRUSTED":
        return "LOW"

    if decision == "REVIEW":
        return "MEDIUM"

    if decision == "HIGH_RISK":
        return "HIGH"

    return "UNKNOWN"


# =====================================================
# ENGINE ALIAS
# =====================================================

run_engine = run_trust_decision_engine

if __name__ == "__main__":
    test_result = run_trust_decision_engine(
        engine1_result={},
        engine2_result={},
        engine3_result={},
        engine4_result={}
    )

    print(test_result)