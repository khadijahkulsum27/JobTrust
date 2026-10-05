from utils.constants import STATUS_FAILED, RISK_UNKNOWN


def create_engine_response(engine_name):
    """
    Creates a standard response structure for every engine/module.
    """

    return {
        "engine": engine_name,
        "status": STATUS_FAILED,
        "score": None,
        "risk": RISK_UNKNOWN,
        "data": {},
        "remarks": [],
        "errors": []
    }