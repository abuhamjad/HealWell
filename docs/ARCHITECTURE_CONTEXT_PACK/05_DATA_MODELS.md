# HealWell Data Models

## Core Input/Output Models

### AnalysisInput
**Location**: `app/ai/models/analysis.py`
**Purpose**: User request data for health analysis

```python
class AnalysisInput(BaseModel):
    symptoms: str
    user_id: Optional[str] = None
    medical_history: Optional[str] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
```

**Used By**:
- AnalysisService (receives from route)
- AnalysisWorkflow (initializes state)
- OpenAIProvider (generates prompt)
- Agents (read from state)

**Example**:
```json
{
  "symptoms": "I have a persistent cough and fever of 38.5°C for 3 days",
  "user_id": "user_123",
  "medical_history": "No chronic conditions",
  "medications": ["vitamin D"],
  "allergies": ["penicillin"]
}
```

---

### AnalysisResult
**Location**: `app/ai/models/analysis.py`
**Purpose**: Complete analysis output from workflow

```python
class AnalysisResult(BaseModel):
    analysis_id: str
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    emergency_alert: bool = False
    emergency_message: Optional[str] = None
```

**Populated By**: AnalysisWorkflow (extracted from final state)

**Used By**:
- AnalysisService (returns to API)
- Route handler (transforms to ApiResponse)

**Example**:
```json
{
  "analysis_id": "588b1d98-3fc6-463d-99bb-235649ded7bb",
  "risk_assessment": {...},
  "specialist_recommendation": {...},
  "health_report": {...},
  "emergency_alert": false
}
```

---

## Agent Output Models

### SymptomAnalysis (NEW v0.7.1)
**Location**: `app/ai/models/symptom.py`
**Purpose**: Structured symptom analysis from LLM

```python
class SymptomAnalysis(BaseModel):
    detected_symptoms: List[str]
    confidence: float  # 0-100
    summary: str
    severity_indicators: List[str] = []
    affected_systems: List[str] = []
```

**Produced By**: SymptomAgent (real LLM call)
**Stored In**: `state["symptom_analysis"]`

**Example**:
```json
{
  "detected_symptoms": ["persistent cough", "fever", "chest pain"],
  "confidence": 92.0,
  "summary": "Patient presents with respiratory infection symptoms...",
  "severity_indicators": ["fever 38.5°C", "chest pain"],
  "affected_systems": ["respiratory", "cardiovascular"]
}
```

---

### RiskAssessment
**Location**: `app/ai/models/risk.py`
**Purpose**: Health risk level assessment

```python
class RiskAssessment(BaseModel):
    risk_level: str  # "low", "moderate", "high"
    confidence: float  # 0-100
    reasoning: str
    warning_signs: List[str] = []
```

**Produced By**: RiskAgent (currently mock)
**Stored In**: `state["risk_assessment"]`

**Example**:
```json
{
  "risk_level": "moderate",
  "confidence": 82.0,
  "reasoning": "Based on detected symptoms: fever and cough suggest possible respiratory infection",
  "warning_signs": ["persistent high fever above 38.5°C", "difficulty breathing"]
}
```

---

### SpecialistRecommendation
**Location**: `app/ai/models/specialist.py`
**Purpose**: Specialist recommendation with urgency

```python
class SpecialistRecommendation(BaseModel):
    specialist: str
    reasoning: str
    urgency: str  # "immediate", "24-48 hours", "1-2 weeks", "routine"
```

**Produced By**: SpecialistAgent (currently mock)
**Stored In**: `state["specialist_recommendation"]`

**Example**:
```json
{
  "specialist": "General Physician",
  "reasoning": "Moderate risk level with respiratory symptoms warrants physician consultation",
  "urgency": "24-48 hours"
}
```

---

### HealthReport
**Location**: `app/ai/models/report.py`
**Purpose**: Comprehensive health guidance report

```python
class HealthReport(BaseModel):
    summary: str
    home_care: List[str] = []
    lifestyle: List[str] = []
    monitoring: List[str] = []
    references: List[str] = []
```

**Produced By**: ReportAgent (currently mock)
**Stored In**: `state["health_report"]`

**Example**:
```json
{
  "summary": "Based on symptom analysis and risk assessment, respiratory infection likely",
  "home_care": ["Get plenty of rest", "Stay hydrated", "Use honey for sore throat"],
  "lifestyle": ["Avoid strenuous activities", "Stay in well-ventilated areas"],
  "monitoring": ["Monitor temperature daily", "Track symptom progression"],
  "references": ["WHO guidelines", "CDC resources"]
}
```

---

## Workflow State Model

### HealthAnalysisState (TypedDict)
**Location**: `app/ai/state/health_state.py`
**Purpose**: Shared mutable state passed through LangGraph

```python
class HealthAnalysisState(TypedDict, total=False):
    session_id: str
    user_input: str
    analysis_input: AnalysisInput
    symptom_analysis: dict[str, Any]
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    doctor_recommendations: List[dict[str, Any]]
    health_report: HealthReport
    workflow_status: str
    current_step: str
    errors: List[str]
    metadata: dict[str, Any]
```

**Lifecycle**:
1. Created by AnalysisWorkflow.execute()
2. Passed to symptom_node → SymptomAgent
3. Updated SymptomAgent returns
4. Passed to risk_node → RiskAgent
5. And so on through workflow
6. Final state returned to AnalysisWorkflow

---

## API Request/Response Models

### AnalysisRequest (Schema)
**Location**: `app/schemas/analysis.py`
**Purpose**: HTTP request validation

```python
class AnalysisRequest(BaseModel):
    symptoms: str
    user_id: Optional[str] = None
```

**Validation**:
- `symptoms`: Required, must be string
- `user_id`: Optional, string

---

### ApiResponse (Schema)
**Location**: `app/schemas/response.py`
**Purpose**: Standardized API response wrapper

```python
class ErrorDetail(BaseModel):
    field: str
    message: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[ErrorDetail]] = None
```

**Success Response**:
```json
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "...",
    "risk_level": "moderate",
    "confidence": 82,
    "specialist": "General Physician",
    "emergency": false
  },
  "errors": null
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Invalid request data",
  "data": null,
  "errors": [
    {
      "field": "symptoms",
      "message": "symptoms is required"
    }
  ]
}
```

---

## Model Relationships

### Data Flow Diagram

```
HTTP Request
    ↓
AnalysisRequest (schema validation)
    ├─ symptoms: str
    └─ user_id: Optional[str]
    ↓
AnalysisInput (structured input)
    ├─ symptoms: str
    ├─ user_id: Optional[str]
    ├─ medical_history: Optional[str]
    ├─ medications: Optional[List[str]]
    └─ allergies: Optional[List[str]]
    ↓
HealthAnalysisState (workflow state)
    ├─ analysis_input: AnalysisInput
    ├─ symptom_analysis: dict
    ├─ risk_assessment: RiskAssessment
    ├─ specialist_recommendation: SpecialistRecommendation
    └─ health_report: HealthReport
    ↓
AnalysisResult (output model)
    ├─ analysis_id: str
    ├─ risk_assessment: RiskAssessment
    ├─ specialist_recommendation: SpecialistRecommendation
    └─ health_report: HealthReport
    ↓
ApiResponse (HTTP response)
    └─ data: {...transformed from AnalysisResult...}
    ↓
HTTP Response (JSON)
```

---

## Model Inheritance & Dependencies

```python
# Pydantic BaseModel (all inherit)
├── AnalysisInput
├── AnalysisResult
│   ├── uses RiskAssessment
│   ├── uses SpecialistRecommendation
│   └── uses HealthReport
├── SymptomAnalysis
├── RiskAssessment
├── SpecialistRecommendation
├── HealthReport
├── ApiResponse
└── ErrorDetail

# TypedDict (workflow state)
├── HealthAnalysisState
    ├── contains AnalysisInput
    ├── contains SymptomAnalysis (dict)
    ├── contains RiskAssessment
    ├── contains SpecialistRecommendation
    └── contains HealthReport
```

---

## Validation Rules

### AnalysisInput Validation
- `symptoms`: Required, non-empty string
- `user_id`: Optional, string format
- `medical_history`: Optional, string
- `medications`: Optional, list of strings
- `allergies`: Optional, list of strings

### SymptomAnalysis Validation
- `detected_symptoms`: List of strings, each lowercase
- `confidence`: Float 0-100
- `summary`: Non-empty string
- `severity_indicators`: Optional list of strings
- `affected_systems`: Optional list of strings

### RiskAssessment Validation
- `risk_level`: Must be "low", "moderate", or "high"
- `confidence`: Float 0-100
- `reasoning`: Non-empty string
- `warning_signs`: Optional list of strings

### ApiResponse Validation
- `success`: Boolean (true for success, false for error)
- `message`: Non-empty string
- `data`: Optional (null for errors, dict for success)
- `errors`: Optional (null for success, list for errors)

---

## Type Safety

All models use Pydantic for runtime validation:
```python
# Will raise ValidationError if data is invalid
try:
    analysis_input = AnalysisInput(**request_data)
except ValidationError as e:
    # Handle validation errors
    pass
```

Benefits:
- Type hints for IDE autocomplete
- Runtime validation on data boundaries
- Clear error messages
- JSON schema generation for API docs

---

## Future Models (Planned)

### v0.8+
- `DrugInteraction`: Drug-to-drug interaction checking
- `PatientHistory`: Structured medical history
- `DoctorProfile`: Healthcare provider information
- `AnalysisHistory`: Saved analysis records
- `UserProfile`: Patient user information

---

## Summary

HealWell's data models provide:
1. **Type Safety**: Pydantic validation at boundaries
2. **Clear Structure**: Each model has single responsibility
3. **Extensibility**: Easy to add fields without breaking
4. **Documentation**: Models serve as API documentation
5. **Validation**: Runtime checks prevent bad data propagation

Models flow: Request → Input → State → Result → Response
