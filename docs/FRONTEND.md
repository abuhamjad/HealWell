# HealWell Frontend Documentation

## Planned Folder Structure
```
src/
├── components/
│   ├── Common/
│   ├── Symptom/
│   ├── Results/
│   └── History/
├── pages/
│   ├── Landing
│   ├── Dashboard
│   ├── SymptomInput
│   ├── Results
│   └── History
├── services/
│   ├── api.ts
│   ├── speechToText.ts
│   └── doctor.ts
├── types/
│   ├── analysis.ts
│   ├── user.ts
│   └── common.ts
├── hooks/
│   ├── useAnalysis.ts
│   └── useHistory.ts
└── App.tsx
```

## Pages
- **Landing**: Project introduction and call-to-action
- **Dashboard**: User home with quick access options
- **Symptom Input**: Speech-to-text symptom collection interface
- **Results**: AI analysis results and recommendations
- **History**: Previous analyses and health records

## Components
- Input components for symptom capture
- Result display components
- Navigation and layout components
- Reusable UI components (buttons, cards, modals)

## Services
- API client for backend communication
- Speech-to-text integration service
- Doctor finder service
- Local storage and session management

## Types
- Analysis type definitions
- User profile types
- API response types
- Domain-specific types
