import sys
import os

# Project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Engine folders
ENGINE_1_PATH = os.path.join(PROJECT_ROOT, "Engine 1")
ENGINE_2_PATH = os.path.join(PROJECT_ROOT, "Engine 2")
ENGINE_3_PATH = os.path.join(PROJECT_ROOT, "Engine 3")
ENGINE_4_PATH = os.path.join(PROJECT_ROOT, "Engine 4 ")
ENGINE_5_PATH = os.path.join(PROJECT_ROOT, "Engine 5")
ENGINE_6_PATH = os.path.join(PROJECT_ROOT, "Engine 6")

# Engine 1
from pathlib import Path
import importlib.util


def load_module(file_path, module_name):
    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

sys.path.insert(0, ENGINE_1_PATH)
sys.modules.pop("explanation_generator", None)
                
# Load Engine 1
engine1 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 1",
        "digital_identity_engine.py"
    ),
    "engine1"
)

sys.path.insert(0, ENGINE_2_PATH)

# Load Engine 2
engine2 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 2",
        "job_content_engine.py"
    ),
    "engine2"
)

sys.path.insert(0, ENGINE_3_PATH)

# Load Engine 3
engine3 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 3",
        "job_intelligence_engine.py"
    ),
    "engine3"
)

# Load Engine 4
engine4 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 4 ",
        "cyber_threat_engine.py"
    ),
    "engine4"
)

sys.path.insert(0, ENGINE_5_PATH)

# Load Engine 5
engine5 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 5",
        "trust_ decision_engine.py"
    ),
    "engine5"
)

sys.modules.pop("explanation_generator", None)
sys.path.insert(0, ENGINE_6_PATH)

# Load Engine 6
engine6 = load_module(
    os.path.join(
        PROJECT_ROOT,
        "Engine 6",
        "trust_report_engine.py"
    ),
    "engine6"
)


if __name__ == "__main__":

    test_job = {
        "company_name": "Microsoft",
        "website": "https://www.microsoft.com",
        "email": "careers@microsoft.com",
        "job_title": "Software Developer",
        "job_description": """
        We are looking for a Software Developer to join our team.
        The candidate should have experience with Python and web development.
        Salary: ₹8,00,000 per year.
        Please apply through our official company website.
        """,
        "salary": 800000,
        "experience_level": "fresher"
    }

    print("\n========== ENGINE 1 ==========")
    engine1_result = engine1.digital_identity_engine(
        test_job
    )
    print(engine1_result)

    print("\n========== ENGINE 2 ==========")
    engine2_result = engine2.analyze_job_content(
        test_job
    )
    print(engine2_result)

    print("\n========== ENGINE 3 ==========")
    engine3_result = engine3.analyze_job_intelligence(
        test_job
    )
    print(engine3_result)

    print("\n========== ENGINE 4 ==========")
    engine4_result = engine4.run_cyber_threat_engine(
        test_job["website"]
    )
    print(engine4_result)

    print("\n========== ENGINE 5 ==========")
    engine5_result = engine5.run_trust_decision_engine(
        engine1_result=engine1_result,
        engine2_result=engine2_result,
        engine3_result=engine3_result,
        engine4_result=engine4_result
    )
    print(engine5_result)

    print("\n========== ENGINE 6 ==========")
    engine6_result = engine6.run_trust_report_engine(
        engine5_result=engine5_result
    )
    print(engine6_result)
    
    # =========================================================
    # SAVE TO DATABASE
    # =========================================================
    import uuid
    from datetime import datetime
    import database

    database.create_tables()

    processing_id = str(uuid.uuid4())

    submission_data = {
        "processing_id": processing_id,
        "company_name": test_job.get("company_name", ""),
        "website": test_job.get("website", ""),
        "email": test_job.get("email", ""),
        "job_title": test_job.get("job_title", ""),
        "job_description": test_job.get("job_description", ""),
        "salary": test_job.get("salary", ""),
        "location": test_job.get("location", ""),
        "experience": test_job.get("experience_level", ""),
        "employment_type": test_job.get("employment_type", ""),
        "skills": test_job.get("skills", []),
        "contact_number": test_job.get("contact_number", ""),
        "application_deadline": test_job.get("application_deadline", ""),
        "source_type": "manual",
        "raw_text": "",
        "metadata": {},
        "processed_timestamp": datetime.now().isoformat()
    }

    database.save_submission(submission_data)

    engine6_report = engine6_result.get("data", {})
    database.save_report(processing_id, engine6_report)

    print("\n========== SAVED TO DATABASE ==========")
    print("processing_id:", processing_id)