"""
input_processing_module.py

Orchestrates the complete Input Processing Module.
"""

from input_processing.file_detector import detect_input_source
from input_processing.pdf_extractor import extract_pdf_data
from input_processing.image_ocr import extract_image_data
from input_processing.website_extractor import extract_website_data
from input_processing.data_standardizer import standardize_data
from input_processing.input_validator import validate_standardized_data

from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_INPUT_PROCESSING,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_HIGH,
    SOURCE_MANUAL,
    SOURCE_PDF,
    SOURCE_IMAGE,
    SOURCE_WEBSITE,
    SOURCE_TEXT
)


def process_input(user_input):
    """
    Executes the complete Input Processing Module.

    Parameters:
        user_input

    Returns:
        dict
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        # ---------------------------------
        # Step 1 : Detect Input Source
        # ---------------------------------

        detector_result = detect_input_source(
            user_input
        )

        if detector_result["status"] != STATUS_SUCCESS:
            return detector_result

        source_type = detector_result["data"][
            "source_type"
        ]

        # ---------------------------------
        # Step 2 : Extract Data
        # ---------------------------------

        if source_type == SOURCE_MANUAL:

            extracted_result = {
                "status": STATUS_SUCCESS,
                "data": user_input
            }

        elif source_type == SOURCE_PDF:

            extracted_result = extract_pdf_data(
                user_input
            )

        elif source_type == SOURCE_IMAGE:

            extracted_result = extract_image_data(
                user_input
            )

        elif source_type == SOURCE_WEBSITE:

            extracted_result = extract_website_data(
                user_input
            )

        elif source_type == SOURCE_TEXT:

            extracted_result = {
                "status": STATUS_SUCCESS,
                "data": {
                    "raw_text": user_input
                }
            }

        else:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Unsupported input source."
            )

            return result

        # ---------------------------------
        # Check extraction result
        # ---------------------------------

        if extracted_result["status"] != STATUS_SUCCESS:
            return extracted_result

        # ---------------------------------
        # Step 3 : Standardize Data
        # ---------------------------------

        standardized_result = standardize_data(
            extracted_result,
            source_type
        )

        if standardized_result["status"] != STATUS_SUCCESS:
            return standardized_result

        # ---------------------------------
        # Step 4 : Validate
        # ---------------------------------

        validation_result = validate_standardized_data(
            standardized_result["data"]
        )

        if validation_result["status"] != STATUS_SUCCESS:
            return validation_result

        # ---------------------------------
        # Step 5 : Return Successful Result
        # ---------------------------------

        result["status"] = STATUS_SUCCESS
        result["risk"] = standardized_result.get(
            "risk",
            None
        )
        result["data"] = standardized_result["data"]

        return result

    except Exception as error:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(error)
        )

        return result