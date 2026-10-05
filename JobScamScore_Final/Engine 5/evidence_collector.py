"""
Engine 5 - Evidence Collector

Collects and normalizes the outputs from Engines 1-4
so that the Trust Decision Engine can evaluate them
consistently.
"""


def collect_evidence(
    engine1_result=None,
    engine2_result=None,
    engine3_result=None,
    engine4_result=None
):
    """
    Collect evidence from Engines 1-4.

    Args:
        engine1_result (dict): Digital Identity Engine result.
        engine2_result (dict): Job Content Analysis Engine result.
        engine3_result (dict): Job Posting Intelligence Engine result.
        engine4_result (dict): Cyber Threat Intelligence Engine result.

    Returns:
        dict: Normalized evidence structure.
    """

    # -----------------------------------------
    # Safely handle missing engine results
    # -----------------------------------------

    engine1_result = (
        engine1_result
        if isinstance(engine1_result, dict)
        else {}
    )

    engine2_result = (
        engine2_result
        if isinstance(engine2_result, dict)
        else {}
    )

    engine3_result = (
        engine3_result
        if isinstance(engine3_result, dict)
        else {}
    )

    engine4_result = (
        engine4_result
        if isinstance(engine4_result, dict)
        else {}
    )

    # -----------------------------------------
    # Extract basic scores
    # -----------------------------------------

    evidence = {
        "engine_1": {
            "status": engine1_result.get(
                "status"
            ),
            "score": engine1_result.get(
                "score"
            ),
            "risk": engine1_result.get(
                "risk"
            ),
            "data": engine1_result.get(
                "data",
                {}
            ),
            "remarks": engine1_result.get(
                "remarks",
                []
            ),
            "errors": engine1_result.get(
                "errors",
                []
            )
        },

        "engine_2": {
            "status": engine2_result.get(
                "status"
            ),
            "score": engine2_result.get(
                "score"
            ),
            "risk": engine2_result.get(
                "risk"
            ),
            "data": engine2_result.get(
                "data",
                {}
            ),
            "remarks": engine2_result.get(
                "remarks",
                []
            ),
            "errors": engine2_result.get(
                "errors",
                []
            )
        },

        "engine_3": {
            "status": engine3_result.get(
                "status"
            ),
            "score": engine3_result.get(
                "score"
            ),
            "risk": engine3_result.get(
                "risk"
            ),
            "data": engine3_result.get(
                "data",
                {}
            ),
            "remarks": engine3_result.get(
                "remarks",
                []
            ),
            "errors": engine3_result.get(
                "errors",
                []
            )
        },

        "engine_4": {
            "status": engine4_result.get(
                "status"
            ),
            "score": engine4_result.get(
                "score"
            ),
            "risk": engine4_result.get(
                "risk"
            ),
            "data": engine4_result.get(
                "data",
                {}
            ),
            "remarks": engine4_result.get(
                "remarks",
                []
            ),
            "errors": engine4_result.get(
                "errors",
                []
            )
        }
    }

    # -----------------------------------------
    # Evidence availability
    # -----------------------------------------

    available_engines = []
    unavailable_engines = []

    for engine_name, engine_data in evidence.items():

        if engine_data.get("score") is not None:

            available_engines.append(
                engine_name
            )

        else:

            unavailable_engines.append(
                engine_name
            )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    evidence["summary"] = {
        "available_engine_count": len(
            available_engines
        ),
        "unavailable_engine_count": len(
            unavailable_engines
        ),
        "available_engines": available_engines,
        "unavailable_engines": unavailable_engines
    }

    return evidence