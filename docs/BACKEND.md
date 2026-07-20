# HealWell Backend Documentation

## Status
✅ **Milestone v0.6 Completed** - LangGraph workflow orchestration implemented.

## Implemented Folder Structure
```
backend/
├── app/
│   ├── main.py
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py
│   │   │   ├── risk.py
│   │   │   ├── specialist.py
│   │   │   └── report.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── gemini.py
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── symptom_prompt.py
│   │   │   ├── risk_prompt.py
│   │   │   ├── specialist_prompt.py
│   │   │   └── report_prompt.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── symptom_agent.py
│   │   │   ├── risk_agent.py
│   │   │   ├── specialist_agent.py
│   │   │   └── report_agent.py
│   │   ├── state/
│   │   │   ├── __init__.py
│   │   │   └── health_state.py
│   │   ├── graphs/
│   │   │   ├── __init__.py
│   │   │   ├── health_graph.py
│   │   │   └── langgraph_builder.py
│   │   └── workflows/
│   │       ├── __init__.py
│   │       └── analysis_workflow.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── analysis.py
│   │       ├── history.py
│   │       └── doctors.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── constants.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   ├── history.py
│   │   ├── doctor.py
│   │   └── response.py
│   └── services/
│       ├── __init__.py
│       ├── analysis_service.py
│       ├── history_service.py
│       ├── doctor_service.py
│       └── report_service.py
├── requirements.txt
├── .env.example
└── README.md
```

## Framework & Setup
- **FastAPI**: Modern web framework with automatic API documentation
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation using Python type annotations
- **Python-dotenv**: Environment configuration management

## Architecture

### Core Configuration (`app/core/config.py`)
- Environment-based settings management
- CORS configuration for frontend development
- API metadata (title, version)

### API Structure (`app/api/`)
- **Router** (`router.py`): Centralized API route registration
- **Routes**: Organized by domain (analysis, history, doctors)
  - Analysis routes: POST /api/v1/analysis
  - History routes: GET/POST /api/v1/history
  - Doctor routes: GET /api/v1/doctors

### Schemas (`app/schemas/`)
- **analysis.py**: AnalysisRequest, AnalysisResponse
- **history.py**: HistoryResponse, HistorySaveRequest
- **doctor.py**: Doctor, DoctorsResponse
- All schemas use Pydantic for type validation

### Main Application (`app/main.py`)
- FastAPI application factory
- CORS middleware configured for http://localhost:5173 (frontend development)
- Health check endpoints (GET / and GET /health)
- API versioning at /api/v1

## Current Endpoints

All endpoints currently return placeholder/mock responses:

- `GET /` - API root with version and status
- `GET /health` - Health check endpoint
- `POST /api/v1/analysis` - Create symptom analysis
- `GET /api/v1/history` - Retrieve analysis history
- `POST /api/v1/history` - Save medical history
- `GET /api/v1/doctors` - Find nearby doctors

## AI Foundation (v0.5)

### Provider Layer (`app/ai/providers/`)
- **BaseProvider**: Abstract interface for AI providers
- **GeminiProvider**: Gemini API implementation (placeholder, pending API integration)
- Extensible architecture for multiple AI provider support

### Prompt Templates (`app/ai/prompts/`)
- **symptom_prompt.py**: Symptom analysis prompt generation
- **risk_prompt.py**: Risk assessment prompt generation
- **specialist_prompt.py**: Specialist recommendation prompt generation
- **report_prompt.py**: Health report generation prompt
- All prompts use TODO markers for future implementation

### Agents (`app/ai/agents/`)
- **BaseAgent**: Abstract agent interface
- **SymptomAgent**: Symptom analysis agent
- **RiskAgent**: Risk assessment agent
- **SpecialistAgent**: Specialist recommendation agent
- **ReportAgent**: Health report generation agent
- Agent-based architecture ready for LangGraph integration

### Workflows (`app/ai/workflows/`)
- **AnalysisWorkflow**: Orchestrates the health analysis workflow using LangGraph
  - Initializes HealthAnalysisState with user input
  - Invokes compiled LangGraph via async `ainvoke()`
  - Returns AnalysisResult with complete workflow output

### AI Models (`app/ai/models/`)
- **AnalysisInput**: User input for analysis
- **AnalysisResult**: Complete analysis output
- **RiskAssessment**: Risk level assessment
- **SpecialistRecommendation**: Specialist matching output
- **HealthReport**: Generated health report

### Business Services (`app/services/`)
- **AnalysisService**: Orchestrates AI workflow for symptom analysis
- **HistoryService**: Manages medical history
- **DoctorService**: Healthcare provider finder
- **ReportService**: Health report management
- Service layer decouples API from business logic

## LangGraph Orchestration (v0.6)

### Shared Workflow State (`app/ai/state/`)
- **HealthAnalysisState** (TypedDict): Single source of truth for workflow
  - `session_id`: Unique workflow session identifier
  - `user_input`: Raw symptom description from user
  - `analysis_input`: Parsed AnalysisInput with medical history
  - `symptom_analysis`: Detected symptoms and confidence scores
  - `risk_assessment`: RiskAssessment with risk_level, confidence, reasoning
  - `specialist_recommendation`: SpecialistRecommendation with specialist type and urgency
  - `doctor_recommendations`: List of nearby doctors (future implementation)
  - `health_report`: HealthReport with recommendations
  - `workflow_status`: Current execution status
  - `current_step`: Last executed agent node
  - `errors`: List of workflow errors
  - `metadata`: User metadata (medical history, medications, allergies)

### LangGraph Workflow (`app/ai/graphs/langgraph_builder.py`)
- **build_health_analysis_graph()**: Creates StateGraph with 4 agent nodes
  - Each node receives HealthAnalysisState
  - Each node updates only its own fields
  - Returns updated HealthAnalysisState
- **compile_health_analysis_graph()**: Compiles graph for execution

### Workflow Execution Pipeline
```
API Route (POST /api/v1/analysis)
    ↓
AnalysisService.analyze()
    ↓
AnalysisWorkflow.execute()
    ↓
compiled_graph.ainvoke(initial_state)
    ↓
SymptomAgent (updates symptom_analysis)
    ↓
RiskAgent (updates risk_assessment)
    ↓
SpecialistAgent (updates specialist_recommendation)
    ↓
ReportAgent (updates health_report)
    ↓
Final HealthAnalysisState
    ↓
AnalysisResult (analysis_id, risk_assessment, specialist_recommendation, health_report)
```

### Agent Execution Flow (v0.6)
Each agent:
1. Receives HealthAnalysisState as input
2. Reads required fields from state
3. Performs analysis or processing
4. Updates only its own fields
5. Returns complete updated state
6. No agent overwrites unrelated data

**Current Implementation**: All agents return realistic mock healthcare data
- Mock symptom detection with confidence scores
- Mock risk levels (low, moderate, high)
- Mock specialist recommendations (General Physician, Cardiologist, Neurologist)
- Mock health report with recommendations

### Service Layer Integration
- **AnalysisService**: Maintains API contract
- Delegates to AnalysisWorkflow.execute()
- Returns structured AnalysisResult
- No breaking changes to API endpoints

## Not Yet Implemented

- Database integration (PostgreSQL)
- Gemini API calls (methods are placeholders in GeminiProvider)
- SQLAlchemy ORM models
- Authentication and authorization
- Actual AI processing and medical reasoning
- Alembic schema migrations
- Advanced error handling
- Geolocation and doctor matching logic
- Emergency detection logic

## Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server
uvicorn app.main:app --reload
```

API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
