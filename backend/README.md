# HealWell Backend

FastAPI-based backend for HealWell health analysis platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Analysis
- `POST /api/v1/analysis` - Create a new health analysis

### History
- `GET /api/v1/history` - Get user analysis history
- `POST /api/v1/history` - Save medical history

### Doctors
- `GET /api/v1/doctors` - Find nearby healthcare providers

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── analysis.py
│   │   │   ├── history.py
│   │   │   └── doctors.py
│   │   └── router.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── doctor.py
│   ├── services/
│   └── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Notes

- Placeholder endpoints return mock data
- No database connection implemented
- No authentication implemented
- No business logic implemented
- CORS configured for frontend at `http://localhost:5173`
