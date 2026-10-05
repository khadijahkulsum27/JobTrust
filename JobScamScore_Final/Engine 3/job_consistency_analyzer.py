from utils.response_builder import create_engine_response

from utils.constants import (
    ENGINE_JOB_CONSISTENCY_ANALYZER,
    STATUS_SUCCESS,
    STATUS_FAILED,
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH
)


def analyze_job_consistency(job_data):
    """
    Analyzes consistency between different parts of a job posting.

    Parameters:
        job_data (dict): Job posting data

    Returns:
        dict: Standard engine response
    """

    result = create_engine_response(
        ENGINE_JOB_CONSISTENCY_ANALYZER
    )

    try:

        # =================================================
        # INPUT VALIDATION
        # =================================================

        if not isinstance(job_data, dict):

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job data must be provided as a dictionary."
            )

            return result

        job_title = str(
            job_data.get(
                "job_title",
                ""
            )
        ).strip()

        job_description = str(
            job_data.get(
                "job_description",
                ""
            )
        ).strip()

        if not job_title:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job title cannot be empty."
            )

            return result

        if not job_description:

            result["status"] = STATUS_FAILED
            result["risk"] = RISK_HIGH

            result["errors"].append(
                "Job description cannot be empty."
            )

            return result

        # =================================================
        # NORMALIZE TEXT
        # =================================================

        title_lower = job_title.lower()
        description_lower = job_description.lower()

        consistency_issues = []
        consistency_checks = []

        # =================================================
        # CHECK 1 - JOB TITLE RELEVANCE
        # =================================================

        title_words = [
            word.strip(".,!?;:()[]{}")
            for word in title_lower.split()
            if len(word.strip(".,!?;:()[]{}")) > 2
        ]

        matching_title_words = [
            word
            for word in title_words
            if word in description_lower
        ]

        if title_words:

            title_match_ratio = (
                len(matching_title_words)
                / len(title_words)
            )

        else:

            title_match_ratio = 0

        if title_match_ratio >= 0.5:

            consistency_checks.append(
                "Job title is reasonably represented in the description."
            )

        else:

            consistency_issues.append(
                "Job title has limited relevance to the job description."
            )

        # =================================================
        # CHECK 2 - EXPERIENCE CONSISTENCY
        # =================================================

        experience_terms = [
            "fresher",
            "entry level",
            "entry-level",
            "junior",
            "mid level",
            "mid-level",
            "senior",
            "experienced",
            "1 year",
            "2 years",
            "3 years",
            "5 years",
            "10 years"
        ]

        detected_experience_terms = [
            term
            for term in experience_terms
            if term in description_lower
        ]

        experience_in_title = any(
            term in title_lower
            for term in [
                "fresher",
                "junior",
                "senior",
                "intern",
                "internship"
            ]
        )

        if detected_experience_terms:

            if experience_in_title:

                consistency_checks.append(
                    "Experience information appears consistent with the job title."
                )

            else:

                consistency_checks.append(
                    "Experience requirements are explicitly stated."
                )

        else:

            consistency_checks.append(
                "No explicit experience requirement was detected."
            )

        # =================================================
        # CHECK 3 - SENIOR ROLE WITH NO EXPERIENCE
        # =================================================

        senior_role = any(
            term in title_lower
            for term in [
                "senior",
                "lead",
                "manager",
                "director"
            ]
        )

        fresher_requirement = any(
            term in description_lower
            for term in [
                "fresher",
                "no experience",
                "no prior experience",
                "freshers welcome"
            ]
        )

        if senior_role and fresher_requirement:

            consistency_issues.append(
                "Senior-level role appears inconsistent with a no-experience requirement."
            )

        # =================================================
        # CHECK 4 - TECHNICAL ROLE WITH UNRELATED CONTENT
        # =================================================

        technical_role = any(
            term in title_lower
            for term in [
                "developer",
                "engineer",
                "programmer",
                "software",
                "data analyst",
                "data scientist",
                "cybersecurity"
            ]
        )

        technical_terms = [
            "python",
            "java",
            "javascript",
            "sql",
            "database",
            "programming",
            "software",
            "coding",
            "api",
            "development",
            "machine learning"
        ]

        technical_terms_found = [
            term
            for term in technical_terms
            if term in description_lower
        ]

        if technical_role:

            if technical_terms_found:

                consistency_checks.append(
                    "Technical job title is supported by relevant technical requirements."
                )

            else:

                consistency_issues.append(
                    "Technical job title has limited technical content in the description."
                )

        # =================================================
        # CHECK 5 - JOB DESCRIPTION LENGTH
        # =================================================

        word_count = len(
            job_description.split()
        )

        if word_count < 20:

            consistency_issues.append(
                "Job description contains very limited information."
            )

        else:

            consistency_checks.append(
                "Job description contains sufficient text for consistency analysis."
            )

        # =================================================
        # DETERMINE RISK
        # =================================================

        issue_count = len(
            consistency_issues
        )

        if issue_count == 0:

            risk = RISK_LOW

            result["remarks"].append(
                "No major consistency issues were detected."
            )

        elif issue_count <= 2:

            risk = RISK_MEDIUM

            result["remarks"].append(
                "Some inconsistencies were detected in the job posting."
            )

        else:

            risk = RISK_HIGH

            result["remarks"].append(
                "Multiple inconsistencies were detected in the job posting."
            )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        result["status"] = STATUS_SUCCESS
        result["risk"] = risk

        result["data"] = {
            "job_title": job_title,
            "word_count": word_count,
            "title_match_ratio": round(
                title_match_ratio,
                2
            ),
            "detected_experience_terms": (
                detected_experience_terms
            ),
            "technical_terms_found": (
                technical_terms_found
            ),
            "consistency_checks": consistency_checks,
            "consistency_issues": consistency_issues,
            "issue_count": issue_count
        }

    except Exception as e:

        result["status"] = STATUS_FAILED
        result["risk"] = RISK_HIGH

        result["errors"].append(
            str(e)
        )

    return result