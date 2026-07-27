# HealWell Architecture

## High-Level Architecture
HealWell follows a modular three-tier architecture: Frontend (React/TailwindCSS), Backend (FastAPI), and Automation (LangGraph workflow).

## Frontend
- **Framework**: React with TypeScript
- **Styling**: TailwindCSS
- **State Management**: React Context/Hooks
- **Pages**: Landing, Dashboard, Symptom Input, Results, History
- **Services**: API client, Speech-to-Text integration, WebRTC utilities

## Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Services**: Analysis engine, History manager, Doctor finder
- **Models**: User, Analysis, History, Doctor profiles

## Automation
- **Orchestration**: LangGraph
- **Workflow**: Multi-agent symptom analysis and risk assessment
- **Agents**: Speech processor, Symptom analyzer, Emergency detector, Specialist recommender, Doctor locator

## Database
- **Type**: PostgreSQL
- **Schema**: Users, Analyses, Medical History, Doctors, Sessions
- **ORM**: SQLAlchemy

## Data Flow
User Input → Speech-to-Text → Symptom Analysis → Risk Assessment → Specialist Matching → Doctor Finder → Report Generation → Database Storage
