# HealWell Backend Architecture

## Overview

The HealWell backend is a FastAPI-based REST API that orchestrates AI workflows and manages healthcare data. It follows a service-oriented, layered architecture with clear separation of concerns.

---

## Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app initialization
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # Settings management
│   │   └── constants.py                 # Application constants
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py                    # Central API router
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── analysis.py              # POST /api/v1/analysis
│   │       ├── history.py               # GET/POST /api/v1/history
│   │       └── doctors.py               # GET /api/v1/doctors
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analysis.py                  # AnalysisRequest/Response
│   │   ├── history.py                   # History schemas
│   │   ├── doctor.py                    # Doctor schemas
│   │   └── response.py                  # ApiResponse helpers
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analysis_service.py          # Analysis orchestration
│   │   ├── history_service.py           # History management
│   │   ├── doctor_service.py            # Doctor finder
│   │   └── report_service.py            # Report management
│   ├── models/
│   │   └── __init__.py                  # Database models (future)
│   ├── ai/                              # Intelligence layer
│   │   ├── __init__.py
│   │   ├── providers/                   # LLM providers
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # BaseProvider interface
│   │   │   ├── openai_provider.py       # Groq/OpenAI impl
│   │   │   ├── gemini.py                # Gemini impl (placeholder)
│   │   │   └── factory.py               # Provider factory
│   │   ├── agents/                      # Multi-step agents
│   │   │   ├── __init__.py
│   │   │   ├── base.py                  # BaseAgent interface
│   │   │   ├── symptom_agent.py         # Symptom analysis (REAL v0.7.1)
│   │   │   ├── risk_agent.py            # Risk assessment (mock)
│   │   │   ├── specialist_agent.py      # Specialist recommendation (mock)
│   │   │   └── report_agent.py          # Report generation (mock)
│   │   ├── prompts/                     # LLM prompt templates
│   │   │   ├── __init__.py
│   │   │   ├── symptom_prompt.py        # Symptom analysis prompt
│   │   │   ├── risk_prompt.py           # Risk assessment prompt
│   │   │   ├── specialist_prompt.py     # Specialist recommendation
│   │   │   └── report_prompt.py         # Report generation prompt
│   │   ├── models/                      # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py              # AnalysisInput, AnalysisResult
│   │   │   ├── symptom.py               # SymptomAnalysis (NEW v0.7.1)
│   │   │   ├── risk.py                  # RiskAssessment
│   │   │   ├── specialist.py            # SpecialistRecommendation
│   │   │   └── report.py                # HealthReport
│   │   ├── state/                       # Workflow state
│   │   │   ├── __init__.py
│   │   │   └── health_state.py          # HealthAnalysisState TypedDict
│   │   ├── workflows/                   # Workflow orchestration
│   │   │   ├── __init__.py
│   │   │   └── analysis_workflow.py     # AnalysisWorkflow
│   │   └── graphs/                      # LangGraph definitions
│   │       ├── __init__.py
│   │       ├── health_graph.py          # Graph docs and visualization
│   │       └── langgraph_builder.py     # Graph builder and compiler
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
```

---

## Layer Architecture

### Request Lifecycle

```
HTTP Request
    ↓
FastAPI Application
    ↓
Middleware (CORS)
    ↓
API Router (/api/v1)
    ↓
Route Handler (analysis, history, doctors)
    ↓
Pydantic Validation (Schema)
    ↓
Service Layer
    ├─ AnalysisService
    ├─ HistoryService
    ├─ DoctorService
    └─ ReportService
    ↓
AI Layer (if applicable)
    ├─ AnalysisWorkflow
    ├─ LangGraph Execution
    └─ Agents + Providers
    ↓
Response Schema
    ↓
ApiResponse (success/error)
    ↓
HTTP Response (JSON)
```

---

## Core Components

### 1. FastAPI Application (`main.py`)

```python
# Key initialization
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# CORS Middleware (environment-aware)
# - Development: Accepts localhost and private IPs
# - Production: Strict domain validation

# API Router included at /api/v1
app.include_router(api_router)

# Health endpoints
GET /             # API status
GET /health       # Health check
```

**Responsibilities**:
- Application initialization
- Middleware configuration
- Route registration
- Health monitoring

### 2. Configuration (`core/config.py`)

**Purpose**: Environment-based settings management using Pydantic Settings

**Key Settings**:
```python
# Core
ENVIRONMENT = "development" | "staging" | "production"
DEBUG = True/False
API_TITLE = "HealWell API"
API_VERSION = "0.7.1"

# Deployment
HOST = "0.0.0.0"
PORT = 8000

# CORS
CORS_ORIGINS = "http://localhost:5173,..."
CORS_ALLOW_CREDENTIALS = True

# LLM Provider (v0.7+)
LLM_PROVIDER = "openai"                    # or "gemini"
LLM_BASE_URL = "https://api.groq.com/openai/v1"
LLM_API_KEY = "${GROQ_API_KEY}"
LLM_MODEL = "openai/gpt-oss-120b"
LLM_TIMEOUT = 30

# Database (v0.9+)
DATABASE_URL = "postgresql://..."

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "json" | "text"
```

**Load Order**: `.env` file → environment variables → defaults

### 3. API Router (`api/router.py`)

```python
api_router = APIRouter(prefix="/api/v1")

# Includes sub-routers
api_router.include_router(analysis.router)    # /analysis
api_router.include_router(history.router)     # /history
api_router.include_router(doctors.router)     # /doctors
```

---

## API Endpoints

### Analysis Route (`api/routes/analysis.py`)

```
POST /api/v1/analysis
├── Request: AnalysisRequest (symptoms: str, user_id: Optional[str])
├── Service: AnalysisService.analyze()
├── Workflow: AnalysisWorkflow.execute()
│   ├── LangGraph State: HealthAnalysisState
│   ├── Symptom Agent: Real LLM analysis (v0.7.1)
│   ├── Risk Agent: Mock analysis
│   ├── Specialist Agent: Mock recommendation
│   └── Report Agent: Mock report
└── Response: ApiResponse with analysis_id, risk_level, specialist, emergency
```

**Status**: Operational - SymptomAgent uses real LLM (v0.7.1), others use mock

### History Route (`api/routes/history.py`)

```
GET /api/v1/history
├── Query params: user_id, limit
├── Service: HistoryService.get_user_history()
└── Response: ApiResponse with history list

POST /api/v1/history
├── Request: HistorySaveRequest
├── Service: HistoryService.save_analysis()
└── Response: ApiResponse with saved history
```

**Status**: Placeholder - Returns mock data, pending database integration

### Doctors Route (`api/routes/doctors.py`)

```
GET /api/v1/doctors
├── Query params: latitude, longitude, specialty, radius_km
├── Service: DoctorService.find_nearby()
└── Response: ApiResponse with doctor list
```

**Status**: Placeholder - Returns mock data, pending geolocation integration

---

## Service Layer

### AnalysisService

```python
class AnalysisService:
    async def analyze(
        symptoms: str,
        user_id: Optional[str] = None
    ) -> AnalysisResult:
        """
        1. Create AnalysisInput from request data
        2. Execute AnalysisWorkflow
        3. Return AnalysisResult
        """
        
        input_data = AnalysisInput(
            symptoms=symptoms,
            user_id=user_id,
        )
        
        result = await self.workflow.execute(input_data)
        return result
```

**Responsibilities**:
- Convert request data to AI model input
- Orchestrate workflow execution
- Format results for API response
- Error handling and logging

### HistoryService

```python
class HistoryService:
    async def get_user_history(user_id: str) -> List[dict]:
        """Retrieve user's analysis history"""
        # TODO: Query database
        
    async def save_analysis(analysis_id: str, data: dict) -> bool:
        """Save analysis result"""
        # TODO: Persist to database
```

**Responsibilities**:
- History retrieval
- History persistence
- History filtering

### DoctorService

```python
class DoctorService:
    async def find_nearby(
        latitude: float,
        longitude: float,
        specialty: Optional[str] = None,
        radius_km: float = 5.0
    ) -> List[dict]:
        """Find nearby healthcare providers"""
        # TODO: Query geolocation database
```

**Responsibilities**:
- Location-based doctor search
- Specialty filtering
- Distance calculation

### ReportService

```python
class ReportService:
    async def generate_pdf(analysis_id: str) -> bytes:
        """Generate PDF report"""
        # TODO: Implement PDF generation
        
    async def export_report(analysis_id: str, format: str) -> bytes:
        """Export in various formats"""
        # TODO: Implement export logic
```

**Responsibilities**:
- Report generation
- Format conversion
- File generation

---

## Request/Response Schemas

### AnalysisRequest

```python
class AnalysisRequest(BaseModel):
    symptoms: str          # Required: patient symptom description
    user_id: Optional[str] = None  # Optional: user identifier
```

### AnalysisResponse (part of ApiResponse)

```json
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "588b1d98-3fc6-463d-99bb-235649ded7bb",
    "risk_level": "moderate",
    "confidence": 82.0,
    "specialist": "General Physician",
    "emergency": false
  },
  "errors": null
}
```

### ApiResponse Wrapper

```python
class ApiResponse(BaseModel):
    success: bool                      # Operation success
    message: str                       # Human-readable message
    data: Optional[Any] = None        # Response data
    errors: Optional[List[ErrorDetail]] = None  # Errors if failed
```

---

## AI Layer Integration

### Provider Factory Pattern

```python
def create_provider() -> BaseProvider:
    """
    Selects provider based on LLM_PROVIDER setting
    
    Returns:
        OpenAIProvider (for Groq/OpenAI-compatible)
        GeminiProvider (for Google Gemini)
    """
    provider_name = settings.LLM_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            timeout=settings.LLM_TIMEOUT,
        )
    # ... other providers
```

**Benefits**:
- Runtime provider selection
- No agent changes needed to switch providers
- Configuration-driven
- Testable with mock providers

### Service → Workflow → LangGraph Flow

```python
# AnalysisService.analyze()
input_data = AnalysisInput(symptoms=symptoms, user_id=user_id)
result = await self.workflow.execute(input_data)

# AnalysisWorkflow.execute()
initial_state = {
    "session_id": uuid.uuid4(),
    "user_input": input_data.symptoms,
    "analysis_input": input_data,
    # ... other state fields
}
final_state = await self.compiled_graph.ainvoke(initial_state)

# LangGraph execution
# Symptom Agent (REAL) → Risk Agent (mock) → 
# Specialist Agent (mock) → Report Agent (mock)

# Extract results
return AnalysisResult(
    analysis_id=session_id,
    risk_assessment=final_state["risk_assessment"],
    specialist_recommendation=final_state["specialist_recommendation"],
    health_report=final_state["health_report"],
    emergency_alert=False,
)
```

---

## Data Validation Pipeline

### Incoming Request

```
HTTP POST /api/v1/analysis
    ↓
JSON Payload
    ↓
Pydantic AnalysisRequest
    ├─ Validates: symptoms (required string)
    ├─ Validates: user_id (optional string)
    └─ Rejects: Invalid types, missing required fields
    ↓
AnalysisService.analyze()
```

### AI Models

```
AnalysisInput
    ├─ symptoms: str
    ├─ user_id: Optional[str]
    ├─ medical_history: Optional[str]
    ├─ medications: Optional[List[str]]
    └─ allergies: Optional[List[str]]
    
SymptomAnalysis (Pydantic model)
    ├─ detected_symptoms: List[str]
    ├─ confidence: float (0-100)
    ├─ summary: str
    ├─ severity_indicators: List[str]
    └─ affected_systems: List[str]

RiskAssessment (Pydantic model)
    ├─ risk_level: str (low/moderate/high)
    ├─ confidence: float
    ├─ reasoning: str
    └─ warning_signs: List[str]

SpecialistRecommendation (Pydantic model)
    ├─ specialist: str
    ├─ reasoning: str
    └─ urgency: str

HealthReport (Pydantic model)
    ├─ summary: str
    ├─ home_care: List[str]
    ├─ lifestyle: List[str]
    ├─ monitoring: List[str]
    └─ references: List[str]
```

### Response Validation

```
AnalysisResult
    ├─ analysis_id: str
    ├─ risk_assessment: RiskAssessment
    ├─ specialist_recommendation: SpecialistRecommendation
    ├─ health_report: HealthReport
    └─ emergency_alert: bool
    
    ↓ (transformed for API)
    
ApiResponse
    ├─ success: bool
    ├─ message: str
    ├─ data: {...response data...}
    └─ errors: null/List[ErrorDetail]
```

---

## Error Handling

### Layer-Wise Error Handling

#### API Layer
```python
@router.post("/analysis")
async def create_analysis(request: AnalysisRequest):
    try:
        result = await analysis_service.analyze(
            symptoms=request.symptoms,
            user_id=request.user_id,
        )
        return success_response(data=analysis_data)
    except Exception as e:
        # Log error
        # Return error response
        return error_response(message=str(e))
```

#### Service Layer
```python
class AnalysisService:
    async def analyze(self, symptoms: str) -> AnalysisResult:
        try:
            input_data = AnalysisInput(symptoms=symptoms)
            result = await self.workflow.execute(input_data)
            return result
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise
```

#### Workflow Layer
```python
class AnalysisWorkflow:
    async def execute(self, input_data: AnalysisInput):
        try:
            final_state = await self.compiled_graph.ainvoke(initial_state)
            return AnalysisResult(...)
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            raise
```

#### Agent Layer
```python
class SymptomAgent(BaseAgent):
    async def execute(self, state: dict):
        try:
            provider = create_provider()
            await provider.initialize()
            result = await provider.analyze_symptoms_structured(analysis_input)
            state["symptom_analysis"] = result.model_dump()
        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}")
            state["errors"].append(f"Symptom analysis error: {str(e)}")
        
        return state
```

**Key Principle**: Errors are logged at each layer and propagated up or handled gracefully.

---

## Dependency Injection

### Service Instantiation

```python
# In route handlers
analysis_service = AnalysisService()
history_service = HistoryService()
doctor_service = DoctorService()
report_service = ReportService()

# Services create their own dependencies
class AnalysisService:
    def __init__(self, ai_provider=None):
        self.ai_provider = ai_provider or create_provider()
        self.workflow = AnalysisWorkflow()
```

**Benefits**:
- Easy to mock for testing
- Flexible initialization
- Clear dependency graph

---

## Async/Await Design

### Async Flow

```python
# All I/O operations are async
async def analyze():
    # Async service call
    result = await analysis_service.analyze(symptoms)
    
    # Inside service
    async def analyze():
        # Async workflow
        result = await self.workflow.execute(input_data)
        
        # Inside workflow
        async def execute():
            # Async LangGraph invocation
            final_state = await self.compiled_graph.ainvoke(state)
            
            # Inside agents (called by LangGraph)
            async def execute():  # SymptomAgent
                # Async provider initialization
                await provider.initialize()
                
                # Async LLM call
                result = await provider.analyze_symptoms_structured(input_data)
```

**Benefits**:
- Non-blocking I/O
- Better resource utilization
- Handles concurrent requests
- Natural fit for FastAPI

---

## Configuration Management

### Environment Variables

```bash
# Core
ENVIRONMENT=development
DEBUG=True

# API
API_TITLE=HealWell API
API_VERSION=0.7.1

# Deployment
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5173,...

# LLM (v0.7+)
LLM_PROVIDER=openai
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=<groq-api-key>
LLM_MODEL=openai/gpt-oss-120b
LLM_TIMEOUT=30

# Database (v0.9+)
DATABASE_URL=postgresql://user:password@host/db

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Environment-Specific Behavior

```python
# Development
- Allow localhost origins
- Allow localhost, 127.0.0.1, private IPs
- Debug mode enabled
- Verbose logging

# Staging
- Limited origins
- TLS enforcement
- Moderate logging
- Rate limiting

# Production
- Strict origin validation
- TLS required
- Minimal logging (performance)
- Enhanced rate limiting
- Security headers
```

---

## Performance Considerations

### Response Times

| Operation | Typical Time | Components |
|-----------|--------------|------------|
| Health check | <10ms | Network + FastAPI |
| Analysis (LLM) | 3-5s | Service setup + LangGraph + Provider + LLM |
| History retrieval | 50-200ms | Service + Database (future) |
| Doctor search | 100-500ms | Service + Geolocation DB (future) |

### Scalability

**Stateless Design**:
- Each request is independent
- No server-side sessions
- Can be load-balanced horizontally

**Bottlenecks**:
1. **LLM Provider**: Rate limits, API latency
2. **Database**: Query performance, connection pooling
3. **Memory**: Agent state size (currently small)

**Optimization Opportunities**:
- Response caching for identical inputs
- Batch processing for multiple analyses
- Database query optimization
- LLM request batching

---

## Logging & Monitoring

### Current Logging

```python
import logging
logger = logging.getLogger(__name__)

# In providers
logger.error(f"Symptom analysis failed: {e}")
logger.info(f"Symptom analysis completed: {len(symptoms)} symptoms")

# In agents
logger.error(f"Symptom analysis failed: {e}")
```

### Recommended Enhancements (v0.9+)

```python
# Structured logging
logger.info("analysis_started", extra={
    "session_id": session_id,
    "user_id": user_id,
    "symptom_length": len(symptoms),
})

# Performance monitoring
logger.debug(f"Provider call duration: {end - start}ms")

# Error tracking
logger.error("provider_error", extra={
    "error_type": type(e).__name__,
    "error_message": str(e),
    "provider": "openai",
    "endpoint": "analyze_symptoms",
})
```

---

## Security Checklist

### Current Implementation
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ Environment-based secrets
- ✅ Error handling (no sensitive leaks)
- ⚠️ HTTP in development (acceptable)

### For Production (v0.9+)
- [ ] HTTPS enforcement
- [ ] Authentication (JWT/OAuth)
- [ ] Authorization (RBAC)
- [ ] Rate limiting
- [ ] Request signing
- [ ] SQL injection prevention (ORM)
- [ ] XSS prevention (API only, but important)
- [ ] CSRF tokens
- [ ] Security headers (HSTS, CSP, etc.)
- [ ] Input sanitization for medical data
- [ ] GDPR compliance for patient data
- [ ] Audit logging for medical records
- [ ] Data encryption (at rest and in transit)

---

## Testing Strategy

### Unit Tests
```python
# Test services independently
test_analysis_service.py
test_history_service.py
test_doctor_service.py

# Test providers
test_openai_provider.py
test_gemini_provider.py

# Test agents
test_symptom_agent.py
test_risk_agent.py
```

### Integration Tests
```python
# Test full workflow
test_analysis_workflow.py

# Test API endpoints
test_analysis_endpoint.py
test_history_endpoint.py
test_doctors_endpoint.py
```

### Mock Providers for Testing
```python
class MockProvider(BaseProvider):
    async def analyze_symptoms(self, input_data):
        return predetermined_response  # For consistent testing
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] LLM provider API key validated
- [ ] CORS origins updated for production
- [ ] Logging configured

### Deployment
- [ ] Run migrations
- [ ] Start backend server
- [ ] Health check endpoint responds
- [ ] API documentation available at /docs
- [ ] HTTPS enforcement enabled

### Post-Deployment
- [ ] Monitor error logs
- [ ] Check response times
- [ ] Verify LLM API connectivity
- [ ] Test critical workflows
- [ ] Monitor resource usage

---

## Summary

The HealWell backend is a well-structured, layered FastAPI application that:
- Separates concerns (routes, services, AI, data)
- Uses async/await throughout
- Validates all inputs with Pydantic
- Provides clear error handling
- Integrates AI via a flexible provider pattern
- Is ready for horizontal scaling
- Maintains backward compatibility as it evolves

The architecture supports the current v0.7.1 milestone and is designed to accommodate future features (database, authentication, additional LLM providers) without major refactoring.
