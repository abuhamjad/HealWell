"""Application constants."""

# API Information
API_TITLE = "HealWell API"
API_VERSION = "0.1.0"
API_PREFIX = "/api/v1"

# Risk Levels
RISK_LOW = "low"
RISK_MODERATE = "moderate"
RISK_HIGH = "high"

VALID_RISK_LEVELS = [RISK_LOW, RISK_MODERATE, RISK_HIGH]

# Response Messages
SUCCESS_ANALYSIS_CREATED = "Health analysis created successfully"
SUCCESS_HISTORY_RETRIEVED = "History retrieved successfully"
SUCCESS_HISTORY_SAVED = "Medical history saved successfully"
SUCCESS_DOCTORS_FOUND = "Nearby doctors found successfully"
SUCCESS_GENERAL = "Operation completed successfully"

ERROR_INVALID_REQUEST = "Invalid request data"
ERROR_MISSING_PARAMETER = "Missing required parameter"
ERROR_INTERNAL_ERROR = "An internal error occurred"

# Default Values
DEFAULT_HISTORY_LIMIT = 20
DEFAULT_DOCTOR_RADIUS = 5.0
MAX_DOCTOR_DISTANCE_KM = 50.0

# Specialty Types
SPECIALTIES = [
    "General Practitioner",
    "General Physician",
    "Cardiologist",
    "Neurologist",
    "Internal Medicine",
    "Emergency Medicine",
]
