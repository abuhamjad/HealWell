# HealWell Project Rules - v1.0.0

This document contains all permanent project decisions for HealWell v1.0.0.

If a future prompt conflicts with these rules, ask for clarification instead of changing the project.

---

## Project Goal

Develop HealWell as a stateless, production-ready AI-powered health analysis platform.

Focus: Stable, working, deployable product.

Principle: Do not over-engineer. Ship simple, working solutions.

---

## Technology Stack

**Frontend:**
- React 19
- TypeScript
- Vite
- Tailwind CSS
- Framer Motion
- Lucide React icons

**Backend:**
- FastAPI
- Python 3.11+
- Pydantic
- LangGraph

**AI/LLM:**
- OpenAI-compatible API
- Supports: OpenAI, OpenRouter, Ollama, Azure OpenAI
- Provider abstraction pattern

**Deployment:**
- Frontend: Vercel
- Backend: Render, Railway, or similar
- No database (stateless architecture)

---

## Architecture Rules

### Stateless Design

- No database persistence
- No user authentication
- No session management
- Each request is independent
- Infinite horizontal scalability

### Single Responsibility

- One endpoint: `POST /api/v1/analysis`
- One workflow: health analysis
- One service: analysis service
- One hook: useAnalysis

### Type Safety

- Full TypeScript frontend
- Pydantic validation backend
- Strict type contracts
- No runtime type errors

---

## Frontend Rules

### UI/Design

Maintain production premium SaaS appearance:

- ✅ Keep glassmorphism design
- ✅ Keep dark theme
- ✅ Keep blue accent colors
- ✅ Keep typography system
- ✅ Keep Framer Motion animations
- ❌ Do NOT redesign unless explicitly requested

### Pages

**Active pages:**
- Home (`/`) - Landing page with CTA
- Analysis (`/analysis`) - Symptom analysis interface

**Removed pages:**
- ❌ History (removed in v0.9)
- ❌ Profile (removed in v0.9)
- ❌ Authentication (removed in v0.9)

### Components

Keep reusable, minimal abstractions:

- Navbar - Navigation
- RiskBadge - Risk display
- Footer - Footer section
- Sections - Page sections (Hero, HowItWorks, etc.)

**Component Rules:**
- Keep components focused
- Avoid over-splitting
- Avoid unnecessary abstraction
- Three similar components → consider extracting one
- Two similar components → probably not worth extracting

### Styling

- Tailwind CSS utility-first
- No CSS files (use Tailwind classes)
- Dark mode default
- Mobile-first responsive

### Services

Single service:
- `analysisService` - API communication for analysis

No services for:
- ❌ Doctor finder (removed)
- ❌ History (removed)
- ❌ Authentication (removed)

### Hooks

Single hook:
- `useAnalysis` - Analysis state management

No hooks for:
- ❌ `useDoctors` (removed)
- ❌ `useHistory` (removed)
- ❌ `useAuth` (removed)

---

## Backend Rules

### API Contract

Single endpoint:
```
POST /api/v1/analysis
```

Health endpoints:
```
GET /
GET /health
```

No endpoints for:
- ❌ History (removed)
- ❌ Doctors (removed)
- ❌ Authentication (removed)

### Workflow

LangGraph agents (sequential):

1. Symptom Analysis Agent
2. Risk Assessment Agent
3. Specialist Recommendation Agent
4. Emergency Detection Agent
5. Health Report Agent

Each agent:
- Receives HealthAnalysisState
- Updates one field
- Returns updated state
- Makes one LLM call

### Services

Single service:
- `AnalysisService` - Orchestrates workflow

No services for:
- ❌ `HistoryService` (removed)
- ❌ `DoctorService` (removed)
- ❌ `AuthService` (removed)

### LLM Provider

Provider pattern:

```python
class BaseProvider(ABC):
    async def call_llm(prompt: str) -> str
    async def structured_call(prompt: str, schema: dict) -> dict
```

Active providers:
- OpenAIProvider (default)

Removed providers:
- ❌ GeminiProvider (removed in v0.7+)

### Configuration

Environment-based:

```python
# Development
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=localhost

# Staging
ENVIRONMENT=staging
DEBUG=True
CORS_ORIGINS=staging-domain

# Production
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=production-domain
```

No hardcoded secrets. All config via environment variables.

### Error Handling

Structured responses:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

Status codes:
- 200: Success
- 400: Bad request
- 500: Server error

---

## Project Structure

### Frontend

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── endpoints.ts
│   │   └── types.ts
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   ├── sections/
│   ├── services/
│   ├── types/
│   ├── config/
│   └── App.tsx
├── public/
├── package.json
└── vite.config.ts
```

### Backend

```
backend/
├── app/
│   ├── ai/
│   │   ├── agents/
│   │   ├── graphs/
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── providers/
│   │   ├── state/
│   │   └── workflows/
│   ├── api/
│   │   ├── routes/
│   │   └── router.py
│   ├── core/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── requirements.txt
└── .env.example
```

---

## Development Rules

### Milestones

Roadmap is locked at v1.0.0 release.

Do not renumber milestones.

Future work:
- Tracked as GitHub issues
- Planned for v1.1+ (if developed)
- Not modifications to v1.0.0

### Workflow

For changes to v1.0.0:

1. Create feature branch
2. Implement change
3. Test locally
4. Create pull request
5. Request review
6. Merge when approved

Never work directly on main.

### Documentation

Update documentation after major changes:

- Architecture changes → Update docs/ARCHITECTURE.md
- API changes → Update docs/API.md
- Deployment changes → Update docs/DEPLOYMENT.md
- New features → Update relevant docs

Keep docs in sync with code.

### Dependencies

**Frontend:**
- Add to `package.json`
- Run `npm install`
- Commit `package-lock.json`

**Backend:**
- Add to `requirements.txt`
- Run `pip install -r requirements.txt`
- Update `.venv`
- Commit `requirements.txt` only

Avoid unnecessary dependencies.

Prefer simple solutions over complex libraries.

---

## Git Rules

### Branches

Never work directly on `main`.

Use branch naming:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `chore/description` - Maintenance

### Commits

Write clear commit messages:

```
Type: Short description

Optional longer explanation
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code reorganization
- chore: Maintenance

Never commit:
- `backend/.venv`
- `frontend/node_modules`
- `.env` files
- API keys or secrets
- Large binary files

### Pull Requests

1. Create PR with description
2. Link related issues
3. Request review
4. Address review comments
5. Merge when approved

Squash commits before merging if needed.

---

## Performance Rules

### Frontend

- Bundle size target: < 200 KB gzipped
- Lighthouse score: > 90
- Interaction to Next Paint: < 100ms
- Cumulative Layout Shift: < 0.1

### Backend

- API response time: < 10 seconds
- LLM timeout: 30 seconds max
- No N+1 queries (no database)
- Stateless design enables scaling

### General

- Ship first, optimize later
- Measure before optimizing
- Prefer simple over clever
- Avoid premature optimization

---

## Code Quality Rules

### TypeScript

- Strict mode enabled
- No `any` types
- Type all function parameters
- Type all component props

### Python

- Type hints on all functions
- Pydantic for validation
- Docstrings for public APIs
- Follow PEP 8

### Comments

- No obvious comments ("increment i")
- Comment the WHY, not the WHAT
- Remove TODO comments before release

---

## Security Rules

### Secrets

Never commit:
- API keys
- Passwords
- Credentials
- Connection strings

Use environment variables:
- `LLM_API_KEY` via Render/Vercel secrets
- Database credentials (if added later)
- Any sensitive configuration

### CORS

**Development:** Permissive (localhost, LAN)

**Production:** Strict (production domain only)

No wildcards in production.

### Dependencies

Keep dependencies updated:
- `npm audit` regularly
- `pip audit` regularly
- Remove unused packages

---

## Medical & Ethical Rules

### Disclaimer

Always include:

> HealWell provides AI-generated health information for educational purposes only. It is not a replacement for professional medical advice. Always consult qualified healthcare professionals.

### Responsibility

- Do not present as medical diagnosis
- Recommend professional consultation
- Detect and alert on emergencies
- Provide evidence-based information

---

## Future Considerations

### Possible v1.1+ Features

- Multi-language support
- Additional LLM providers
- Offline mode
- Mobile app (React Native)
- Advanced medical context
- Integration with health apps

### Do Not Add to v1.0.0

- Database persistence
- User authentication
- Analysis history
- Doctor finder
- Subscription model

These were removed for simplicity and stateless design.

---

## Documentation Standards

All documentation files:
- Use Markdown
- Clear headings
- Code examples where applicable
- Links to related docs
- Accurate to current version

Keep docs in:
- `docs/` - Project documentation
- `README.md` - Quick start
- `backend/README.md` - Backend setup
- `frontend/README.md` - Frontend setup

---

## Support & Questions

If implementation conflicts with these rules:

1. Ask for clarification in a comment/issue
2. Do not assume or guess
3. Reference the relevant rule
4. Wait for direction

These rules exist to keep the project focused and maintainable.

---

**HealWell v1.0.0 Project Rules**

Last Updated: July 27, 2026

Status: Production Release
