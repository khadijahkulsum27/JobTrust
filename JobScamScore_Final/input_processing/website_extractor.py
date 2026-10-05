"""
website_extractor.py

Extracts job-related information from a website.
"""

import re
import requests
import validators

from bs4 import BeautifulSoup

from utils.response_builder import create_engine_response

from utils.constants import (
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_HIGH,
    HTTP_TIMEOUT,
    USER_AGENT,
    ENGINE_INPUT_PROCESSING
)


def extract_website_data(website_url):
    """
    Extracts job information from a website.

    Parameters:
        website_url (str)

    Returns:
        dict
    """

    result = create_engine_response(
        ENGINE_INPUT_PROCESSING
    )

    try:

        # ---------------------------------
        # Validate URL
        # ---------------------------------

        if not validators.url(website_url):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Invalid website URL."
            )

            return result

        # ---------------------------------
        # Download Webpage
        # ---------------------------------

        response = requests.get(
            website_url,
            headers=USER_AGENT,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True
        )
        

        response.raise_for_status()

        # ---------------------------------
        # Parse HTML
        # ---------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove scripts and styles
        for tag in soup(
            [
                "script",
                "style",
                "noscript"
            ]
        ):
            tag.decompose()

        # ---------------------------------
        # Extract Metadata
        # ---------------------------------

        page_title = ""

        if soup.title:
            page_title = soup.title.get_text(
                strip=True
            )

        meta_description = ""

        meta = soup.find(
            "meta",
            attrs={
                "name": "description"
            }
        )

        if meta:
            meta_description = meta.get(
                "content",
                ""
            ).strip()

        # ---------------------------------
        # Extract Visible Text
        # ---------------------------------

        raw_text = soup.get_text(
            separator="\n"
        )

        raw_text = "\n".join(
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        )

        # ---------------------------------
        # Email Extraction
        # ---------------------------------

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            raw_text
        )

        email = (
            email_match.group()
            if email_match
            else ""
        )

        # ---------------------------------
        # Salary Extraction
        # ---------------------------------

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

        # ---------------------------------
        # Phone Number
        # ---------------------------------

        phone_match = re.search(
            r"\b\d{10}\b",
            raw_text
        )

        contact_number = (
            phone_match.group()
            if phone_match
            else ""
        )

        # ---------------------------------
        # Final Response
        # ---------------------------------

        result["status"] = STATUS_SUCCESS

        result["risk"] = RISK_LOW

        result["data"] = {

            "raw_text": raw_text,

            "metadata": {

                "page_title": page_title,

                "meta_description": meta_description
            },

            "company_name": "",

            "website": website_url,

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
            "Website processed successfully."
        )

    except Exception as e:

        result["status"] = STATUS_FAILED

        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result