# HealWell Frontend-Backend Mapping

## Component → API Mapping

### Landing Page
- **Components**: Hero, CTA, Features, Footer
- **API Calls**: None (static page)
- **Data Flow**: No backend interaction

### Analysis Page
- **Component**: SymptomInputForm
- **API Endpoint**: POST /api/v1/analysis
- **Request Schema**: AnalysisRequest
  - symptoms: str (required)
  - user_id: str (optional)
- **Response Schema**: ApiResponse
  - data.analysis_id
  - data.risk_level
  - data.confidence
  - data.specialist
  - data.emergency
- **Workflow**: 
  1. User enters symptoms
  2. Form submits to API
  3. AnalysisService → AnalysisWorkflow
  4. LangGraph executes agents
  5. Results returned and displayed
- **State Used**: Local component state + Axios response
- **Error Handling**: Catch 400/500 errors, display to user

### Results Page
- **Component**: AnalysisResults
- **Data Source**: Previous API response (passed via navigation state or stored)
- **Display**:
  - Risk level badge (color-coded: low=green, moderate=yellow, high=red)
  - Specialist recommendation
  - Home care tips from health_report
  - Lifestyle recommendations
  - Monitoring advice
- **No Additional API Calls**: Uses cached results

### History Page
- **Component**: AnalysisHistory
- **API Endpoint**: GET /api/v1/history
- **Query Parameters**: user_id, limit
- **Response Schema**: ApiResponse with list of past analyses
- **Status**: Placeholder (mock data, no persistence)
- **Future**: Will show user's analysis history from database

### Doctor Finder (Planned)
- **Component**: DoctorFinder
- **API Endpoint**: GET /api/v1/doctors
- **Query Parameters**: latitude, longitude, specialty, radius_km
- **Response Schema**: List of doctors with distance/rating
- **Status**: Placeholder (mock data, no geolocation)
- **Integration**: Will be triggered after specialist recommendation

---

## Service Layer Architecture

### Frontend Services (TypeScript/Axios)
```
api/
├── analysisService.ts
│   └── analyzeSymptoms(symptoms, userId): Promise<AnalysisResponse>
│       └── POST /api/v1/analysis
├── historyService.ts
│   └── getUserHistory(userId, limit): Promise<HistoryResponse>
│       └── GET /api/v1/history
└── doctorService.ts
    └── findDoctors(lat, lon, specialty): Promise<DoctorsResponse>
        └── GET /api/v1/doctors

hooks/
├── useAnalysis.ts         → Manages analysis state + API calls
├── useHistory.ts          → Manages history state + API calls
└── useDoctor.ts           → Manages doctor search state + API calls
```

---

## Detailed Component Mappings

### SymptomInputForm Component
```
Component Tree:
AnalysisPage
└── SymptomInputForm
    ├── symptoms textarea input
    ├── Submit button
    └── Loading/error states

Flow:
1. User types symptoms
2. On submit:
   - Validate (required field)
   - Call analysisService.analyzeSymptoms()
   - Show loading spinner
   - Wait for response (~3-5s)
   - Redirect to results page with data
   OR
   - Show error message if failed

API Integration:
POST /api/v1/analysis
{
  "symptoms": "user input text"
}

Response Handling:
{
  "success": true,
  "data": {
    "analysis_id": "...",
    "risk_level": "moderate",
    "specialist": "General Physician",
    ...
  }
}
```

### AnalysisResults Component
```
Component Tree:
ResultsPage
├── RiskLevelBadge
│   └── Displays: risk_level, confidence percentage
├── SpecialistCard
│   └── Displays: specialist, urgency, reasoning
├── RecommendationsSection
│   ├── HomeCareList
│   ├── LifestyleList
│   └── MonitoringList
└── ActionButtons
    ├── Download PDF (future)
    ├── View History
    └── New Analysis

Data Binding:
- Risk Level: data.risk_level (color-coded styling)
- Confidence: data.confidence (percentage display)
- Specialist: data.specialist (card title)
- Recommendations: data from health_report object
```

---

## Request/Response Examples

### Analysis Request Flow
```
Frontend:
POST /api/v1/analysis
Content-Type: application/json

{
  "symptoms": "I have a persistent cough, fever of 38.5°C for 3 days, and chest pain"
}

Backend Processing:
1. AnalysisService.analyze()
2. AnalysisWorkflow.execute()
3. LangGraph state processing
4. SymptomAgent → OpenAI API → Groq
5. Extract results

Response:
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "588b1d98-3fc6-463d-99bb-235649ded7bb",
    "risk_level": "moderate",
    "confidence": 82,
    "specialist": "General Physician",
    "emergency": false
  },
  "errors": null
}

Frontend Display:
- Show risk badge "Moderate Risk"
- Display specialist: "General Physician"
- Show recommendations
```

---

## State Management

### Frontend State Flow
```
1. SymptomInputForm (local state)
   - symptoms: string
   - loading: boolean
   - error: string

2. API Call
   - Send symptoms to backend
   - Receive AnalysisResult

3. Store Result
   - Pass via navigation state OR
   - Store in context/Redux (future)
   - Store in localStorage for persistence

4. ResultsPage (display state)
   - Receive data from props/context
   - Render based on response
   - Handle error states
```

### Backend State Flow
```
HTTP Request → AnalysisService
    ↓
AnalysisInput (schema validated)
    ↓
AnalysisWorkflow
    ↓
HealthAnalysisState (shared by agents)
    ├── SymptomAgent updates symptom_analysis
    ├── RiskAgent updates risk_assessment
    ├── SpecialistAgent updates specialist_recommendation
    └── ReportAgent updates health_report
    ↓
AnalysisResult (extracted from final state)
    ↓
ApiResponse (HTTP response)
    ↓
Frontend
```

---

## Error Handling Bridge

### Frontend Error Cases
```
1. Network Error
   - Show: "Unable to connect to server"
   - Action: Retry button

2. Validation Error (400)
   - Show: Field-specific error messages
   - Action: Correct input and retry

3. Server Error (500)
   - Show: "Server error occurred"
   - Action: Retry or contact support

4. Timeout
   - Show: "Request timed out"
   - Action: Retry
```

### Backend Error Responses
```
Validation Error (400):
{
  "success": false,
  "message": "Invalid request data",
  "errors": [
    {
      "field": "symptoms",
      "message": "symptoms is required"
    }
  ]
}

Server Error (500):
{
  "success": false,
  "message": "Internal server error",
  "errors": null
}
```

---

## Future Enhancements

### v0.8 Frontend-Backend
- Authentication flow
- User profile management
- Medical history persistence
- Results history page
- Doctor appointment integration
- PDF report export

### v0.9 Enhancements
- Real-time updates (WebSocket)
- Analytics integration
- Payment processing
- Insurance verification
- Multi-language support

---

## Testing Strategy

### Frontend
- Mock API responses for component testing
- Integration tests with mock backend
- E2E tests against real backend

### Backend
- Unit tests for services
- Integration tests for workflows
- API contract testing

### Integration Testing
```
1. Send AnalysisRequest from frontend
2. Verify backend processing
3. Validate AnalysisResult response
4. Confirm frontend displays correctly
```

---

## Performance Considerations

### Frontend
- Show loading spinner during 3-5s LLM call
- Debounce input if needed
- Cache results locally
- Lazy load history

### Backend
- LLM call dominates latency (~3s)
- Agent processing negligible (<50ms)
- Database queries TBD (v0.9)
- Consider response caching

---

## Summary

Frontend-Backend mapping:
- **Analysis Flow**: Most complex, involves LLM processing
- **History Flow**: Simple data retrieval (placeholder)
- **Doctor Flow**: Simple data retrieval (placeholder)
- **Error Handling**: Standardized ApiResponse format
- **State**: Clear boundaries between frontend/backend
- **Latency**: Dominated by LLM provider (~3-5s)
