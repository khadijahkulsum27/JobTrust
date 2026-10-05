"""
image_ocr.py

Extracts job-related information from image files
using OCR.
"""

import re
import validators
import easyocr

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_PROCESSING
)
_reader = None
def get_reader():
    """Loads the OCR model once and reuses it (loading is the slow part)."""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader

def extract_image_data(image_path):
    """
    Extracts job information from an image.

    Parameters:
        image_path (str)

    Returns:
        dict
    """
    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        reader = get_reader()

        text_list = reader.readtext(
            image_path,
            detail=0
        )

        raw_text = "\n".join(text_list)

        # Email

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            raw_text
        )

        email = (
            email_match.group()
            if email_match
            else ""
        )

        # Website

        website = ""

        websites = re.findall(
            r"https?://[^\s]+|www\.[^\s]+",
            raw_text
        )

        for url in websites:

            if validators.url(url):

                website = url

                break

        # Salary

        salary_match = re.search(
            r"(₹\s?[\d,]+(?:\s?LPA)?|Rs\.?\s?[\d,]+)",
            raw_text,
            re.IGNORECASE
        )

        salary = (
            salary_match.group()
            if salary_match
            else ""
        )

        # Phone

        phone_match = re.search(
            r"\b\d{10}\b",
            raw_text
        )

        contact_number = (
            phone_match.group()
            if phone_match
            else ""
        )

        result["status"] = STATUS_SUCCESS

        result["risk"] = RISK_LOW

        result["data"] = {

            "raw_text": raw_text,

            "company_name": "",

            "website": website,

            "email": email,

            "job_title": "",

            "job_description": "",

            "salary": salary,

            "location": "",

            "experience": "",

            "employment_type": "",

            "skills": [],

            "contact_number": contact_number,

            "application_deadline": ""
        }

        result["remarks"].append(
            "Image processed successfully using OCR."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED

        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result