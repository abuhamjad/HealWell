# HealWell Project Rules

This document contains all permanent project decisions.

If a future prompt conflicts with these rules, ask for clarification instead of changing the project.

---

# Project Goal

Develop HealWell as an AI-powered healthcare navigation platform aligned with SDG 3.

The priority is completing a stable, working project.

Do not over-engineer.

---

# Tech Stack

Frontend
- React
- TypeScript
- Tailwind CSS
- Framer Motion

Backend
- FastAPI

Automation
- LangGraph

Database
- PostgreSQL

Deployment
- Vercel
- Render

---

# UI Rules

Maintain the current premium SaaS appearance.

Do not redesign UI unless explicitly instructed.

Keep:

- Glassmorphism
- Dark theme
- Blue accent color
- Typography
- Animations

---

# Homepage Structure

The homepage consists of:

1. Hero
2. Problem Statement
3. How It Works
4. Automation
5. Begin Health Analysis
6. Footer

Remove permanently:

- Features section
- Technology section
- Agent information cards

---

# How It Works

Use a vertical timeline.

Eight steps:

1. Describe Symptoms
2. Speech-to-Text
3. Symptom Analysis
4. Medical History
5. Risk Assessment
6. Specialist Recommendation
7. Nearby Doctors
8. Health Report

---

# Automation

Keep LangGraph workflow.

Use SVG/Lucide icons.

Do not use emojis.

Do not recreate the workflow layout unless requested.

---

# Analyze Page

Keep existing UI.

No redesign.

---

# History Page

Keep existing UI.

No redesign.

---

# Component Rules

Keep components reusable.

Do not over-split.

Avoid unnecessary abstraction.

---

# Folder Rules

Frontend

src/
pages/
sections/
components/
services/
types/
utils/

Backend

backend/
app/
api/
services/
models/
schemas/
core/

---

# Development Rules

Finish one milestone.

Stop.

Wait for review.

Never continue automatically.

---

# Documentation Rules

Update documentation only after major milestones.

Major milestones:

v0.1

v0.2

v0.3

v0.4

v0.5

---

# Git Rules

Never work directly on main.

Use release branches.

Commit after every approved milestone.

---

# Performance Rules

Prefer simple solutions.

Avoid unnecessary dependencies.

Avoid unnecessary files.

Ship first.

Optimize later.

# Development Environment

## Frontend

Always execute frontend commands from:

frontend/

Examples:

cd frontend
npm install
npm run dev
npm run build

---

## Backend

Always execute backend commands from:

backend/

Examples:

cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

---

## Python Environment

Always use the project's virtual environment.

Do not install Python packages globally.

All backend dependencies must be installed inside:

backend/.venv

---

## Dependency Management

Frontend dependencies:
- package.json

Backend dependencies:
- requirements.txt

Update dependency files whenever a new package is added.

---

## Git

Never commit:

- backend/.venv
- frontend/node_modules
- .env

Ensure they remain in .gitignore.

# Roadmap Rules

The project roadmap is locked.

Milestones must not be renumbered.

If additional work is discovered during development:

- Add it as a task within the current milestone.
- Do not create unnecessary sub-versions.
- Do not move completed work into future milestones.