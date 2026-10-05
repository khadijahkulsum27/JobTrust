"""
pdf_extractor.py

Extracts useful job information from PDF files.
"""

import re
import pdfplumber
import validators

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    ENGINE_INPUT_PROCESSING
)


def extract_pdf_data(pdf_path):
    """
    Extracts job-related information from a PDF.

    Parameters:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict: Standard engine response.
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        raw_text = ""

        # ------------------------------------
        # Read PDF
        # ------------------------------------

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    raw_text += page_text + "\n"

        # ------------------------------------
        # Clean Text
        # ------------------------------------

        raw_text = raw_text.strip()

        # ------------------------------------
        # Email Extraction
        # ------------------------------------

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            raw_text
        )

        email = (
            email_match.group()
            if email_match
            else ""
        )

        # ------------------------------------
        # Website Extraction
        # ------------------------------------

        website = ""

        website_matches = re.findall(
            r"https?://[^\s]+|www\.[^\s]+",
            raw_text
        )

        for url in website_matches:

            if validators.url(url):

                website = url

                break

        # ------------------------------------
        # Salary Extraction
        # ------------------------------------

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

        # ------------------------------------
        # Phone Number Extraction
        # ------------------------------------

        phone_match = re.search(
            r"\b\d{10}\b",
            raw_text
        )

        contact_number = (
            phone_match.group()
            if phone_match
            else ""
        )

        # ------------------------------------
        # Structured Output
        # ------------------------------------

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
            "PDF processed successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED

        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result