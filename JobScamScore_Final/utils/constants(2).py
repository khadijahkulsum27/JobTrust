"""
constants.py

Project-wide constants for the AI Job Trust Platform.
"""

# =====================================================
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