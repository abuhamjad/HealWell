# HealWell Architecture Context Pack

Complete technical documentation for the HealWell AI-powered healthcare platform. This context pack replaces future architecture audits and enables new developers to understand the entire system.

**Version**: v0.7.1 (Real Symptom Analysis Agent)  
**Generated**: July 2024  
**Audience**: Developers, architects, maintainers

---

## 📚 Documentation Index

### 1. **[PROJECT_OVERVIEW.md](01_PROJECT_OVERVIEW.md)** 
High-level overview of HealWell's purpose, technology stack, architecture philosophy, and roadmap.
- Project mission and problem statement
- Technology stack (React, FastAPI, LangGraph, Groq)
- Architecture philosophy and design decisions
- Completed and planned milestones
- High-level architecture diagram

### 2. **[BACKEND_ARCHITECTURE.md](02_BACKEND_ARCHITECTURE.md)**
Detailed backend structure, services, routers, and dependency flow.
- Folder structure and organization
- API layer (routes, endpoints)
- Service layer architecture
- Schemas and validation
- Data flow lifecycle
- Error handling patterns

### 3. **[AI_ARCHITECTURE.md](03_AI_ARCHITECTURE.md)**
AI module design with LangGraph, agents, providers, and execution flow.
- LangGraph workflow orchestration
- HealthAnalysisState and shared state
- Provider abstraction pattern
- Agent architecture and responsibilities
- Prompt templates
- Execution lifecycle with detailed flow

### 4. **[RUNTIME_FLOW.md](04_RUNTIME_FLOW.md)**
Complete sequence diagrams showing request lifecycle from user input to API response.
- Step-by-step request flow
- Performance timeline (3-5 seconds typical)
- Detailed state progression
- Error handling flow
- Concurrent request handling

### 5. **[DATA_MODELS.md](05_DATA_MODELS.md)**
Comprehensive documentation of all Pydantic models and data structures.
- Input/output models (AnalysisInput, AnalysisResult)
- Agent output models (SymptomAnalysis, RiskAssessment, etc.)
- Workflow state model (HealthAnalysisState)
- API request/response models
- Model relationships and validation rules

### 6. **[API_REFERENCE.md](06_API_REFERENCE.md)**
Complete REST API endpoint documentation with examples.
- POST /api/v1/analysis (real analysis endpoint)
- GET /api/v1/history (placeholder)
- POST /api/v1/history (placeholder)
- GET /api/v1/doctors (placeholder)
- Health endpoints
- Response formats and error codes

### 7. **[PROVIDER_SYSTEM.md](07_PROVIDER_SYSTEM.md)**
LLM provider infrastructure and implementation details.
- BaseProvider interface
- OpenAIProvider (Groq-compatible, active v0.7.1)
- GeminiProvider (placeholder)
- Provider factory pattern
- Environment configuration
- How to add new providers

### 8. **[AGENT_REFERENCE.md](08_AGENT_REFERENCE.md)**
Detailed documentation of all agents and their responsibilities.
- BaseAgent interface
- SymptomAgent (real LLM calls, v0.7.1)
- RiskAgent (mock data)
- SpecialistAgent (mock data)
- ReportAgent (mock data)
- Agent development patterns
- Error handling in agents

### 9. **[FRONTEND_BACKEND_MAPPING.md](09_FRONTEND_BACKEND_MAPPING.md)**
Maps frontend components to backend APIs and workflows.
- Component → API endpoint mappings
- State management flow
- Request/response examples
- Error handling bridge
- Frontend-backend communication
- Integration testing strategy

### 10. **[IMPLEMENTATION_STATUS.md](10_IMPLEMENTATION_STATUS.md)**
Current implementation status with feature matrix and roadmap.
- Feature completion status (40% complete)
- Module completion breakdown
- API endpoint status
- Agent implementation status
- Technical debt inventory
- Testing status and coverage

### 11. **[KNOWN_ISSUES.md](11_KNOWN_ISSUES.md)**
Comprehensive list of known limitations, issues, and architectural risks.
- Critical issues (none currently)
- High priority issues (mock data, no persistence, no auth)
- Medium priority issues (limited context, no emergency detection)
- Low priority issues (performance, configuration)
- Architectural risks and mitigations

### 12. **[DEVELOPMENT_GUIDE.md](12_DEVELOPMENT_GUIDE.md)**
Step-by-step guide for developers implementing new features.
- Environment setup instructions
- How to implement a new agent
- How to add LLM calls via providers
- How to create prompts
- How to add API endpoints
- Coding conventions and best practices
- Testing guidelines

### 13. **[FILE_DEPENDENCY_MAP.md](13_FILE_DEPENDENCY_MAP.md)**
File-level dependency analysis and impact assessment.
- Core files and their dependencies
- API layer structure
- AI module organization
- Dependency graph visualization
- Circular dependency analysis
- Module size and modification impact

### 14. **[DEBUGGING_GUIDE.md](14_DEBUGGING_GUIDE.md)**
Practical debugging strategies and troubleshooting guide.
- Common issues and solutions
- Workflow debugging techniques
- Logging best practices
- Testing providers and agents independently
- Browser console debugging
- Performance profiling tips

---

## 🗺️ Navigation Guide

### For New Developers
Start here → **PROJECT_OVERVIEW** → **BACKEND_ARCHITECTURE** → **DEVELOPMENT_GUIDE**

### For API Integration
**API_REFERENCE** → **FRONTEND_BACKEND_MAPPING** → **DATA_MODELS**

### For AI/LLM Work
**AI_ARCHITECTURE** → **AGENT_REFERENCE** → **PROVIDER_SYSTEM** → **DEVELOPMENT_GUIDE**

### For Debugging Issues
**DEBUGGING_GUIDE** → Relevant section in other docs

### For Architecture Understanding
**PROJECT_OVERVIEW** → **BACKEND_ARCHITECTURE** → **AI_ARCHITECTURE** → **RUNTIME_FLOW**

### For Feature Implementation
**IMPLEMENTATION_STATUS** → **DEVELOPMENT_GUIDE** → **KNOWN_ISSUES**

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Version | v0.7.1 |
| Status | Development |
| Completion | 40% |
| Total LOC (Backend) | ~1,100 |
| Typical Response Time | 3-5 seconds |
| API Endpoints | 6 (1 real, 5 placeholder) |
| Agents | 4 (1 real, 3 mock) |
| Providers | 2 (OpenAI active, Gemini placeholder) |

---

## 🎯 Key Milestones

| Version | Status | Highlights |
|---------|--------|-----------|
| **v0.7.0** | ✅ Done | Provider infrastructure, Groq API configured |
| **v0.7.1** | ✅ Done | Real SymptomAgent with LLM calls |
| **v0.7.2** | 📋 Next | Real RiskAgent implementation |
| **v0.7.3** | 📋 Planned | Real SpecialistAgent implementation |
| **v0.7.4** | 📋 Planned | Real ReportAgent implementation |
| **v0.8** | ⏳ Future | Application features, medical history, doctor finder |
| **v0.9** | ⏳ Future | Production hardening, database, authentication |
| **v1.0** | ⏳ Future | Production release |

---

## 🔧 Technology Stack

**Frontend**:
- React 18 + TypeScript
- Tailwind CSS
- Framer Motion
- Axios

**Backend**:
- FastAPI 0.104
- Python 3.9+
- Pydantic 2.5
- Uvicorn

**AI & Automation**:
- LangGraph 0.0.29
- OpenAI SDK (for Groq compatibility)
- Groq API (primary LLM provider)
- Google Gemini (placeholder for future)

**Infrastructure** (Planned):
- PostgreSQL (database)
- Docker (containerization)
- AWS/GCP (deployment)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Groq API key (free at https://console.groq.com/)

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # Add your Groq API key
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

---

## 🏗️ Architecture at a Glance

```
┌─────────────────────┐
│   Frontend (React)  │
└──────────┬──────────┘
           │ HTTP/JSON
           ▼
┌─────────────────────┐
│  FastAPI Backend    │
│  - Routes           │
│  - Services         │
│  - Schemas          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    AI Module        │
│  - LangGraph        │
│  - Agents (4)       │
│  - Providers        │
│  - Prompts          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   LLM Provider      │
│   (Groq/OpenAI)     │
└─────────────────────┘
```

---

## 📖 Documentation Philosophy

This context pack is designed to:
- ✅ **Replace future architecture audits**: No need to reverse-engineer
- ✅ **Accelerate onboarding**: New developers can understand the system
- ✅ **Enable independent work**: Developers can implement features without constant guidance
- ✅ **Facilitate code reviews**: Clear standards and patterns documented
- ✅ **Guide future development**: Roadmap and best practices established

---

## 🔍 What's Documented

- ✅ Architecture and design patterns
- ✅ All major modules and their responsibilities
- ✅ Data flow from request to response
- ✅ All API endpoints and request/response formats
- ✅ All data models and validation rules
- ✅ LLM provider system and provider implementations
- ✅ Agents and workflow orchestration
- ✅ Frontend-backend communication
- ✅ Development and testing guidelines
- ✅ Debugging strategies and troubleshooting
- ✅ File dependencies and impact analysis
- ✅ Known issues and limitations
- ✅ Feature roadmap and implementation status

---

## 🚫 What's NOT Documented

- 🚫 Day-to-day PR reviews (covered by code review guidelines)
- 🚫 Deployment procedures (in progress)
- 🚫 Production monitoring (future docs)
- 🚫 Security hardening (in progress for v0.9)
- 🚫 Performance tuning (future optimization)

---

## 📝 Documentation Maintenance

### Update When
- Major architectural changes
- New agents or providers added
- API endpoints added/modified
- Known issues discovered
- Significant design decisions made

### Who Maintains
- Developers implementing features
- Tech lead/architect for major updates
- Entire team via code reviews

### How to Update
1. Locate relevant document
2. Make changes
3. Update README.md if new sections added
4. Commit with message: `docs: update [section] in context pack`

---

## ✅ Completeness Checklist

This context pack is complete when:
- [x] Project overview documented
- [x] Architecture documented
- [x] API endpoints documented
- [x] Data models documented
- [x] Runtime flow explained
- [x] Debugging guide provided
- [x] Development guidelines provided
- [x] Known issues listed
- [x] File dependencies mapped
- [x] Implementation status clear
- [x] Setup instructions complete
- [x] Roadmap documented

---

## 📞 Questions?

- **Architecture questions?** → See PROJECT_OVERVIEW.md and AI_ARCHITECTURE.md
- **How do I implement X?** → See DEVELOPMENT_GUIDE.md
- **What's not working?** → See DEBUGGING_GUIDE.md
- **Is this feature done?** → See IMPLEMENTATION_STATUS.md
- **What's the API contract?** → See API_REFERENCE.md
- **How does data flow?** → See RUNTIME_FLOW.md

---

## 📦 Generated

This architecture context pack was generated as part of v0.7.1 completion to enable sustainable development and knowledge transfer across the team.

**Scope**: Complete technical architecture of HealWell v0.7.1  
**Depth**: Implementation-level detail  
**Audience**: Current and future developers  
**Lifespan**: Maintained alongside codebase  

---

## License

This documentation is part of the HealWell project. All rights reserved.
