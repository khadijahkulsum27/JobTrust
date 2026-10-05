"""
Engine 6 - Trust Score + Explainable AI Report Engine

Main orchestrator for Engine 6.

Engine 6 receives the final decision from Engine 5,
calculates/presents the final trust score, classifies
risk, generates explanations, and builds the final
structured report.

It does not repeat the analysis performed by
Engines 1-5.
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
    ENGINE_TRUST_REPORT,
    STATUS_SUCCESS,
    STATUS_FAILED
)

from utils.response_builder import create_engine_response

from trust_score_calculator import (
    calculate_trust_score
)

from risk_classifier import (
    classify_risk
)

from explanation_generator import (
    generate_explanation
)

from report_builder import (
    build_trust_report
)


# =====================================================
# MAIN ENGINE FUNCTION
# =====================================================

def run_trust_report_engine(engine5_result=None):
    """
    Runs the complete Engine 6 process.

    Parameters
    ----------
    engine5_result : dict
        Complete result from Engine 5.

    Returns
    -------
    dict
        Standardized Engine 6 response.
    """

    response = create_engine_response(
        ENGINE_TRUST_REPORT
    )

    try:

        # =================================================
        # VALIDATE INPUT
        # =================================================

        if not isinstance(engine5_result, dict):

            response["status"] = STATUS_FAILED

            response["errors"].append(
                "Engine 5 result must be a dictionary."
            )

            return response

        # =================================================
        # STEP 1 - CALCULATE / VALIDATE TRUST SCORE
        # =================================================

        trust_score_result = calculate_trust_score(
            engine5_result
        )

        trust_score = trust_score_result.get(
            "trust_score"
        )

        decision = trust_score_result.get(
            "decision",
            "REVIEW"
        )

        # =================================================
        # STEP 2 - CLASSIFY RISK
        # =================================================

        risk_result = classify_risk(
            trust_score,
            decision
        )

        # =================================================
        # STEP 3 - GENERATE EXPLANATION
        # =================================================

        explanation_result = generate_explanation(
            engine5_result,
            trust_score_result,
            risk_result
        )

        # =================================================
        # STEP 4 - BUILD FINAL REPORT
        # =================================================

        report = build_trust_report(
            engine5_result,
            trust_score_result,
            risk_result,
            explanation_result
        )

        # =================================================
        # STANDARD RESPONSE
        # =================================================

        response["status"] = STATUS_SUCCESS

        response["score"] = trust_score

        response["risk"] = risk_result.get(
            "risk",
            "UNKNOWN"
        )

        response["data"] = report

        # =================================================
        # REMARKS
        # =================================================

        response["remarks"] = []

        if explanation_result.get(
            "summary"
        ):
            response["remarks"].append(
                explanation_result["summary"]
            )

        if explanation_result.get(
            "recommendation"
        ):
            response["remarks"].append(
                explanation_result["recommendation"]
            )

        return response

    except Exception as exc:

        response["status"] = STATUS_FAILED

        response["errors"].append(
            f"Trust report engine error: {str(exc)}"
        )

        return response


# =====================================================
# ENGINE ALIAS
# =====================================================

run_engine = run_trust_report_engine

if __name__ == "__main__":
    test_result = run_trust_report_engine(
        engine5_result={}
    )

    print(test_result)