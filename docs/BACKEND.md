# HealWell Backend Documentation

## Planned Folder Structure
```
backend/
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── user.py
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── doctor.py
│   ├── schemas/
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── user.py
│   ├── services/
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── doctor.py
│   ├── routes/
│   │   ├── analysis.py
│   │   ├── history.py
│   │   └── doctor.py
│   ├── database/
│   │   ├── db.py
│   │   └── session.py
│   └── utils/
│       ├── auth.py
│       └── validators.py
├── requirements.txt
├── .env.example
└── config.py
```

## FastAPI Layout
- Application factory pattern in `main.py`
- Route handlers organized by domain
- Middleware for authentication and error handling
- CORS configuration for frontend integration

## Services
- Analysis service for symptom processing
- History service for data retrieval and storage
- Doctor finder service for location-based search

## Models
- User: User accounts and profiles
- Analysis: Individual analysis records
- History: Patient medical history
- Doctor: Healthcare provider profiles

## Database Integration
- SQLAlchemy ORM for PostgreSQL
- Alembic for schema migrations
- Connection pooling for performance
