# HealWell Backend Documentation

## Status
✅ **Milestone v0.3 Completed** - FastAPI backend foundation established.

## Implemented Folder Structure
```
backend/
├── app/
│   ├── main.py
│   ├── __init__.py
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
│   │   └── config.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── doctor.py
│   └── services/
│       └── __init__.py
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

## Not Yet Implemented

- Database integration (PostgreSQL)
- SQLAlchemy ORM models
- Authentication and authorization
- AI and LangGraph workflow integration
- Business logic and actual processing
- Alembic schema migrations
- Advanced error handling

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
