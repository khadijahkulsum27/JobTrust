"""
Engine 4 - Cyber Threat Intelligence Engine

Main orchestration layer for Engine 4.

This module connects:
    URL Analyzer
    HTTPS Checker
    RDAP Checker
    Phishing Detector
    Threat Intelligence
    Cyber Risk Scorer
    Cyber Threat Explanation

and returns the standard project response format.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
print("PYTHON PATH:", sys.path)
print("HTTPS CHECKER EXISTS:", os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "https_checker.py")))
from utils.constants import (
    ENGINE_CYBER_THREAT,
    STATUS_SUCCESS,
    STATUS_FAILED,
)

from utils.response_builder import create_engine_response
print("ENGINE 4 FOLDER:", os.path.dirname(os.path.abspath(__file__)))
print("URL ANALYZER EXISTS:", os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_analyzer.py")))
    
import importlib.util

_url_analyzer_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "url_analyzer.py"
)

_spec = importlib.util.spec_from_file_location(
    "url_analyzer",
    _url_analyzer_path
)

_url_analyzer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_url_analyzer)

analyze_url = _url_analyzer.analyze_url

_https_checker_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "https_checker.py"
)

_https_spec = importlib.util.spec_from_file_location(
    "https_checker",
    _https_checker_path
)

_https_checker = importlib.util.module_from_spec(_https_spec)
_https_spec.loader.exec_module(_https_checker)

check_https = _https_checker.check_https

_rdap_checker_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rdap_checker.py"
)

_rdap_spec = importlib.util.spec_from_file_location(
    "rdap_checker",
    _rdap_checker_path
)

_rdap_checker = importlib.util.module_from_spec(_rdap_spec)
_rdap_spec.loader.exec_module(_rdap_checker)

check_rdap = _rdap_checker.check_rdap

_phishing_detector_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "phishing_detector.py"
)

_phishing_spec = importlib.util.spec_from_file_location(
    "phishing_detector",
    _phishing_detector_path
)

_phishing_detector = importlib.util.module_from_spec(_phishing_spec)
_phishing_spec.loader.exec_module(_phishing_detector)

detect_phishing = _phishing_detector.detect_phishing

_threat_intelligence_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "threat_intelligence.py"
)

_threat_spec = importlib.util.spec_from_file_location(
    "threat_intelligence",
    _threat_intelligence_path
)

_threat_intelligence = importlib.util.module_from_spec(_threat_spec)
_threat_spec.loader.exec_module(_threat_intelligence)

check_threat_intelligence = _threat_intelligence.check_threat_intelligence
_cyber_risk_scorer_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cyber_risk_scorer.py"
)

_cyber_risk_spec = importlib.util.spec_from_file_location(
    "cyber_risk_scorer",
    _cyber_risk_scorer_path
)

_cyber_risk_scorer = importlib.util.module_from_spec(_cyber_risk_spec)
_cyber_risk_spec.loader.exec_module(_cyber_risk_scorer)

calculate_cyber_risk = _cyber_risk_scorer.calculate_cyber_risk
_cyber_explanation_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cyber_threat_explanation.py"
)

_cyber_explanation_spec = importlib.util.spec_from_file_location(
    "cyber_threat_explanation",
    _cyber_explanation_path
)

_cyber_threat_explanation = importlib.util.module_from_spec(
    _cyber_explanation_spec
)

_cyber_explanation_spec.loader.exec_module(
    _cyber_threat_explanation
)

generate_cyber_explanation = (
    _cyber_threat_explanation.generate_cyber_explanation
)

def run_cyber_threat_engine(url):
    """
    Run the complete Engine 4 cyber-threat analysis.

    Args:
        url (str): Website URL to analyze.

    Returns:
        dict: Standard Engine 4 response.
    """

    response = create_engine_response(
        ENGINE_CYBER_THREAT
    )

    # -----------------------------------------
    # Input validation
    # -----------------------------------------

    if not isinstance(url, str) or not url.strip():

        response["status"] = STATUS_FAILED

        response["errors"].append(
            "A valid website URL is required."
        )

        return response

    url = url.strip()

    try:

        # =========================================
        # 1. URL ANALYSIS
        # =========================================

        url_result = analyze_url(url)

        # -----------------------------------------
        # Extract domain
        # -----------------------------------------

        domain = url_result.get(
            "domain"
        )

        # =========================================
        # 2. HTTPS CHECK
        # =========================================

        https_result = check_https(url)

        # =========================================
        # 3. RDAP CHECK
        # =========================================

        if domain:

            rdap_result = check_rdap(domain)

        else:

            rdap_result = {
                "status": "SKIPPED",
                "domain": None,
                "registered": False,
                "registration_date": None,
                "expiration_date": None,
                "last_changed": None,
                "domain_age_days": None,
                "domain_age_category": "UNKNOWN",
                "registrar": None,
                "indicators": [],
                "positive_indicators": [],
                "remarks": [
                    "RDAP check skipped because "
                    "a valid domain could not be extracted."
                ],
                "errors": []
            }

        # =========================================
        # 4. PHISHING DETECTION
        # =========================================

        phishing_result = detect_phishing(url)

        # =========================================
        # 5. THREAT INTELLIGENCE
        # =========================================

        threat_result = check_threat_intelligence(url)

        # =========================================
        # 6. CYBER RISK SCORING
        # =========================================

        scoring_result = calculate_cyber_risk(
            url_result,
            https_result,
            rdap_result,
            phishing_result,
            threat_result
        )

        score = scoring_result.get(
            "score",
            50
        )

        risk = scoring_result.get(
            "risk",
            "MEDIUM"
        )

        # =========================================
        # 7. EXPLANATION GENERATION
        # =========================================

        explanation = generate_cyber_explanation(
            url_result,
            https_result,
            rdap_result,
            phishing_result,
            threat_result,
            score,
            risk
        )

        # =========================================
        # STANDARD RESPONSE
        # =========================================

        response["status"] = STATUS_SUCCESS
        response["score"] = score
        response["risk"] = risk

        response["data"] = {
            "url": url,

            "url_analysis": url_result,

            "https_check": https_result,

            "rdap_check": rdap_result,

            "phishing_detection": phishing_result,

            "threat_intelligence": threat_result,

            "risk_components": scoring_result.get(
                "components",
                {}
            ),

            "explanation": explanation
        }

        # =========================================
        # COLLECT REMARKS
        # =========================================

        response["remarks"].extend(
            url_result.get(
                "remarks",
                []
            )
        )

        response["remarks"].extend(
            https_result.get(
                "remarks",
                []
            )
        )

        response["remarks"].extend(
            rdap_result.get(
                "remarks",
                []
            )
        )

        response["remarks"].extend(
            phishing_result.get(
                "remarks",
                []
            )
        )

        response["remarks"].extend(
            threat_result.get(
                "remarks",
                []
            )
        )

        # =========================================
        # COLLECT ERRORS
        # =========================================

        response["errors"].extend(
            url_result.get(
                "errors",
                []
            )
        )

        response["errors"].extend(
            https_result.get(
                "errors",
                []
            )
        )

        response["errors"].extend(
            rdap_result.get(
                "errors",
                []
            )
        )

        response["errors"].extend(
            phishing_result.get(
                "errors",
                []
            )
        )

        response["errors"].extend(
            threat_result.get(
                "errors",
                []
            )
        )

        return response

    except Exception as exc:

        response["status"] = STATUS_FAILED

        response["errors"].append(
            f"Cyber Threat Engine failed: {str(exc)}"
        )

        return response


# ---------------------------------------------
# Alias for integration convenience
# ---------------------------------------------

run_engine = run_cyber_threat_engine
if __name__ == "__main__":
    test_result = run_cyber_threat_engine(
        "https://example.com"
    )

    print(test_result)