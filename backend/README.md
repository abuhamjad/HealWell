# HealWell Backend - v1.0.0

FastAPI-based REST API for HealWell health analysis platform.

Production-ready backend with LangGraph workflow orchestration and OpenAI-compatible LLM integration.

## Quick Start

### 1. Install Dependencies

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
- `LLM_API_KEY=sk-...your-key...`
- `ENVIRONMENT=development`

### 3. Run Development Server

```bash
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`

## API Documentation

**Swagger UI:** `http://localhost:8000/docs`

**ReDoc:** `http://localhost:8000/redoc`

## Active Endpoints

### POST /api/v1/analysis

Submit symptoms for health analysis.

**Request:**
```json
{
  "symptoms": "I have a headache and fever"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "analysis_id": "uuid",
    "risk_level": "moderate",
    "confidence": 0.91,
    "specialist": "General Physician",
    "emergency": false,
    "risk_assessment": { ... },
    "specialist_recommendation": { ... },
    "health_report": { ... }
  }
}
```

### GET /

API health check with version info.

### GET /health

Health status endpoint.

## Project Structure

```
backend/
├── app/
│   ├── ai/                  # Workflow, agents, LLM
│   │   ├── agents/          # Analysis agents
│   │   ├── graphs/          # LangGraph workflow
│   │   ├── models/          # Data models
│   │   ├── prompts/         # Agent prompts
│   │   ├── providers/       # LLM providers
│   │   ├── state/           # Workflow state
│   │   └── workflows/       # Orchestration
│   ├── api/
│   │   ├── routes/
│   │   │   └── analysis.py  # Analysis endpoint
│   │   └── router.py        # Route registration
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── constants.py     # Constants
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic
│   └── main.py              # FastAPI app
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
└── README.md
```

## Architecture

**Three-Tier Design:**

```
API Routes
    ↓
Services
    ↓
LangGraph Workflow
    ↓
Multi-Agent Analysis
    ↓
OpenAI-Compatible LLM
```

## Workflow Agents

1. **Symptom Analysis** - Parse and normalize symptoms
2. **Risk Assessment** - Evaluate medical risk level
3. **Specialist Recommendation** - Determine appropriate specialist
4. **Emergency Detection** - Identify emergency conditions
5. **Health Report** - Generate personalized recommendations

## Configuration

All configuration via environment variables. See [docs/ENVIRONMENT.md](../docs/ENVIRONMENT.md).

**Key Variables:**

| Variable | Description |
|----------|-------------|
| ENVIRONMENT | development/staging/production |
| DEBUG | Enable debug mode |
| LLM_API_KEY | OpenAI API key |
| LLM_MODEL | Model name (gpt-4, etc.) |
| CORS_ORIGINS | Allowed frontend origins |

## Development

### Running with Hot Reload

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Coming soon
pytest
```

### Type Checking

```bash
# Using Pydantic for validation
# Type hints on all functions
```

## Production

### Building

No build step needed. FastAPI runs on Uvicorn.

### Deployment Options

- **Render:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Railway:** Auto-detects Procfile
- **Heroku:** `web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

### Performance

For production:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

## Stateless Architecture

✅ **No Database Required**
- Each request is independent
- No session management
- No user accounts
- Infinite horizontal scalability

✅ **OpenAI-Compatible**
- Works with OpenAI, OpenRouter, Ollama
- Provider abstraction layer
- Easy provider switching

✅ **Production Ready**
- Full error handling
- Type validation
- Environment-aware config
- Structured logging

## API Response Format

All responses follow envelope structure:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

## Error Handling

| Status | Scenario |
|--------|----------|
| 200 | Success |
| 400 | Invalid request |
| 500 | Server error |

## Medical Disclaimer

HealWell provides AI-generated health information for **educational purposes only**.

It is **not** a replacement for professional medical advice. Always consult qualified healthcare professionals.

In case of emergency, contact local emergency services immediately.

## Support

- 📖 Documentation: [docs/](../docs/)
- 🐛 Issues: GitHub Issues
- 📧 Contact: See main README

## Version

**v1.0.0** - Production Ready

---

**Made with FastAPI, LangGraph, and OpenAI.**
