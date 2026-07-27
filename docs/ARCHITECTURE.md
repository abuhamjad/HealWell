# HealWell Architecture - v1.0.0

HealWell is a stateless AI-powered health analysis platform built with a modern three-tier architecture: React frontend, FastAPI backend, and LangGraph workflow orchestration.

## High-Level Architecture

```
React Frontend
    ↓
Axios API Client
    ↓
FastAPI Backend
    ↓
AnalysisService
    ↓
LangGraph Workflow
    ↓
OpenAI-Compatible LLM
```

## Frontend Layer

**Framework & Tools:**
- React 19 with TypeScript
- Vite build system
- Tailwind CSS for styling
- Framer Motion for animations
- Lucide React for icons
- Axios for HTTP requests

**Pages:**
- Home/Landing - Hero section with CTA
- Analysis - Symptom input and results display

**Components:**
- Navbar - Navigation
- RiskBadge - Risk level display
- Footer - Footer with links
- HowItWorks - Workflow explanation
- Automation - Visual workflow diagram

**Services:**
- `analysisService` - API communication with backend

**State Management:**
- `useAnalysis` - React hook managing analysis state
- React Hooks for UI state

## Backend Layer

**Framework & Tools:**
- FastAPI for REST API
- Python 3.11+
- Pydantic for data validation
- Uvicorn ASGI server

**API Routes:**
- `POST /api/v1/analysis` - Submit symptoms for analysis
- `GET /` - API health check
- `GET /health` - Health status endpoint

**Services:**
- `AnalysisService` - Orchestrates analysis workflow

**Configuration:**
- Environment-aware settings (development, staging, production)
- CORS configuration per environment
- OpenAI-compatible LLM provider settings

## AI Workflow Layer

**Orchestration:**
- LangGraph - Workflow state machine and graph orchestration
- Multi-agent analysis pipeline

**Workflow Stages:**
1. **Symptom Analysis Agent** - Parse and normalize symptoms
2. **Risk Assessment Agent** - Evaluate medical risk level
3. **Specialist Recommendation Agent** - Determine specialist
4. **Emergency Detection Agent** - Identify emergency conditions
5. **Health Report Agent** - Generate personalized report

**LLM Provider:**
- OpenAI-compatible API (OpenAI, OpenRouter, Ollama, etc.)
- Configurable model selection
- Timeout and retry handling
- JSON response validation

## Data Flow

```
User Input (Symptoms)
    ↓
Frontend Service Call
    ↓
FastAPI /analysis Endpoint
    ↓
AnalysisService.analyze()
    ↓
LangGraph Workflow Execution
    ↓
Symptom Analysis Agent
    ↓
Risk Assessment Agent
    ↓
Specialist Recommendation Agent
    ↓
Emergency Detection Agent
    ↓
Health Report Agent
    ↓
AnalysisResult (JSON)
    ↓
Frontend Display
```

## Response Structure

```json
{
  "success": true,
  "data": {
    "analysis_id": "uuid",
    "risk_level": "low|moderate|high",
    "confidence": 0.0-1.0,
    "specialist": "Specialist recommendation",
    "emergency": false,
    "risk_assessment": { "details": "..." },
    "specialist_recommendation": { "details": "..." },
    "health_report": { "details": "..." },
    "emergency_message": null
  }
}
```

## Project Structure

```
HealWell/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── agents/        # LLM agents
│   │   │   ├── graphs/        # LangGraph workflow
│   │   │   ├── models/        # Data models
│   │   │   ├── prompts/       # Agent prompts
│   │   │   ├── providers/     # LLM providers
│   │   │   ├── state/         # Workflow state
│   │   │   └── workflows/     # Workflow orchestration
│   │   ├── api/
│   │   │   ├── routes/        # API endpoints
│   │   │   └── router.py      # Route registration
│   │   ├── core/
│   │   │   ├── config.py      # Settings
│   │   │   └── constants.py   # Constants
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.ts      # Axios client
│   │   │   ├── endpoints.ts   # API endpoints
│   │   │   └── types.ts       # Request/response types
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── pages/             # Page components
│   │   ├── sections/          # Section components
│   │   ├── services/          # Business logic
│   │   ├── types/             # TypeScript types
│   │   ├── config/            # Configuration
│   │   ├── App.tsx            # Root component
│   │   └── main.tsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
│
├── docs/                      # Documentation
├── README.md                  # Main README
└── LICENSE                    # MIT License
```

## Key Design Principles

**Stateless:** No database, no user sessions, no stored analysis history. Each request is independent.

**Modular:** Clear separation of concerns (frontend, backend, AI workflow).

**OpenAI-Compatible:** LLM provider abstraction allows any OpenAI-compatible API (OpenAI, OpenRouter, Ollama).

**Type-Safe:** Full TypeScript frontend and Pydantic backend with strict typing.

**Scalable:** Stateless architecture enables horizontal scaling without session management.

**Responsive:** Modern UI with mobile support via Tailwind CSS and Framer Motion animations.

## Environment Configuration

### Development
- Debug mode enabled
- Localhost CORS
- Development LLM provider

### Production
- Debug mode disabled
- Strict CORS origins
- Production LLM provider
- Security headers enabled

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Python 3.11+ |
| AI | LangGraph, OpenAI-compatible LLMs |
| Deployment | Docker, Vercel, Railway |
