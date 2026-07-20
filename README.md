# HealWell

AI-powered healthcare navigation platform built with React, FastAPI, and LangGraph.

## Project Structure

```
HealWell/
├── frontend/          # React + TypeScript + Tailwind
├── backend/           # FastAPI backend
├── docs/              # Project documentation
├── MASTER_CODE.md
└── README.md
```

---

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Framer Motion

### Backend
- FastAPI
- Pydantic

### AI (Planned)
- LangGraph
- OpenAI

### Database (Planned)
- PostgreSQL

---

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd HealWell
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Backend

```bash
cd backend

python -m venv .venv

# PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger API:

```
http://127.0.0.1:8000/docs
```

---

## Documentation

Project documentation is available in the `docs/` folder:

- PROJECT.md
- PROJECT_RULES.md
- ARCHITECTURE.md
- ROADMAP.md
- FRONTEND.md
- BACKEND.md
- API.md
- AUTOMATION.md
- PROMPTS.md

---

## Current Status

- ✅ Documentation
- ✅ Frontend Foundation
- ✅ Backend Foundation
- 🚧 AI Integration (Next)
- ⏳ LangGraph Workflow
- ⏳ Database Integration

---

## License

This project is developed as part of the IBM SkillsBuild AI Internship.