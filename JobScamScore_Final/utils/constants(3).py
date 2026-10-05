"""
constants.py

Project-wide constants for the AI Job Trust Platform.
"""

# =====================================================
# ENGINE STATUS
# =====================================================

STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_WARNING = "WARNING"


# =====================================================
# RISK LEVELS
# =====================================================

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_UNKNOWN = "UNKNOWN"


# =====================================================
# ENGINE NAMES
# =====================================================

ENGINE_INPUT_VALIDATION = "Input Validation"
ENGINE_WEBSITE_VERIFICATION = "Website Verification"
ENGINE_SSL_VERIFICATION = "SSL Verification"
ENGINE_EMAIL_VERIFICATION = "Email Verification"
ENGINE_WHOIS_VERIFICATION = "WHOIS Verification"
ENGINE_DOMAIN_MATCHING = "Domain Matching"
ENGINE_MCA_VERIFICATION = "MCA Verification"
ENGINE_IDENTITY_SCORING = "Identity Scoring"
ENGINE_EXPLANATION_GENERATOR = "Explanation Generator"
ENGINE_DIGITAL_IDENTITY = "Digital Identity Engine"
ENGINE_AI_CONTENT = "AI Content Analysis Engine"


# =====================================================
# HTTP STATUS CODES
# =====================================================

HTTP_OK = 200
HTTP_MOVED_PERMANENTLY = 301
HTTP_FOUND = 302
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500


# =====================================================
# REQUEST CONFIGURATION
# =====================================================

HTTP_TIMEOUT = 10

USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


# =====================================================
# NETWORK PORTS
# =====================================================

HTTPS_PORT = 443


# =====================================================
# PUBLIC EMAIL PROVIDERS
# =====================================================

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


# =====================================================
# MCA STATUS
# =====================================================

MCA_ACTIVE = "Active"
MCA_INACTIVE = "Inactive"
MCA_NOT_FOUND = "Not Found"
MCA_UNKNOWN = "Unknown"

MCA_PENDING = "PENDING"

MCA_VERIFIED = "VERIFIED"
MCA_UNVERIFIED = "UNVERIFIED"
MCA_SKIPPED = "SKIPPED"


# =====================================================
# AI CONTENT CLASSIFICATION
# =====================================================

CONTENT_LEGITIMATE = "LEGITIMATE"
CONTENT_SUSPICIOUS = "SUSPICIOUS"
CONTENT_UNKNOWN = "UNKNOWN"


# =====================================================
# SUSPICIOUS JOB KEYWORDS
# =====================================================

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


# =====================================================
# SALARY THRESHOLDS
# =====================================================

MAX_REASONABLE_MONTHLY_SALARY = 500000


# =====================================================
# INPUT SOURCE TYPES
# =====================================================

SOURCE_MANUAL = "manual"
SOURCE_PDF = "pdf"
SOURCE_IMAGE = "image"
SOURCE_WEBSITE = "website"
SOURCE_TEXT = "text"
SOURCE_DOCX = "docx"
SOURCE_API = "api"


# =====================================================
# ENGINE 1 SCORING WEIGHTS
# =====================================================

WEBSITE_SCORE = 17
SSL_SCORE = 17
EMAIL_SCORE = 17
WHOIS_SCORE = 17
DOMAIN_MATCH_SCORE = 16
MCA_SCORE = 16


# =====================================================
# ENGINE 2 SCORING WEIGHTS
# =====================================================

TEXT_QUALITY_SCORE = 25
FEATURE_SCORE = 25
PATTERN_SCORE = 25
CLASSIFICATION_SCORE = 25


# =====================================================
# TRUST SCORE THRESHOLDS
# =====================================================

TRUST_HIGH = 80
TRUST_MEDIUM = 50
TRUST_LOW = 0