# HealWell Project Overview

## Executive Summary

HealWell is an AI-powered healthcare accessibility platform designed to democratize medical guidance for underserved populations. It combines speech-to-text input, intelligent symptom analysis, and specialist matchmaking to provide accessible healthcare guidance through an intuitive web interface.

**Current Version**: v0.7.1 (Real Symptom Analysis Agent)
**Status**: Development - Core AI foundation complete, expanding AI capabilities

---

## Project Purpose

### Problem Statement
Millions of people lack access to timely, reliable medical information and specialist care due to:
- Geographic barriers (remote areas)
- Economic constraints (cost of consultations)
- Infrastructure limitations (poor connectivity)
- Language barriers
- Health literacy gaps

### Solution
HealWell provides an intelligent system that:
1. **Accepts patient input** via natural speech or text
2. **Analyzes symptoms** using AI to identify patterns and risks
3. **Assesses urgency** to determine if emergency care is needed
4. **Recommends specialists** for appropriate follow-up care
5. **Generates comprehensive reports** for patient education

### Alignment
**UN SDG 3 Goal**: Good Health and Well-Being
- Ensure healthy lives and promote well-being for all at all ages
- Reduce premature mortality from non-communicable diseases
- Promote mental health and well-being

---

## Technology Stack

### Frontend
- **Framework**: React 18.x with TypeScript
- **Styling**: Tailwind CSS (utility-first CSS framework)
- **Animations**: Framer Motion
- **State Management**: React Context API + Hooks
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (modern async Python web framework)
- **Server**: Uvicorn (ASGI application server)
- **Validation**: Pydantic 2.x (data validation using type hints)
- **Configuration**: Pydantic Settings (environment-based config)
- **Type Hints**: Python 3.9+ type annotations

### AI & Automation
- **Workflow Orchestration**: LangGraph 0.0.29
- **LLM Provider**: OpenAI-compatible API (Groq)
- **LLM Integration**: Python OpenAI SDK (>=2.46.0)
- **Provider Abstraction**: Custom BaseProvider pattern

### Infrastructure (Planned)
- **Database**: PostgreSQL (for data persistence)
- **Deployment**: TBD (AWS/GCP/Azure)
- **Analytics**: TBD
- **Logging**: Python logging module

---

## Architecture Philosophy

### Core Principles

1. **Separation of Concerns**
   - Frontend: User interface and experience
   - Backend: Business logic and data processing
   - AI: Intelligence and medical reasoning
   - Database: Persistent data storage

2. **Provider Abstraction**
   - Multiple LLM providers can be swapped (OpenAI, Gemini, Groq, etc.)
   - Provider factory pattern allows easy switching
   - No provider-specific logic in agents or services

3. **Service-Oriented Architecture**
   - Clear service boundaries (Analysis, History, Doctor, Report)
   - Services orchestrate workflows
   - Dependency injection for flexibility

4. **Async-First Design**
   - All I/O operations are asynchronous
   - LangGraph enables async agent execution
   - FastAPI handles async naturally

5. **Type Safety**
   - Pydantic models for all data structures
   - Type hints throughout codebase
   - Runtime validation of all inputs

6. **Workflow-Centric**
   - LangGraph orchestrates multi-step medical reasoning
   - Shared state pattern for agent coordination
   - Clear data flow through sequential agent nodes

---

## Major Modules

### 1. Frontend Module (`frontend/`)
```
frontend/
├── src/
│   ├── pages/           # Page components (Landing, Analysis, Results, History)
│   ├── components/      # Reusable UI components
│   ├── sections/        # Page sections
│   ├── services/        # API client layer (Axios)
│   ├── hooks/           # Custom React hooks
│   ├── api/             # API route definitions
│   ├── config/          # Configuration
│   ├── types/           # TypeScript type definitions
│   └── utils/           # Utility functions
├── App.tsx              # Root component
├── main.tsx             # Entry point
└── index.css            # Global styles
```

**Responsibility**: User interface, form handling, API communication, state management

### 2. Backend API Module (`backend/app/api/`)
```
api/
├── routes/
│   ├── analysis.py      # POST /api/v1/analysis
│   ├── history.py       # GET/POST /api/v1/history
│   └── doctors.py       # GET /api/v1/doctors
└── router.py            # Central API router
```

**Responsibility**: HTTP endpoints, request/response handling, API contracts

### 3. Services Module (`backend/app/services/`)
```
services/
├── analysis_service.py      # Orchestrates analysis workflow
├── history_service.py       # Manages medical history
├── doctor_service.py        # Finds nearby doctors
└── report_service.py        # Manages report generation
```

**Responsibility**: Business logic, workflow orchestration, service interfaces

### 4. AI Module (`backend/app/ai/`)
```
ai/
├── providers/               # LLM provider implementations
│   ├── base.py             # BaseProvider abstract interface
│   ├── openai_provider.py  # Groq/OpenAI-compatible API
│   ├── gemini.py           # Google Gemini (placeholder)
│   └── factory.py          # Provider factory
├── agents/                  # Multi-step analysis agents
│   ├── base.py             # BaseAgent abstract interface
│   ├── symptom_agent.py    # Real LLM symptom analysis
│   ├── risk_agent.py       # Risk assessment (mock)
│   ├── specialist_agent.py # Specialist recommendation (mock)
│   └── report_agent.py     # Report generation (mock)
├── prompts/                # LLM prompt templates
│   ├── symptom_prompt.py   # Symptom analysis prompt
│   ├── risk_prompt.py      # Risk assessment prompt
│   ├── specialist_prompt.py # Specialist recommendation prompt
│   └── report_prompt.py    # Report generation prompt
├── models/                 # Pydantic data models
│   ├── analysis.py         # AnalysisInput, AnalysisResult
│   ├── symptom.py          # SymptomAnalysis
│   ├── risk.py             # RiskAssessment
│   ├── specialist.py       # SpecialistRecommendation
│   └── report.py           # HealthReport
├── state/                  # Workflow state
│   └── health_state.py     # HealthAnalysisState (TypedDict)
├── workflows/              # Workflow orchestration
│   └── analysis_workflow.py # AnalysisWorkflow
└── graphs/                 # LangGraph definitions
    ├── langgraph_builder.py # Graph builder and compiler
    └── health_graph.py      # Graph visualization docs
```

**Responsibility**: AI logic, LLM communication, medical reasoning, workflow orchestration

### 5. Core Module (`backend/app/core/`)
```
core/
├── config.py           # Environment-based settings
└── constants.py        # Application constants
```

**Responsibility**: Configuration management, constants

### 6. Schemas Module (`backend/app/schemas/`)
```
schemas/
├── analysis.py         # AnalysisRequest, AnalysisResponse
├── history.py          # History request/response schemas
├── doctor.py           # Doctor schemas
└── response.py         # ApiResponse, success/error helpers
```

**Responsibility**: Data validation, API contracts

---

## Current Version: v0.7.1

### Version Description
**Real Symptom Analysis Agent** - The SymptomAgent now uses real LLM calls instead of hardcoded mock data.

### Key Features Implemented
- ✅ Frontend UI for symptom input
- ✅ Backend API with FastAPI
- ✅ LangGraph workflow orchestration
- ✅ Real symptom analysis via Groq API (v0.7.1)
- ✅ Service-oriented architecture
- ✅ Type-safe data validation

### Features In Development
- 🔄 Real risk assessment agent (v0.7.2)
- 🔄 Real specialist recommendation (v0.7.3)
- 🔄 Real report generation (v0.7.4)

### Features Planned
- ⏳ Medical history integration
- ⏳ Doctor finder with geolocation
- ⏳ Report PDF export
- ⏳ Analytics dashboard
- ⏳ Database persistence
- ⏳ Authentication
- ⏳ Production deployment

---

## Development Roadmap

### Completed Milestones

| Version | Name | Status | Details |
|---------|------|--------|---------|
| v0.1 | Foundation | ✅ Complete | Project setup, documentation, architecture |
| v0.2 | Frontend | ✅ Complete | React UI, components, pages |
| v0.3 | Backend | ✅ Complete | FastAPI foundation, endpoints |
| v0.4 | Integration | ✅ Complete | Frontend-Backend communication |
| v0.5 | AI Foundation | ✅ Complete | AI module, providers, agents, models |
| v0.6 | LangGraph Workflow | ✅ Complete | Workflow orchestration, mock agents |
| v0.7.0 | Provider Foundation | ✅ Complete | Groq integration, provider pattern |

### Active Development

| Version | Name | Status | Details |
|---------|------|--------|---------|
| v0.7.1 | Real Symptom Analysis | ✅ Complete | SymptomAgent with real LLM calls |
| v0.7.2 | Real Risk Agent | 🔄 Planned | Replace RiskAgent mock data |
| v0.7.3 | Real Specialist Agent | 🔄 Planned | Replace SpecialistAgent mock data |
| v0.7.4 | Real Report Agent | 🔄 Planned | Replace ReportAgent mock data |

### Future Phases

| Version | Name | Status | Details |
|---------|------|--------|---------|
| v0.8 | Application Features | ⏳ Pending | History, doctors, reports, analytics |
| v0.9 | Production Hardening | ⏳ Pending | Database, logging, security, performance |
| v1.0 | Release | ⏳ Pending | Production deployment |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Pages: Landing, Analysis, Results, History          │   │
│  │ Components: Reusable UI elements                     │   │
│  │ Services: Axios API client                           │   │
│  │ Hooks: Custom React logic                            │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/HTTPS
                           │ JSON Payloads
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Routers: /api/v1/analysis, /history, /doctors       │   │
│  │ Services: Analysis, History, Doctor, Report         │   │
│  │ Schemas: Pydantic models for validation             │   │
│  │ Config: Environment-based settings                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              AI Module (Intelligence)                │   │
│  │                                                      │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │         LangGraph Workflow                   │   │   │
│  │  │  Orchestrates multi-step medical reasoning  │   │   │
│  │  │  ┌───────┐  ┌───────┐  ┌──────┐  ┌────────┐│   │   │
│  │  │  │Symptom│→ │Risk   │→ │Spec. │→ │Report ││   │   │
│  │  │  │Agent  │  │Agent  │  │Agent │  │Agent  ││   │   │
│  │  │  └───────┘  └───────┘  └──────┘  └────────┘│   │   │
│  │  │           HealthAnalysisState              │   │   │
│  │  │      Shared state flows through agents     │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  │                           │                        │   │
│  │  ┌──────────────────────┐ │                        │   │
│  │  │  Providers           │ │                        │   │
│  │  │  ├─ OpenAI          │ │                        │   │
│  │  │  ├─ Gemini          │ │                        │   │
│  │  │  └─ BaseProvider    │ │                        │   │
│  │  └──────────────────────┘ │                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│                    ┌─────────────────┐                      │
│                    │ LLM Provider    │                      │
│                    │ (Groq/OpenAI)   │                      │
│                    └─────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Groq API        │
                  │  (OpenAI-compat) │
                  └──────────────────┘
```

---

## Key Design Decisions

### 1. Why LangGraph?
- **Sequential workflow orchestration**: Medical reasoning requires ordered steps
- **Shared state pattern**: All agents access/modify common state
- **Clear data flow**: Easy to trace data transformations
- **Extensible**: Simple to add new agents

### 2. Why Provider Pattern?
- **Flexibility**: Swap LLM providers without changing agent code
- **Testability**: Mock providers for testing
- **Future-proof**: Can add new providers (Claude, Llama, etc.)
- **Configuration-driven**: Provider selection via environment variables

### 3. Why Service Layer?
- **Separation of concerns**: Services isolate business logic
- **Testability**: Easy to mock services
- **Reusability**: Services can be used by multiple routes
- **Clear boundaries**: Explicit service responsibilities

### 4. Why Async/Await?
- **Performance**: Non-blocking I/O operations
- **Scalability**: Handle many concurrent requests
- **Natural in FastAPI**: Async is first-class citizen
- **Matches LangGraph**: Async providers and agents

### 5. Why TypedDict for State?
- **Type safety**: Type hints for state fields
- **Performance**: No runtime overhead vs. classes
- **Simplicity**: Just a dictionary with type annotations
- **LangGraph compatible**: Works naturally with LangGraph

---

## Communication Patterns

### Frontend → Backend
1. **HTTP REST**: Standard JSON over HTTPS
2. **Axios client**: Abstraction over fetch
3. **Service layer**: Business logic in services
4. **Hooks**: React custom hooks for API calls

### Backend → AI
1. **Service layer**: Creates workflow input
2. **AnalysisWorkflow**: Orchestrates execution
3. **LangGraph**: Executes agents in sequence
4. **Agents**: Modify shared state

### AI → LLM Provider
1. **Provider abstraction**: BaseProvider interface
2. **Factory pattern**: Selects provider at runtime
3. **OpenAI SDK**: Communicates with Groq API
4. **JSON format**: Structured prompts and responses

### Workflow State
```
HealthAnalysisState
├── session_id: str
├── user_input: str
├── analysis_input: AnalysisInput
├── symptom_analysis: dict (populated by SymptomAgent)
├── risk_assessment: RiskAssessment (populated by RiskAgent)
├── specialist_recommendation: SpecialistRecommendation (populated by SpecialistAgent)
├── health_report: HealthReport (populated by ReportAgent)
├── workflow_status: str
├── current_step: str
├── errors: List[str]
└── metadata: dict
```

---

## Performance Characteristics

### Current
- API response time: ~3-5 seconds (includes LLM call)
- Frontend rendering: <100ms
- State transfer: <10KB typical payload

### Scalability
- **Horizontal**: Stateless backend can be horizontally scaled
- **Database**: Will be bottleneck once persistence added
- **LLM**: Provider rate limits will be constraint

---

## Security Considerations

### Current Implementation
- ✅ CORS properly configured
- ✅ Input validation via Pydantic
- ✅ Environment variables for secrets
- ⚠️ No authentication (placeholder)
- ⚠️ No authorization (placeholder)
- ⚠️ No HTTPS enforcement (dev environment)

### Planned for v0.9
- Authentication (JWT or OAuth)
- Authorization (role-based access)
- Input sanitization
- Rate limiting
- HTTPS enforcement
- GDPR compliance for medical data

---

## Deployment Architecture (Planned)

```
┌──────────────────────────────────────────┐
│      Frontend (React SPA)                │
│  Hosted on: Vercel/Netlify/S3            │
│  CDN: CloudFront/Cloudflare              │
└──────────────────────────────────────────┘
                   │
                   │
┌──────────────────────────────────────────┐
│      Backend (FastAPI)                   │
│  Hosted on: AWS/GCP/Azure (Docker)       │
│  Load Balancer: AWS ALB                  │
│  Auto-scaling: Based on CPU/Memory       │
└──────────────────────────────────────────┘
                   │
                   │
┌──────────────────────────────────────────┐
│      Database (PostgreSQL)               │
│  Managed: AWS RDS/GCP Cloud SQL          │
│  Backups: Automated daily                │
│  Replicas: Read replicas for scale       │
└──────────────────────────────────────────┘
                   │
                   │
┌──────────────────────────────────────────┐
│      LLM Provider (Groq)                 │
│  API calls: ~100ms latency               │
│  Rate limits: Provider-dependent         │
└──────────────────────────────────────────┘
```

---

## Summary

HealWell is a modern, well-architected healthcare AI platform combining:
- **Clean architecture** with clear separation of concerns
- **Type-safe** design with Pydantic and TypeScript
- **Async-first** for scalability and performance
- **Provider abstraction** for flexibility
- **AI-powered** medical reasoning via LangGraph
- **Extensible** design for future growth

The foundation is solid for implementing v0.7.2+ which will replace mock agents with real LLM-powered analysis across all medical reasoning steps.
