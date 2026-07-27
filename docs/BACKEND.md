# HealWell Backend Documentation - v1.0.0

Production-ready backend for HealWell v1.0.0. FastAPI REST API with LangGraph workflow orchestration and OpenAI-compatible LLM integration.

## Status

✅ **v1.0.0 Production Release** - Complete stateless health analysis backend with real OpenAI LLM integration and comprehensive workflow orchestration.

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application factory
│   ├── ai/
│   │   ├── models/             # Data models
│   │   │   ├── analysis.py     # AnalysisInput, AnalysisResult
│   │   │   ├── risk.py         # RiskAssessment
│   │   │   ├── specialist.py   # SpecialistRecommendation
│   │   │   └── report.py       # HealthReport
│   │   ├── providers/          # LLM provider abstraction
│   │   │   ├── base.py         # BaseProvider interface
│   │   │   ├── openai_provider.py  # OpenAI implementation
│   │   │   └── factory.py      # Provider factory
│   │   ├── prompts/            # Agent prompt templates
│   │   │   ├── symptom_prompt.py
│   │   │   ├── risk_prompt.py
│   │   │   ├── specialist_prompt.py
│   │   │   └── report_prompt.py
│   │   ├── agents/             # LangGraph agents
│   │   │   ├── base.py         # BaseAgent interface
│   │   │   ├── symptom_agent.py
│   │   │   ├── risk_agent.py
│   │   │   ├── specialist_agent.py
│   │   │   └── report_agent.py
│   │   ├── state/              # Workflow state
│   │   │   └── health_state.py # HealthAnalysisState (TypedDict)
│   │   ├── graphs/             # LangGraph workflow
│   │   │   ├── health_graph.py
│   │   │   └── langgraph_builder.py
│   │   └── workflows/          # Workflow orchestration
│   │       └── analysis_workflow.py
│   ├── api/
│   │   ├── router.py           # API route registration
│   │   └── routes/
│   │       └── analysis.py     # Analysis endpoints
│   ├── core/
│   │   ├── config.py           # Environment configuration
│   │   └── constants.py        # Application constants
│   ├── schemas/                # Request/response schemas
│   │   ├── analysis.py         # AnalysisRequest, AnalysisResponse
│   │   └── response.py         # ApiResponse envelope
│   └── services/
│       └── analysis_service.py # Business logic
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md                   # Setup instructions
```

## Technology Stack

- **FastAPI** - Modern async Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Type-safe data validation
- **LangGraph** - Workflow orchestration
- **OpenAI API** - LLM provider (supports OpenAI, OpenRouter, Ollama)
- **Python 3.11+** - Runtime environment

## Architecture

### Core Configuration (`app/core/`)

**config.py:**
- Environment-aware settings (development, staging, production)
- CORS configuration per environment
- LLM provider configuration
- Logging configuration

**constants.py:**
- API metadata and versioning
- Risk level constants
- Response messages

### API Routes (`app/api/`)

**router.py:**
- Centralized route registration
- `/api/v1` versioning prefix

**routes/analysis.py:**
- `POST /api/v1/analysis` - Submit symptoms for analysis
- Single active endpoint with full workflow

### Schemas (`app/schemas/`)

**analysis.py:**
- `AnalysisRequest` - User input (symptoms, optional medical history)
- `AnalysisResponse` - Complete analysis result

**response.py:**
- `ApiResponse` - Envelope structure for all responses
- `success_response()` - Helper for successful responses

### Main Application (`app/main.py`)

```python
# FastAPI app factory
# CORS middleware configured per environment
# Health check endpoints (GET /, GET /health)
# API route registration
```

## AI/LLM Layer

### Provider Pattern (`app/ai/providers/`)

**base.py:**
```python
class BaseProvider(ABC):
    async def call_llm(self, prompt: str) -> str
    async def structured_call(self, prompt: str, schema: dict) -> dict
```

**openai_provider.py:**
- OpenAI-compatible API client
- Timeout and retry logic
- JSON response validation
- Medical context integration

**factory.py:**
```python
def create_provider() -> BaseProvider:
    return OpenAIProvider(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
        timeout=settings.LLM_TIMEOUT
    )
```

### Prompt Templates (`app/ai/prompts/`)

Each prompt enhances the LLM with:
- Medical domain knowledge
- Structured output expectations
- Optional medical history, medications, allergies
- Safety and accuracy constraints

### Agents (`app/ai/agents/`)

Each agent processes HealthAnalysisState and performs its stage:

1. **SymptomAgent** - Parse and normalize symptoms
2. **RiskAgent** - Assess medical risk level
3. **SpecialistAgent** - Determine specialist recommendation
4. **EmergencyAgent** - Detect emergency conditions
5. **ReportAgent** - Generate personalized health report

### Workflow State (`app/ai/state/`)

**HealthAnalysisState (TypedDict):**

```python
{
    "session_id": str,                              # Unique workflow ID
    "user_input": str,                              # Raw symptoms
    "analysis_input": AnalysisInput,                # Parsed input
    "symptom_analysis": dict,                       # Detected symptoms
    "risk_assessment": RiskAssessment,              # Risk level & confidence
    "specialist_recommendation": SpecialistRecommendation,  # Specialist type
    "health_report": HealthReport,                  # Report & recommendations
    "workflow_status": str,                         # "started", "in_progress", "completed"
    "current_step": str,                            # Last executed agent
    "errors": List[str],                            # Error tracking
    "metadata": dict,                               # Medical context
}
```

### LangGraph Workflow (`app/ai/graphs/`)

**langgraph_builder.py:**

```python
def compile_health_analysis_graph() -> CompiledStateGraph:
    graph = StateGraph(HealthAnalysisState)
    
    # Add nodes (agents)
    graph.add_node("symptom_analysis", symptom_agent)
    graph.add_node("risk_assessment", risk_agent)
    graph.add_node("specialist_recommendation", specialist_agent)
    graph.add_node("emergency_detection", emergency_agent)
    graph.add_node("health_report", report_agent)
    
    # Define edges (execution order)
    graph.add_edge("START", "symptom_analysis")
    graph.add_edge("symptom_analysis", "risk_assessment")
    graph.add_edge("risk_assessment", "specialist_recommendation")
    graph.add_edge("specialist_recommendation", "emergency_detection")
    graph.add_edge("emergency_detection", "health_report")
    graph.add_edge("health_report", "END")
    
    return graph.compile()
```

### Workflow Execution Pipeline

```
POST /api/v1/analysis
    ↓
AnalysisService.analyze()
    ↓
AnalysisWorkflow.execute()
    ↓
compiled_graph.ainvoke(initial_state)
    ↓
symptom_analysis (LLM call)
    ↓
risk_assessment (LLM call)
    ↓
specialist_recommendation (LLM call)
    ↓
emergency_detection (LLM call)
    ↓
health_report (LLM call)
    ↓
AnalysisResult
    ↓
FastAPI Response → Frontend
```

### Services (`app/services/`)

**AnalysisService:**
```python
class AnalysisService:
    async def analyze(self, symptoms: str) -> AnalysisResult:
        workflow = AnalysisWorkflow()
        result = await workflow.execute(AnalysisInput(symptoms=symptoms))
        return result
```

## Workflow Features

✅ **AI Workflow:**
- Multi-agent orchestration via LangGraph
- Sequential execution with state sharing
- Real OpenAI-compatible LLM calls
- Async execution for scalability

✅ **Medical Analysis:**
- Symptom parsing and normalization
- Risk assessment (low, moderate, high)
- Specialist recommendations
- Emergency detection
- Health report generation

✅ **Production Ready:**
- Error handling and logging
- Type safety via Pydantic
- Environment-aware configuration
- Timeout and retry logic
- JSON schema validation

## Configuration

### Environment Variables

```bash
# Core
ENVIRONMENT=production
DEBUG=False
API_TITLE=HealWell API
API_VERSION=1.0.0

# Deployment
HOST=0.0.0.0
PORT=8000

# Frontend URLs
FRONTEND_URL=http://localhost:5173
FRONTEND_STAGING_URL=http://staging.healwell.app
FRONTEND_PRODUCTION_URL=https://healwell.app

# CORS
CORS_ORIGINS=http://localhost:5173,https://healwell.app

# LLM Provider
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4
LLM_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Running the Backend

### Development

```bash
cd backend

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your OpenAI API key

uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

**Swagger UI:** `http://localhost:8000/docs`

**ReDoc:** `http://localhost:8000/redoc`

## Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Analysis Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache"}'
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

1. Set environment variables in production environment
2. Ensure OpenAI API key is configured
3. Configure CORS origins for your domain
4. Run with production settings

## Performance

- **Stateless:** Enables horizontal scaling
- **Async:** Non-blocking I/O
- **Timeout:** 30s max per analysis
- **Caching:** Provider-level response caching
- **Optimization:** Efficient state management

## Error Handling

All errors return structured responses:

```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error"
}
```

Status codes:
- 200: Success
- 400: Invalid request
- 500: Server error
