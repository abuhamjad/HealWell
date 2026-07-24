# HealWell File Dependency Map

## Core Files

### app/main.py
**Purpose**: FastAPI application initialization and middleware setup  
**Imports**:
- fastapi.FastAPI
- CORSMiddleware
- app.core.config.settings
- app.api.router.api_router
**Imported By**:
- CLI (entry point)
- Tests
**Dependencies**: Core, API Router, CORS  
**Runtime Importance**: 🔴 Critical (entry point)

---

### app/core/config.py
**Purpose**: Environment-based settings management  
**Imports**:
- pydantic_settings.BaseSettings
- python-dotenv
**Imported By**:
- main.py (CORS configuration)
- OpenAIProvider (LLM settings)
- All agents (logging level)
**Dependencies**: Environment variables (.env)  
**Runtime Importance**: 🔴 Critical (configuration)

---

### app/core/constants.py
**Purpose**: Application constants and defaults  
**Imports**: None (pure constants)  
**Imported By**:
- API routes (response messages)
- Schemas (constants validation)
**Dependencies**: None  
**Runtime Importance**: 🟢 Low (constants)

---

## API Layer

### app/api/router.py
**Purpose**: Central API router registration  
**Imports**:
- fastapi.APIRouter
- app.api.routes.analysis
- app.api.routes.history
- app.api.routes.doctors
**Imported By**: main.py  
**Dependencies**: Route handlers  
**Runtime Importance**: 🔴 Critical (routing)

### app/api/routes/analysis.py
**Purpose**: POST /api/v1/analysis endpoint  
**Imports**:
- app.schemas.analysis.AnalysisRequest
- app.services.analysis_service.AnalysisService
**Imported By**: router.py  
**Dependencies**: AnalysisService, schemas  
**Runtime Importance**: 🔴 Critical (main endpoint)

### app/api/routes/history.py
**Purpose**: History endpoints (mock)  
**Imported By**: router.py  
**Dependencies**: HistoryService, schemas  
**Runtime Importance**: 🟡 Medium (placeholder)

### app/api/routes/doctors.py
**Purpose**: Doctor finder endpoint (mock)  
**Imported By**: router.py  
**Dependencies**: DoctorService, schemas  
**Runtime Importance**: 🟡 Medium (placeholder)

---

## Schemas

### app/schemas/response.py
**Purpose**: Standardized API response formats  
**Imports**:
- pydantic.BaseModel
**Imported By**:
- All route handlers
- All services
**Dependencies**: None (only Pydantic)  
**Runtime Importance**: 🔴 Critical (response format)

### app/schemas/analysis.py
**Purpose**: AnalysisRequest/Response validation  
**Imported By**: analysis route  
**Dependencies**: Pydantic  
**Runtime Importance**: 🟡 High (API contract)

---

## Services

### app/services/analysis_service.py
**Purpose**: Orchestrate analysis workflow  
**Imports**:
- app.ai.models.AnalysisInput, AnalysisResult
- app.ai.workflows.AnalysisWorkflow
- app.ai.providers.factory.create_provider
**Imported By**: analysis route  
**Dependencies**: Workflow, models, providers  
**Runtime Importance**: 🔴 Critical

### app/services/history_service.py
**Purpose**: History management (placeholder)  
**Imported By**: history route  
**Runtime Importance**: 🟡 Medium

### app/services/doctor_service.py
**Purpose**: Doctor finder (placeholder)  
**Imported By**: doctors route  
**Runtime Importance**: 🟡 Medium

---

## AI Module - Providers

### app/ai/providers/base.py
**Purpose**: Abstract provider interface  
**Imports**:
- abc.ABC, abstractmethod
- app.ai.models
**Imported By**:
- openai_provider.py
- gemini.py
- factory.py
**Dependencies**: Models  
**Runtime Importance**: 🔴 Critical (interface)

### app/ai/providers/openai_provider.py
**Purpose**: Real LLM calls via Groq/OpenAI API  
**Imports**:
- openai.AsyncOpenAI
- app.ai.models (SymptomAnalysis, etc.)
- app.ai.prompts.symptom_prompt
- app.core.config.settings
**Imported By**:
- factory.py
- symptom_agent.py
- Tests
**Dependencies**:
- OpenAI SDK
- Models
- Prompts
- Settings
**Runtime Importance**: 🔴 Critical (LLM)

### app/ai/providers/gemini.py
**Purpose**: Gemini provider (placeholder)  
**Imported By**: factory.py  
**Dependencies**: Base provider  
**Runtime Importance**: 🟡 Medium (future)

### app/ai/providers/factory.py
**Purpose**: Provider factory pattern  
**Imports**:
- openai_provider.OpenAIProvider
- gemini.GeminiProvider
- app.core.config.settings
**Imported By**:
- Services
- Agents
- Tests
**Dependencies**: Providers, settings  
**Runtime Importance**: 🔴 Critical (provider selection)

---

## AI Module - Agents

### app/ai/agents/base.py
**Purpose**: Abstract agent interface  
**Imports**: abc.ABC, abstractmethod  
**Imported By**: All agent implementations  
**Runtime Importance**: 🔴 Critical (interface)

### app/ai/agents/symptom_agent.py
**Purpose**: Real symptom analysis with LLM (v0.7.1)  
**Imports**:
- app.ai.providers.factory.create_provider
- app.ai.models.AnalysisInput
- logging
**Imported By**: langgraph_builder.py  
**Dependencies**: Provider, models, logging  
**Runtime Importance**: 🔴 Critical (real analysis)

### app/ai/agents/risk_agent.py, specialist_agent.py, report_agent.py
**Purpose**: Risk, specialist, report analysis (mock)  
**Imported By**: langgraph_builder.py  
**Dependencies**: Models  
**Runtime Importance**: 🟡 High (mock data)

---

## AI Module - Models

### app/ai/models/analysis.py
**Purpose**: AnalysisInput, AnalysisResult  
**Imported By**:
- Services
- Workflows
- Providers
**Dependencies**: Pydantic  
**Runtime Importance**: 🔴 Critical (core models)

### app/ai/models/symptom.py
**Purpose**: SymptomAnalysis Pydantic model (NEW v0.7.1)  
**Imported By**:
- symptom_agent.py
- openai_provider.py
- Tests
**Dependencies**: Pydantic  
**Runtime Importance**: 🔴 Critical

### app/ai/models/risk.py, specialist.py, report.py
**Purpose**: Risk, specialist, report output models  
**Imported By**:
- Agents
- Services
- Workflows
**Dependencies**: Pydantic  
**Runtime Importance**: 🟡 High

### app/ai/models/__init__.py
**Purpose**: Export all models  
**Imports**: All model classes  
**Imported By**: Everywhere  
**Runtime Importance**: 🔴 Critical

---

## AI Module - Workflows & Graphs

### app/ai/workflows/analysis_workflow.py
**Purpose**: Orchestrate health analysis workflow  
**Imports**:
- app.ai.graphs.langgraph_builder.compile_health_analysis_graph
- app.ai.models
- app.ai.state.HealthAnalysisState
**Imported By**: AnalysisService  
**Dependencies**: Graph builder, models, state  
**Runtime Importance**: 🔴 Critical (orchestration)

### app/ai/graphs/langgraph_builder.py
**Purpose**: LangGraph workflow construction  
**Imports**:
- langgraph.graph.StateGraph
- app.ai.agents (all agents)
- app.ai.state.HealthAnalysisState
**Imported By**: analysis_workflow.py  
**Dependencies**: LangGraph, agents, state  
**Runtime Importance**: 🔴 Critical (workflow)

### app/ai/state/health_state.py
**Purpose**: HealthAnalysisState TypedDict  
**Imports**: Models, typing  
**Imported By**:
- langgraph_builder.py
- Agents
- Workflows
**Dependencies**: Models  
**Runtime Importance**: 🔴 Critical (shared state)

---

## AI Module - Prompts

### app/ai/prompts/symptom_prompt.py
**Purpose**: Symptom analysis prompt generation (real v0.7.1)  
**Imports**: None (pure string functions)  
**Imported By**: openai_provider.py  
**Dependencies**: None  
**Runtime Importance**: 🔴 Critical

### app/ai/prompts/risk_prompt.py, specialist_prompt.py, report_prompt.py
**Purpose**: Prompt templates (placeholder)  
**Imported By**: Agent implementations (future)  
**Runtime Importance**: 🟡 Medium

---

## Dependency Graph (Critical Path)

```
HTTP Request
    ↓
main.py (entry)
    ↓
api/router.py (routing)
    ↓
api/routes/analysis.py (handler)
    ├─ schemas/analysis.py (validation)
    ├─ schemas/response.py (response format)
    └─ services/analysis_service.py (orchestration)
        └─ ai/workflows/analysis_workflow.py (workflow)
            └─ ai/graphs/langgraph_builder.py (LangGraph)
                ├─ ai/agents/symptom_agent.py (execution)
                │   ├─ ai/providers/factory.py (provider selection)
                │   └─ ai/providers/openai_provider.py (LLM call)
                │       ├─ ai/prompts/symptom_prompt.py (prompt)
                │       ├─ ai/models/symptom.py (output model)
                │       └─ openai.AsyncOpenAI (Groq API)
                ├─ ai/agents/risk_agent.py
                ├─ ai/agents/specialist_agent.py
                └─ ai/agents/report_agent.py
                    └─ ai/models/* (output models)

Configuration (across all layers):
    app/core/config.py (settings)
    app/core/constants.py (constants)
```

---

## Circular Dependency Analysis

**Status**: ✅ No circular dependencies detected

All imports follow hierarchy:
1. Core (config, constants)
2. Schemas
3. Models
4. Providers
5. Prompts
6. Agents
7. State
8. Workflows
9. Services
10. Routes
11. Main

---

## Module Size (Approximate LOC)

| Module | LOC | Type |
|--------|-----|------|
| main.py | 50 | Core |
| config.py | 150 | Config |
| analysis_service.py | 50 | Service |
| openai_provider.py | 150 | Provider (real) |
| symptom_agent.py | 50 | Agent (real) |
| langgraph_builder.py | 50 | Graph |
| risk_agent.py | 30 | Agent (mock) |
| specialist_agent.py | 30 | Agent (mock) |
| report_agent.py | 40 | Agent (mock) |
| Models (total) | 150 | Models |
| Prompts (total) | 100 | Templates |
| API routes (total) | 100 | Routes |
| Schemas (total) | 100 | Schemas |

**Total Backend**: ~1,100 LOC

---

## Modification Impact Analysis

### Impact of changes to core files:

**api/router.py**:
- Impact: All API endpoints (HIGH)
- Change frequency: RARE
- Test impact: All endpoint tests

**openai_provider.py**:
- Impact: All LLM calls (CRITICAL)
- Change frequency: COMMON (adding provider methods)
- Test impact: Agent tests, integration tests

**langgraph_builder.py**:
- Impact: Workflow execution (CRITICAL)
- Change frequency: MEDIUM (adding agents)
- Test impact: Workflow tests

**symptom_agent.py**:
- Impact: Symptom analysis (CRITICAL)
- Change frequency: RARE (stable in v0.7.1+)
- Test impact: Symptom analysis tests

---

## Summary

Critical dependencies:
- Config → Everything (settings cascade)
- Models → Providers, Agents (type definitions)
- Providers → Agents (LLM implementation)
- Agents → Workflow (execution)
- Workflow → Service → Route (data flow)

Safe to modify:
- Constants (no side effects)
- Individual agents (one at a time)
- Prompts (just text changes)
- Routes (endpoint changes)

High-risk modifications:
- Core workflow architecture
- Provider interface changes
- Model structure changes
- Config schema changes
