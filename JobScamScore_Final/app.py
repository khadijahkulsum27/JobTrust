"""
app.py

Flask API layer for the AI Job Trust Platform.

This file does not modify any Engine 1-6 code, database.py,
or integration_test.py. It simply exposes the same engine
pipeline over HTTP so the React frontend can call it.
"""

import sys
import os
import json
import uuid
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

import database

# =========================================================
# LOAD ENGINES (same exact method as integration_test.py)
# =========================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

ENGINE_1_PATH = os.path.join(PROJECT_ROOT, "Engine 1")
ENGINE_2_PATH = os.path.join(PROJECT_ROOT, "Engine 2")
ENGINE_3_PATH = os.path.join(PROJECT_ROOT, "Engine 3")
ENGINE_4_PATH = os.path.join(PROJECT_ROOT, "Engine 4")
ENGINE_5_PATH = os.path.join(PROJECT_ROOT, "Engine 5")
ENGINE_6_PATH = os.path.join(PROJECT_ROOT, "Engine 6")

import importlib.util


def load_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, ENGINE_1_PATH)
sys.modules.pop("explanation_generator", None)

engine1 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 1", "digital_identity_engine.py"),
    "engine1"
)

sys.path.insert(0, ENGINE_2_PATH)
engine2 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 2", "job_content_engine.py"),
    "engine2"
)

sys.path.insert(0, ENGINE_3_PATH)
engine3 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 3", "job_intelligence_engine.py"),
    "engine3"
)

engine4 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 4", "cyber_threat_engine.py"),
    "engine4"
)

sys.path.insert(0, ENGINE_5_PATH)
engine5 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 5", "trust_ decision_engine.py"),
    "engine5"
)

sys.modules.pop("explanation_generator", None)
sys.path.insert(0, ENGINE_6_PATH)
engine6 = load_module(
    os.path.join(PROJECT_ROOT, "Engine 6", "trust_report_engine.py"),
    "engine6"
)


# =========================================================
# FLASK APP SETUP
# =========================================================

app = Flask(__name__)
CORS(app)  # allows the React app (running on a different port) to call this API

database.create_tables()


# =========================================================
# ROUTES
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

def clean_salary(value):
    """Turns salary into a number, or None if blank or not a number."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value if value > 0 else None
    try:
        number = float(str(value).replace(",", "").strip())
    except ValueError:
        return None
    return number if number > 0 else None

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts a job posting from the frontend, runs it through
    Engines 1-6, saves the result, and returns the full report.
    """

    job_data = request.get_json()

    if not job_data:
        return jsonify({"error": "No job data provided."}), 400

    test_job = {
        "company_name": job_data.get("company_name", ""),
        "website": job_data.get("website", ""),
        "email": job_data.get("email", ""),
        "job_title": job_data.get("job_title", ""),
        "job_description": job_data.get("job_description", ""),
        "salary": clean_salary(job_data.get("salary")),
        "experience_level": job_data.get("experience_level", "")
    }

    try:
        engine1_result = engine1.digital_identity_engine(test_job)
        engine2_result = engine2.analyze_job_content(test_job)
        engine3_result = engine3.analyze_job_intelligence(test_job)
        engine4_result = engine4.run_cyber_threat_engine(test_job["website"])

        engine5_result = engine5.run_trust_decision_engine(
            engine1_result=engine1_result,
            engine2_result=engine2_result,
            engine3_result=engine3_result,
            engine4_result=engine4_result
        )

        engine6_result = engine6.run_trust_report_engine(
            engine5_result=engine5_result
        )

    except Exception as e:
        return jsonify({"error": f"Engine processing failed: {str(e)}"}), 500

    processing_id = str(uuid.uuid4())

    submission_data = {
        "processing_id": processing_id,
        "company_name": job_data.get("company_name", ""),
        "website": job_data.get("website", ""),
        "email": job_data.get("email", ""),
        "job_title": job_data.get("job_title", ""),
        "job_description": job_data.get("job_description", ""),
        "salary": job_data.get("salary", ""),
        "location": job_data.get("location", ""),
        "experience": job_data.get("experience_level", ""),
        "employment_type": job_data.get("employment_type", ""),
        "skills": job_data.get("skills", []),
        "contact_number": job_data.get("contact_number", ""),
        "application_deadline": job_data.get("application_deadline", ""),
        "source_type": "manual",
        "raw_text": "",
        "metadata": {},
        "processed_timestamp": datetime.now().isoformat()
    }

    database.save_submission(submission_data)

    engine6_report = engine6_result.get("data", {})
    database.save_report(processing_id, engine6_report)

    return jsonify({
        "processing_id": processing_id,
        "engine1": engine1_result,
        "engine2": engine2_result,
        "engine3": engine3_result,
        "engine4": engine4_result,
        "engine5": engine5_result,
        "engine6": engine6_result
    })


@app.route("/api/reports", methods=["GET"])
def list_reports():
    """
    Returns a summary list of all past reports, newest first,
    for the report-history feature.
    """

    conn = database.get_connection()
    rows = conn.execute("""
        SELECT s.processing_id, s.company_name, s.job_title,
               r.trust_score, r.decision, r.risk, r.created_timestamp
        FROM submissions s
        JOIN reports r ON s.processing_id = r.processing_id
        ORDER BY r.created_timestamp DESC
    """).fetchall()
    conn.close()

    reports = []
    for row in rows:
        reports.append({
            "processing_id": row[0],
            "company_name": row[1],
            "job_title": row[2],
            "trust_score": row[3],
            "decision": row[4],
            "risk": row[5],
            "created_timestamp": row[6]
        })

    return jsonify(reports)


@app.route("/api/reports/<processing_id>", methods=["GET"])
def get_report(processing_id):
    """
    Returns the full detail for one past report, by its
    processing_id.
    """

    conn = database.get_connection()

    submission = conn.execute(
        "SELECT * FROM submissions WHERE processing_id = ?",
        (processing_id,)
    ).fetchone()

    report = conn.execute(
        "SELECT * FROM reports WHERE processing_id = ?",
        (processing_id,)
    ).fetchone()

    findings = conn.execute(
        "SELECT * FROM engine_findings WHERE processing_id = ?",
        (processing_id,)
    ).fetchone()

    conn.close()

    if not submission or not report:
        return jsonify({"error": "Report not found."}), 404

    submission_cols = [
        "processing_id", "company_name", "website", "email",
        "job_title", "job_description", "salary", "location",
        "experience", "employment_type", "skills", "contact_number",
        "application_deadline", "source_type", "raw_text",
        "metadata", "processed_timestamp"
    ]
    report_cols = [
        "processing_id", "report_status", "trust_score", "decision",
        "risk", "confidence", "summary", "recommendation",
        "verified_label", "created_timestamp"
    ]
    findings_cols = [
        "processing_id", "engine_findings", "positive_findings",
        "negative_findings", "uncertain_findings", "conflict_findings"
    ]

    submission_dict = dict(zip(submission_cols, submission))
    report_dict = dict(zip(report_cols, report))

    submission_dict["skills"] = json.loads(submission_dict["skills"] or "[]")
    submission_dict["metadata"] = json.loads(submission_dict["metadata"] or "{}")

    findings_dict = {}
    if findings:
        findings_dict = dict(zip(findings_cols, findings))
        for key in ["engine_findings", "positive_findings", "negative_findings",
                    "uncertain_findings", "conflict_findings"]:
            findings_dict[key] = json.loads(findings_dict[key] or "[]")

    return jsonify({
        "submission": submission_dict,
        "report": report_dict,
        "findings": findings_dict
    })

@app.route("/api/extract", methods=["POST"])
def extract():
    """
    Reads a screenshot, PDF or job link with the Input Processing layer
    and returns the job text. It does NOT run the engines.
    """
    import tempfile

    # Imported here so a problem in input_processing cannot stop the API starting.
    try:
        from input_processing.input_processing_module import process_input
        from utils.constants import STATUS_SUCCESS
    except Exception as e:
        return jsonify({"error": f"Input processing could not be loaded: {e}"}), 500

    temp_path = None
    try:
        if "file" in request.files:
            uploaded = request.files["file"]
            extension = os.path.splitext(uploaded.filename or "")[1].lower()
            if extension not in (".pdf", ".png", ".jpg", ".jpeg"):
                return jsonify({"error": "Only PDF, PNG and JPG files are supported."}), 400
            handle, temp_path = tempfile.mkstemp(suffix=extension)
            os.close(handle)
            uploaded.save(temp_path)
            user_input = temp_path
        else:
            body = request.get_json(silent=True) or {}
            user_input = str(body.get("url", "")).strip()
            if not user_input:
                return jsonify({"error": "Send a file or a url."}), 400

        result = process_input(user_input)
    except Exception as e:
        return jsonify({"error": f"Extraction failed: {e}"}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    if result.get("status") != STATUS_SUCCESS:
        problems = "; ".join(result.get("errors") or []) or "Could not read this input."
        if "raw_text" in problems:
            problems = "No readable text was found. If this is a scanned PDF, upload a screenshot of it instead."
        return jsonify({"error": problems}), 422

    data = result.get("data") or {}
    return jsonify({
        "source_type": data.get("source_type", ""),
        "raw_text": data.get("raw_text", ""),
        "website": data.get("website", ""),
        "email": data.get("email", ""),
        "salary": data.get("salary", ""),
        "contact_number": data.get("contact_number", "")
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
