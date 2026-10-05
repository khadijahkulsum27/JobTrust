"""
data_standardizer.py

Standardizes extracted job data into a common format
used throughout the AI Job Trust Platform.
"""

import uuid
from datetime import datetime

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_PROCESSING
)


def standardize_data(
    extracted_data,
    source_type
):
    """
    Standardizes extracted job data.

    Parameters:
        extracted_data (dict)
        source_type (str)

    Returns:
        dict
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        data = extracted_data.get("data", {})

        standardized_data = {

            "company_name":
                str(
                    data.get(
                        "company_name",
                        ""
                    )
                ).strip(),

            "website":
                str(
                    data.get(
                        "website",
                        ""
                    )
                ).strip(),

            "email":
                str(
                    data.get(
                        "email",
                        ""
                    )
                ).strip(),

            "job_title":
                str(
                    data.get(
                        "job_title",
                        ""
                    )
                ).strip(),

            "job_description":
                str(
                    data.get(
                        "job_description",
                        ""
                    )
                ).strip(),

            "salary":
                str(
                    data.get(
                        "salary",
                        ""
                    )
                ).strip(),

            "location":
                str(
                    data.get(
                        "location",
                        ""
                    )
                ).strip(),

            "experience":
                str(
                    data.get(
                        "experience",
                        ""
                    )
                ).strip(),

            "employment_type":
                str(
                    data.get(
                        "employment_type",
                        ""
                    )
                ).strip(),

            "skills":
                data.get(
                    "skills",
                    []
                ),

            "contact_number":
                str(
                    data.get(
                        "contact_number",
                        ""
                    )
                ).strip(),

            "application_deadline":
                str(
                    data.get(
                        "application_deadline",
                        ""
                    )
                ).strip(),

            "source_type":
                source_type,

            "raw_text":
                str(
                    data.get(
                        "raw_text",
                        ""
                    )
                ).strip(),

            "metadata":
                data.get(
                    "metadata",
                    {
                        "page_title": "",
                        "meta_description": ""
                    }
                ),
            "processing_id":
                str(uuid.uuid4()),
            "processed_timestamp":
                datetime.now().isoformat()
        }

        result["status"] = STATUS_SUCCESS

        result["risk"] = RISK_LOW

        result["data"] = standardized_data

        result["remarks"].append(
            "Job data standardized successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED

        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result