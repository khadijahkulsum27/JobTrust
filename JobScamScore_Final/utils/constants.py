"""
constants.py

Project-wide constants for the AI Job Trust Platform.
"""

# GLOBAL CONSTANTS
# =====================================================

# -----------------------------
# Engine Status
# -----------------------------

STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_WARNING = "WARNING"


# -----------------------------
# Risk Levels
# -----------------------------

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_UNKNOWN = "UNKNOWN"


# -----------------------------
# HTTP Status Codes
# -----------------------------

HTTP_OK = 200
HTTP_MOVED_PERMANENTLY = 301
HTTP_FOUND = 302
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500


# -----------------------------
# Request Configuration
# -----------------------------

HTTP_TIMEOUT = 10

USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


# -----------------------------
# Network Ports
# -----------------------------

HTTPS_PORT = 443


# -----------------------------
# Global Trust Thresholds
# -----------------------------

TRUST_HIGH = 80
TRUST_MEDIUM = 50
TRUST_LOW = 0


# =====================================================
# GLOBAL INPUT SOURCES
# =====================================================

SOURCE_MANUAL = "manual"
SOURCE_PDF = "pdf"
SOURCE_IMAGE = "image"
SOURCE_WEBSITE = "website"
SOURCE_TEXT = "text"
SOURCE_DOCX = "docx"
SOURCE_API = "api"


# =====================================================
# GLOBAL FILE EXTENSIONS
# =====================================================

PDF_EXTENSION = ".pdf"
DOCX_EXTENSION = ".docx"

JPG_EXTENSION = ".jpg"
JPEG_EXTENSION = ".jpeg"
PNG_EXTENSION = ".png"


# =====================================================
# ENGINE 1 : DIGITAL IDENTITY VERIFICATION ENGINE
# =====================================================

# -----------------------------
# Engine Names
# -----------------------------

ENGINE_DIGITAL_IDENTITY = "Digital Identity Engine"

ENGINE_INPUT_PROCESSING = "Input Processing"
ENGINE_INPUT_VALIDATION = "Input Validation"
ENGINE_WEBSITE_VERIFICATION = "Website Verification"
ENGINE_SSL_VERIFICATION = "SSL Verification"
ENGINE_EMAIL_VERIFICATION = "Email Verification"
ENGINE_WHOIS_VERIFICATION = "WHOIS Verification"
ENGINE_DOMAIN_MATCHING = "Domain Matching"
ENGINE_MCA_VERIFICATION = "MCA Verification"
ENGINE_IDENTITY_SCORING = "Identity Scoring"
ENGINE_EXPLANATION_GENERATOR = "Explanation Generator"


# -----------------------------
# Public Email Providers
# -----------------------------

PUBLIC_EMAIL_PROVIDERS = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "live.com",
    "icloud.com",
    "proton.me",
    "protonmail.com",
    "aol.com"
]


# -----------------------------
# MCA Status
# -----------------------------

MCA_ACTIVE = "Active"
MCA_INACTIVE = "Inactive"
MCA_NOT_FOUND = "Not Found"
MCA_UNKNOWN = "Unknown"

MCA_PENDING = "PENDING"

MCA_VERIFIED = "VERIFIED"
MCA_UNVERIFIED = "UNVERIFIED"
MCA_SKIPPED = "SKIPPED"


# -----------------------------
# Engine 1 Scoring Weights
# -----------------------------

WEBSITE_SCORE = 17
SSL_SCORE = 17
EMAIL_SCORE = 17
WHOIS_SCORE = 17
DOMAIN_MATCH_SCORE = 16
MCA_SCORE = 16


# =====================================================
# ENGINE 2 : AI JOB CONTENT ANALYSIS ENGINE
# =====================================================

# -----------------------------
# Engine Names
# -----------------------------

ENGINE_JOB_CONTENT = "Job Content Analysis Engine"

ENGINE_JOB_VALIDATOR = "Job Validator"
ENGINE_KEYWORD_DETECTOR = "Keyword Detector"
ENGINE_SALARY_ANALYZER = "Salary Analyzer"
ENGINE_GRAMMAR_CHECKER = "Grammar Checker"
ENGINE_URGENCY_DETECTOR = "Urgency Detector"
ENGINE_CONTACT_ANALYZER = "Contact Analyzer"
ENGINE_CONTENT_SCORER = "Content Scorer"
ENGINE_CONTENT_EXPLANATION = "Content Explanation"


# -----------------------------
# AI Content Classification
# -----------------------------

CONTENT_LEGITIMATE = "LEGITIMATE"
CONTENT_SUSPICIOUS = "SUSPICIOUS"
CONTENT_UNKNOWN = "UNKNOWN"


# -----------------------------
# Suspicious Job Keywords
# -----------------------------

SUSPICIOUS_KEYWORDS = [
    "earn money fast",
    "work from home",
    "no interview",
    "no experience",
    "immediate joining",
    "limited vacancies",
    "registration fee",
    "processing fee",
    "whatsapp",
    "telegram",
    "urgent hiring",
    "easy money",
    "guaranteed job",
    "100% placement",
    "click here",
    "apply now"
]


# -----------------------------
# Urgency Phrases
# -----------------------------

URGENCY_PHRASES = [
    "apply now",
    "hurry",
    "urgent hiring",
    "last chance",
    "only today",
    "join immediately",
    "limited vacancies",
    "instant joining"
]


# -----------------------------
# Salary Threshold
# -----------------------------

MAX_REASONABLE_MONTHLY_SALARY = 500000


# -----------------------------
# Engine 2 Scoring Weights
# -----------------------------

KEYWORD_SCORE = 20
SALARY_SCORE = 20
GRAMMAR_SCORE = 20
URGENCY_SCORE = 20
CONTACT_SCORE = 20


# -----------------------------
# Engine 2 Trust Thresholds
# -----------------------------

CONTENT_TRUST_HIGH = 80
CONTENT_TRUST_MEDIUM = 50
CONTENT_TRUST_LOW = 0


# =====================================================
# ENGINE 3 : JOB POSTING INTELLIGENCE ENGINE
# =====================================================

# -----------------------------
# Engine Names
# -----------------------------

ENGINE_JOB_INTELLIGENCE = "Job Posting Intelligence Engine"

ENGINE_PATTERN_DETECTOR = "Pattern Detector"
ENGINE_SCAM_BEHAVIOR_DETECTOR = "Scam Behavior Detector"
ENGINE_JOB_CONSISTENCY_ANALYZER = "Job Consistency Analyzer"
ENGINE_SALARY_CONSISTENCY_ANALYZER = "Role Salary Consistency Analyzer"
ENGINE_AI_CONTENT_ANALYZER = "AI Content Analyzer"
ENGINE_ANOMALY_DETECTOR = "Anomaly Detector"
ENGINE_INTELLIGENCE_SCORER = "Intelligence Scorer"
ENGINE_INTELLIGENCE_EXPLANATION = "Intelligence Explanation"


# -----------------------------
# Engine 3 Scoring Weights
# -----------------------------

PATTERN_SCORE = 15
SCAM_BEHAVIOR_SCORE = 15
JOB_CONSISTENCY_SCORE = 15
SALARY_CONSISTENCY_SCORE = 15
AI_CONTENT_SCORE = 15
ANOMALY_SCORE = 15
INTELLIGENCE_CLASSIFICATION_SCORE = 10


# -----------------------------
# Engine 3 Trust Thresholds
# -----------------------------

INTELLIGENCE_TRUST_HIGH = 80
INTELLIGENCE_TRUST_MEDIUM = 50
INTELLIGENCE_TRUST_LOW = 0


# =====================================================
# ENGINE 4 : CYBER THREAT INTELLIGENCE ENGINE
# =====================================================

# -----------------------------
# Engine Name
# -----------------------------

ENGINE_CYBER_THREAT = "Cyber Threat Intelligence Engine"


# -----------------------------
# Engine 4 Components
# -----------------------------

ENGINE_URL_ANALYZER = "URL Analyzer"
ENGINE_HTTPS_CHECKER = "HTTPS Checker"
ENGINE_RDAP_CHECKER = "RDAP Checker"
ENGINE_PHISHING_DETECTOR = "Phishing Detector"
ENGINE_THREAT_INTELLIGENCE = "Threat Intelligence"
ENGINE_CYBER_RISK_SCORER = "Cyber Risk Scorer"
ENGINE_CYBER_EXPLANATION = "Cyber Explanation"


# -----------------------------
# Cyber Risk Indicators
# -----------------------------

CYBER_INDICATOR_SUSPICIOUS_URL = "SUSPICIOUS_URL"
CYBER_INDICATOR_IP_ADDRESS = "IP_ADDRESS_URL"
CYBER_INDICATOR_LONG_URL = "LONG_URL"
CYBER_INDICATOR_SUSPICIOUS_SUBDOMAIN = "SUSPICIOUS_SUBDOMAIN"
CYBER_INDICATOR_SUSPICIOUS_ENCODING = "SUSPICIOUS_ENCODING"
CYBER_INDICATOR_HTTP_ONLY = "HTTP_ONLY"
CYBER_INDICATOR_INVALID_CERTIFICATE = "INVALID_CERTIFICATE"
CYBER_INDICATOR_RECENT_DOMAIN = "RECENT_DOMAIN"
CYBER_INDICATOR_RISKY_DOMAIN = "RISKY_DOMAIN"
CYBER_INDICATOR_THREAT_DETECTED = "THREAT_DETECTED"


# -----------------------------
# Cyber Positive Indicators
# -----------------------------

CYBER_POSITIVE_HTTPS = "VALID_HTTPS"
CYBER_POSITIVE_VALID_DOMAIN = "VALID_DOMAIN"
CYBER_POSITIVE_CLEAN_THREAT_CHECK = "NO_THREAT_DETECTED"
CYBER_POSITIVE_ESTABLISHED_DOMAIN = "ESTABLISHED_DOMAIN"


# -----------------------------
# Engine 4 Risk Thresholds
# -----------------------------

CYBER_RISK_LOW = 29
CYBER_RISK_MEDIUM = 59
CYBER_RISK_HIGH = 60


# -----------------------------
# Engine 4 Scoring Weights
# -----------------------------

CYBER_URL_SCORE = 20
CYBER_HTTPS_SCORE = 20
CYBER_RDAP_SCORE = 20
CYBER_PHISHING_SCORE = 20
CYBER_THREAT_INTELLIGENCE_SCORE = 20


# -----------------------------
# Domain Age Thresholds
# -----------------------------

RECENT_DOMAIN_DAYS = 180
ESTABLISHED_DOMAIN_DAYS = 730


# -----------------------------
# Cyber URL Thresholds
# -----------------------------

MAX_URL_LENGTH = 200
MAX_SUBDOMAIN_COUNT = 3


# -----------------------------
# VirusTotal Threat Intelligence
# -----------------------------

VIRUSTOTAL_API_URL = "https://www.virustotal.com/api/v3"

VIRUSTOTAL_URL_ENDPOINT = "/urls"

VIRUSTOTAL_TIMEOUT = 15


# -----------------------------
# Engine 4 Check Status
# -----------------------------

CHECK_AVAILABLE = "AVAILABLE"
CHECK_UNAVAILABLE = "UNAVAILABLE"
CHECK_SKIPPED = "SKIPPED"
CHECK_ERROR = "ERROR"


# =====================================================
# ENGINE 5 : AI TRUST DECISION ENGINE
# =====================================================

ENGINE_TRUST_DECISION = "AI Trust Decision Engine"

TRUST_DECISION_EVIDENCE = "Evidence Collector"
TRUST_DECISION_RULE_ENGINE = "Trust Rule Engine"
TRUST_DECISION_CONFLICT_RESOLVER = "Conflict Resolver"
TRUST_DECISION_SCORER = "Trust Decision Scorer"
TRUST_DECISION_EXPLANATION = "Trust Decision Explanation"

TRUST_DECISION_TRUSTED = "TRUSTED"
TRUST_DECISION_REVIEW = "REVIEW"
TRUST_DECISION_HIGH_RISK = "HIGH_RISK"

TRUST_DECISION_ENGINE_COUNT = 4

TRUST_DECISION_MIN_SCORE = 0
TRUST_DECISION_MAX_SCORE = 100

TRUST_DECISION_HIGH_CONFIDENCE = 75
TRUST_DECISION_MEDIUM_CONFIDENCE = 50

TRUST_DECISION_AVAILABLE = "AVAILABLE"
TRUST_DECISION_UNAVAILABLE = "UNAVAILABLE"
TRUST_DECISION_UNKNOWN = "UNKNOWN"


# =====================================================
# ENGINE 6 : TRUST SCORE + EXPLAINABLE AI REPORT ENGINE
# =====================================================

ENGINE_TRUST_REPORT = "Trust Score + Explainable AI Report Engine"

ENGINE_TRUST_SCORE_CALCULATOR = "Trust Score Calculator"
ENGINE_RISK_CLASSIFIER = "Risk Classifier"
ENGINE_EXPLANATION_GENERATOR = "Explanation Generator"
ENGINE_REPORT_BUILDER = "Report Builder"

REPORT_COMPLETE = "COMPLETE"
REPORT_PARTIAL = "PARTIAL"
REPORT_UNAVAILABLE = "UNAVAILABLE"

REPORT_SCORE_MIN = 0
REPORT_SCORE_MAX = 100

REPORT_TRUSTED_THRESHOLD = 80
REPORT_REVIEW_THRESHOLD = 50

REPORT_RISK_LOW = "LOW"
REPORT_RISK_MEDIUM = "MEDIUM"
REPORT_RISK_HIGH = "HIGH"
REPORT_RISK_UNKNOWN = "UNKNOWN"


# -----------------------------
# Engine 3 Salary Classification
# -----------------------------

SALARY_NORMAL = "NORMAL"
SALARY_UNUSUAL = "UNUSUAL"
SALARY_HIGHLY_UNUSUAL = "HIGHLY_UNUSUAL"
SALARY_UNKNOWN = "UNKNOWN"