"""
file_detector.py

Detects the type of user input and determines
the next processing module.
"""

import os
import validators

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_PROCESSING,
    SOURCE_MANUAL,
    SOURCE_PDF,
    SOURCE_IMAGE,
    SOURCE_WEBSITE,
    SOURCE_TEXT,
    PDF_EXTENSION,
    DOCX_EXTENSION,
    JPG_EXTENSION,
    JPEG_EXTENSION,
    PNG_EXTENSION
)


def detect_input_source(user_input):
    """
    Detects the type of user input.

    Parameters:
        user_input:
            Dictionary
            Website URL
            PDF file path
            Image file path
            DOCX file path
            Plain text

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        # -----------------------------
        # Manual Dictionary Input
        # -----------------------------
        if isinstance(user_input, dict):

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_LOW

            result["data"] = {
                "source_type": SOURCE_MANUAL,
                "next_module": "input_validator",
                "processing_required": False
            }

            result["remarks"].append(
                "Manual input detected."
            )

            return result

        # -----------------------------
        # Website URL
        # -----------------------------
        if isinstance(user_input, str):

            input_value = user_input.strip()

            if validators.url(input_value):

                result["status"] = STATUS_SUCCESS
                result["risk"] = RISK_LOW

                result["data"] = {
                    "source_type": SOURCE_WEBSITE,
                    "next_module": "website_extractor",
                    "processing_required": True
                }

                result["remarks"].append(
                    "Website URL detected."
                )

                return result

            # -------------------------
            # File Detection
            # -------------------------

            extension = os.path.splitext(
                input_value
            )[1].lower()

            if extension == PDF_EXTENSION:

                result["status"] = STATUS_SUCCESS
                result["risk"] = RISK_LOW

                result["data"] = {
                    "source_type": SOURCE_PDF,
                    "next_module": "pdf_extractor",
                    "processing_required": True
                }

                result["remarks"].append(
                    "PDF file detected."
                )

                return result

            elif extension == DOCX_EXTENSION:

                result["status"] = STATUS_FAILED
                result["risk"] = RISK_HIGH

                result["errors"].append(
                    "DOCX files are not currently supported. "
                    "Please upload a PDF, an image, or paste the "
                    "job text directly."
                )

                return result

            elif extension in (
                JPG_EXTENSION,
                JPEG_EXTENSION,
                PNG_EXTENSION
            ):

                result["status"] = STATUS_SUCCESS
                result["risk"] = RISK_LOW

                result["data"] = {
                    "source_type": SOURCE_IMAGE,
                    "next_module": "image_ocr",
                    "processing_required": True
                }

                result["remarks"].append(
                    "Image file detected."
                )

                return result

            # -------------------------
            # Plain Text
            # -------------------------

            result["status"] = STATUS_SUCCESS
            result["risk"] = RISK_LOW

            result["data"] = {
                "source_type": SOURCE_TEXT,
                "next_module": "input_validator",
                "processing_required": False
            }

            result["remarks"].append(
                "Plain text input detected."
            )

            return result

        # -----------------------------
        # Unsupported Input Type
        # -----------------------------

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            "Unsupported input type."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result