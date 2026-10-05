"""
database.py

Handles saving and reading Job Trust Platform results
using a simple SQLite database.

This file does not change any Engine 1-6 code.
It only saves the results they already produce.
"""

import sqlite3
import json
import os

# The database file will be created right here,
# in the same folder as this file.
DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "jobscamscore.db"
)


def get_connection():
    """
    Opens a connection to the database file.
    Creates the file automatically if it doesn't exist yet.
    """
    return sqlite3.connect(DB_PATH)


def create_tables():
    """
    Creates the 3 tables if they don't already exist.
    Safe to run every time the program starts -
    it will NOT delete existing data or recreate
    tables that already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: submissions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            processing_id TEXT PRIMARY KEY,
            company_name TEXT,
            website TEXT,
            email TEXT,
            job_title TEXT,
            job_description TEXT,
            salary TEXT,
            location TEXT,
            experience TEXT,
            employment_type TEXT,
            skills TEXT,
            contact_number TEXT,
            application_deadline TEXT,
            source_type TEXT,
            raw_text TEXT,
            metadata TEXT,
            processed_timestamp TEXT
        )
    """)

    # Table 2: reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            processing_id TEXT PRIMARY KEY,
            report_status TEXT,
            trust_score REAL,
            decision TEXT,
            risk TEXT,
            confidence REAL,
            summary TEXT,
            recommendation TEXT,
            verified_label TEXT,
            created_timestamp TEXT,
            FOREIGN KEY (processing_id) REFERENCES submissions (processing_id)
        )
    """)

    # Table 3: engine_findings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engine_findings (
            processing_id TEXT PRIMARY KEY,
            engine_findings TEXT,
            positive_findings TEXT,
            negative_findings TEXT,
            uncertain_findings TEXT,
            conflict_findings TEXT,
            FOREIGN KEY (processing_id) REFERENCES submissions (processing_id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully at:")
    print(DB_PATH)

def save_submission(data):
    """
    Saves one job submission into the 'submissions' table.

    Parameters:
        data (dict) - the standardized job data,
        exactly what data_standardizer.py produces
        (the 'data' part of its result).

    Returns:
        True if saved successfully, False if something went wrong.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO submissions (
                processing_id, company_name, website, email,
                job_title, job_description, salary, location,
                experience, employment_type, skills, contact_number,
                application_deadline, source_type, raw_text,
                metadata, processed_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("processing_id"),
            data.get("company_name"),
            data.get("website"),
            data.get("email"),
            data.get("job_title"),
            data.get("job_description"),
            data.get("salary"),
            data.get("location"),
            data.get("experience"),
            data.get("employment_type"),
            json.dumps(data.get("skills", [])),
            data.get("contact_number"),
            data.get("application_deadline"),
            data.get("source_type"),
            data.get("raw_text"),
            json.dumps(data.get("metadata", {})),
            data.get("processed_timestamp"),
        ))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Error saving submission:", e)
        return False

def save_report(processing_id, report):
    """
    Saves the final Engine 6 report into the 'reports'
    and 'engine_findings' tables.

    Parameters:
        processing_id (str) - the same ID used in save_submission,
        so this report links back to the correct job submission.

        report (dict) - exactly what report_builder.py's
        build_trust_report() returns.

    Returns:
        True if saved successfully, False if something went wrong.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        trust_assessment = report.get("trust_assessment", {})

        from datetime import datetime
        created_timestamp = datetime.now().isoformat()

        # Table 2: reports
        cursor.execute("""
            INSERT OR REPLACE INTO reports (
                processing_id, report_status, trust_score, decision,
                risk, confidence, summary, recommendation,
                verified_label, created_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            processing_id,
            report.get("report_status"),
            trust_assessment.get("trust_score"),
            trust_assessment.get("decision"),
            trust_assessment.get("risk"),
            trust_assessment.get("confidence"),
            report.get("summary"),
            report.get("recommendation"),
            None,  # verified_label - filled in later by a human
            created_timestamp,
        ))

        # Table 3: engine_findings
        cursor.execute("""
            INSERT OR REPLACE INTO engine_findings (
                processing_id, engine_findings, positive_findings,
                negative_findings, uncertain_findings, conflict_findings
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            processing_id,
            json.dumps(report.get("engine_findings", [])),
            json.dumps(report.get("positive_findings", [])),
            json.dumps(report.get("negative_findings", [])),
            json.dumps(report.get("uncertain_findings", [])),
            json.dumps(report.get("conflict_findings", [])),
        ))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Error saving report:", e)
        return False