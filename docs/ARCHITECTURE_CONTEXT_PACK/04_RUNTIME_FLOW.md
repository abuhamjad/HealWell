# HealWell Runtime Flow

## Request Lifecycle: Symptom Analysis

### Complete Sequence Diagram

```
User (Frontend)
    │
    │ 1. User enters symptom text and clicks "Analyze"
    │
    ▼
React Component (AnalysisPage)
    │
    │ 2. Form validation
    │
    ▼
Axios HTTP Client
    │
    │ 3. POST /api/v1/analysis
    │    {
    │      "symptoms": "I have a persistent cough, fever of 38.5°C, chest pain..."
    │    }
    │
    ▼
FastAPI Application (main.py)
    │
    │ 4. Route matching
    │    - Match: POST /api/v1/analysis
    │    - Router: api_router
    │    - Route handler: analysis.create_analysis()
    │
    ▼
CORS Middleware
    │
    │ 5. Validate CORS headers
    │    - Check Origin header
    │    - Allow if in CORS_ORIGINS or matches regex
    │
    ▼
Pydantic Validation
    │
    │ 6. Validate AnalysisRequest schema
    │    {
    │      "symptoms": str (required),
    │      "user_id": str (optional)
    │    }
    │
    ▼
Route Handler (api/routes/analysis.py)
    │
    │ 7. create_analysis(request: AnalysisRequest)
    │    - Extract: symptoms, user_id
    │
    ▼
AnalysisService (services/analysis_service.py)
    │
    │ 8. analyze(symptoms, user_id)
    │    - Create AnalysisInput
    │    - Call workflow.execute()
    │
    ▼
AnalysisWorkflow (ai/workflows/analysis_workflow.py)
    │
    │ 9. execute(input_data: AnalysisInput)
    │    - Generate session_id (UUID)
    │    - Create initial HealthAnalysisState
    │    - Invoke compiled LangGraph
    │
    ▼
LangGraph Compiled Graph (ai/graphs/langgraph_builder.py)
    │
    ├──────────────────────────────────────────┐
    │  LangGraph State Execution                │
    │                                           │
    │  10a. symptom_node (Async)               │
    │       ┌─────────────────────────────┐   │
    │       │ SymptomAgent.execute()      │   │
    │       │ (REAL - v0.7.1)             │   │
    │       │                             │   │
    │       │ Input State:                │   │
    │       │  - user_input               │   │
    │       │  - analysis_input           │   │
    │       │  - metadata                 │   │
    │       │                             │   │
    │       │ 1. Extract analysis_input  │   │
    │       │ 2. Create provider         │   │
    │       │ 3. Initialize provider     │   │
    │       │    - AsyncOpenAI(          │   │
    │       │      api_key=...,          │   │
    │       │      base_url=groq,        │   │
    │       │      timeout=30            │   │
    │       │    )                        │   │
    │       │ 4. Call analyze_          │   │
    │       │    symptoms_structured()   │   │
    │       │                             │   │
    │       │ ▼                           │   │
    │       │ OpenAIProvider             │   │
    │       │ .analyze_symptoms_        │   │
    │       │  structured()              │   │
    │       │                             │   │
    │       │ 1. Generate prompt        │   │
    │       │    using get_symptom_     │   │
    │       │    analysis_prompt()      │   │
    │       │                             │   │
    │       │ 2. Create API request:    │   │
    │       │    POST https://api.groq  │   │
    │       │    .com/openai/v1/chat/   │   │
    │       │    completions            │   │
    │       │    {                       │   │
    │       │      "model": "openai/    │   │
    │       │               gpt-oss-120b",│   │
    │       │      "messages": [{        │   │
    │       │        "role": "system",  │   │
    │       │        "content": "You   │   │
    │       │                  are a   │   │
    │       │                  medical │   │
    │       │                  analysis │   │
    │       │                  assistant"│   │
    │       │      }, {                 │   │
    │       │        "role": "user",   │   │
    │       │        "content": "[full │   │
    │       │                    prompt]"│   │
    │       │      }],                  │   │
    │       │      "temperature": 0.7, │   │
    │       │      "max_tokens": 1000  │   │
    │       │    }                       │   │
    │       │                             │   │
    │       │ 3. Wait for LLM response │   │
    │       │    (HTTP timeout: 30s)    │   │
    │       │                             │   │
    │       │ 4. Parse JSON response:   │   │
    │       │    {                       │   │
    │       │      "detected_symptoms": │   │
    │       │        ["persistent cough",│   │
    │       │         "fever",           │   │
    │       │         "chest pain"],    │   │
    │       │      "confidence": 92.0,  │   │
    │       │      "summary": "The     │   │
    │       │               patient... ",│   │
    │       │      "severity_indicators":│   │
    │       │        ["fever 38.5°C"],  │   │
    │       │      "affected_systems":  │   │
    │       │        ["respiratory"]    │   │
    │       │    }                       │   │
    │       │                             │   │
    │       │ 5. Validate with        │   │
    │       │    SymptomAnalysis      │   │
    │       │    Pydantic model       │   │
    │       │                             │   │
    │       │ Output State:               │   │
    │       │  - symptom_analysis (dict) │   │
    │       │  - current_step: "symptom_ │   │
    │       │    analysis"                │   │
    │       │  - workflow_status:        │   │
    │       │    "symptom_analysis_     │   │
    │       │     complete"               │   │
    │       └─────────────────────────────┘   │
    │                                           │
    │  Edge: symptom_agent → risk_agent        │
    │                                           │
    │  10b. risk_node (Async)                  │
    │       ┌─────────────────────────────┐   │
    │       │ RiskAgent.execute()         │   │
    │       │ (MOCK)                      │   │
    │       │                             │   │
    │       │ Input State:                │   │
    │       │  - symptom_analysis         │   │
    │       │                             │   │
    │       │ 1. Read symptom_analysis   │   │
    │       │ 2. Assess risk based on   │   │
    │       │    symptoms                │   │
    │       │ 3. Generate RiskAssessment │   │
    │       │                             │   │
    │       │ Output State:               │   │
    │       │  - risk_assessment          │   │
    │       │  - current_step: "risk_    │   │
    │       │    assessment"              │   │
    │       └─────────────────────────────┘   │
    │                                           │
    │  Edge: risk_agent → specialist_agent    │
    │                                           │
    │  10c. specialist_node (Async)            │
    │       ┌─────────────────────────────┐   │
    │       │ SpecialistAgent.execute()   │   │
    │       │ (MOCK)                      │   │
    │       │                             │   │
    │       │ Input State:                │   │
    │       │  - risk_assessment          │   │
    │       │                             │   │
    │       │ 1. Read risk_assessment    │   │
    │       │ 2. Recommend specialist    │   │
    │       │ 3. Generate Specialist     │   │
    │       │    Recommendation          │   │
    │       │                             │   │
    │       │ Output State:               │   │
    │       │  - specialist_recommendation│   │
    │       │  - current_step: "specialist│   │
    │       │    _recommendation"         │   │
    │       └─────────────────────────────┘   │
    │                                           │
    │  Edge: specialist_agent → report_agent   │
    │                                           │
    │  10d. report_node (Async)                │
    │       ┌─────────────────────────────┐   │
    │       │ ReportAgent.execute()       │   │
    │       │ (MOCK)                      │   │
    │       │                             │   │
    │       │ Input State:                │   │
    │       │  - All previous results     │   │
    │       │                             │   │
    │       │ 1. Read all previous      │   │
    │       │    analysis results        │   │
    │       │ 2. Generate health report  │   │
    │       │ 3. Generate HealthReport   │   │
    │       │                             │   │
    │       │ Output State:               │   │
    │       │  - health_report            │   │
    │       │  - current_step: "health_  │   │
    │       │    report"                  │   │
    │       └─────────────────────────────┘   │
    │                                           │
    │  Finish: report_agent (workflow complete)│
    │                                           │
    └──────────────────────────────────────────┘
    │
    │ 11. LangGraph returns final state
    │
    ▼
AnalysisWorkflow
    │
    │ 12. Extract AnalysisResult from final state:
    │     {
    │       "analysis_id": "session_id",
    │       "risk_assessment": {...},
    │       "specialist_recommendation": {...},
    │       "health_report": {...},
    │       "emergency_alert": false
    │     }
    │
    ▼
AnalysisService
    │
    │ 13. Return AnalysisResult to route handler
    │
    ▼
Route Handler (api/routes/analysis.py)
    │
    │ 14. Transform AnalysisResult to API response:
    │     {
    │       "analysis_id": "...",
    │       "risk_level": "moderate",
    │       "confidence": 82,
    │       "specialist": "General Physician",
    │       "emergency": false
    │     }
    │
    ▼
ApiResponse Wrapper
    │
    │ 15. Create success response:
    │     {
    │       "success": true,
    │       "message": "Health analysis created successfully",
    │       "data": {...},
    │       "errors": null
    │     }
    │
    ▼
HTTP Response (200 OK)
    │
    │ 16. JSON serialization
    │     Content-Type: application/json
    │
    ▼
Axios HTTP Client (Frontend)
    │
    │ 17. Receive response
    │     HTTP 200 with JSON body
    │
    ▼
React Component
    │
    │ 18. Update component state
    │     - Show results
    │     - Risk level badge
    │     - Specialist recommendation
    │     - Home care recommendations
    │
    ▼
User (Frontend Display)
    │
    │ Results displayed:
    │ - Risk Level: Moderate
    │ - Specialist: General Physician
    │ - Recommendations shown
    └─ Timeline: ~3-5 seconds
```

---

## Performance Timeline

```
Component                  Time        Notes
─────────────────────────────────────────────────
Frontend validation        <10ms       Form validation
HTTP round-trip 1          ~50ms       Request to backend
Pydantic validation        <5ms        Schema validation
Service setup              <5ms        Create AnalysisInput
LangGraph initialization   <10ms       Initialize state
────────────────────────────────────────────────
SymptomAgent               ~3000ms     Dominated by LLM call
  ├─ Provider init         ~100ms
  ├─ Prompt generation     <1ms
  ├─ LLM API call          ~2800ms     Groq API latency
  ├─ JSON parsing          <5ms
  └─ Validation            <10ms
────────────────────────────────────────────────
RiskAgent                  <10ms       Simple logic (mock)
SpecialistAgent            <10ms       Simple logic (mock)
ReportAgent                <10ms       Simple logic (mock)
────────────────────────────────────────────────
Result extraction          <5ms        Convert state to AnalysisResult
Response formatting        <5ms        ApiResponse wrapper
HTTP serialization         <5ms        JSON encoding
HTTP round-trip 2          ~50ms       Response to frontend
────────────────────────────────────────────────
TOTAL                      ~3150ms     ~3.15 seconds (typical)
                           2500-5000ms Range depends on LLM latency
```

---

## Error Handling Flow

### Provider Error During LLM Call

```
SymptomAgent.execute()
    │
    ├─ try:
    │   ├─ provider.initialize()
    │   └─ provider.analyze_symptoms_structured()
    │       └─ LLM API call fails
    │           └─ Timeout / Rate limit / Server error
    │
    └─ except Exception as e:
        ├─ logger.error(f"Symptom analysis failed: {e}")
        ├─ state["errors"].append(f"Symptom analysis error: {str(e)}")
        ├─ state["current_step"] = "symptom_analysis_failed"
        └─ return state (errors don't crash workflow)

Result:
  - state["symptom_analysis"] remains empty or partial
  - state["errors"] contains error message
  - RiskAgent still executes (uses empty symptom_analysis)
  - Final response includes error information
```

### JSON Parse Error

```
OpenAIProvider.analyze_symptoms_structured()
    │
    └─ try:
        └─ response_text = response.choices[0].message.content
           └─ json.loads(response_text) fails
    
    └─ except json.JSONDecodeError:
        ├─ logger.error(f"Failed to parse: {e}")
        └─ raise ValueError(f"Invalid JSON response from LLM")

Result:
  - Exception propagates to SymptomAgent
  - SymptomAgent catches and logs
  - State includes error
  - Workflow continues
```

### Validation Error

```
SymptomAnalysis validation fails:
    
    SymptomAnalysis(
        detected_symptoms=None,  # Expected List[str]
        confidence="invalid",    # Expected float
        summary=None             # Expected str
    )
    
    └─ Pydantic ValidationError raised

Result:
  - Exception caught in SymptomAgent
  - Error added to state
  - Agent returns error state
  - Workflow continues with error
```

---

## State Progression Example

### Initial State
```python
{
    "session_id": "12345-67890",
    "user_input": "I have persistent cough and fever of 38.5°C",
    "analysis_input": AnalysisInput(...),
    "symptom_analysis": {},
    "risk_assessment": None,
    "specialist_recommendation": None,
    "health_report": None,
    "workflow_status": "started",
    "current_step": "initialization",
    "errors": [],
    "metadata": {...}
}
```

### After SymptomAgent
```python
{
    # ... previous fields ...
    "symptom_analysis": {
        "detected_symptoms": ["persistent cough", "fever"],
        "confidence": 92.0,
        "summary": "Patient presents with respiratory symptoms...",
        "severity_indicators": ["fever 38.5°C"],
        "affected_systems": ["respiratory", "immune"]
    },
    "workflow_status": "symptom_analysis_complete",
    "current_step": "symptom_analysis",
    "errors": []
}
```

### After RiskAgent
```python
{
    # ... previous fields ...
    "risk_assessment": RiskAssessment(
        risk_level="moderate",
        confidence=82.0,
        reasoning="Based on detected symptoms...",
        warning_signs=["persistent fever above 38.5°C"]
    ),
    "workflow_status": "risk_assessment_complete",
    "current_step": "risk_assessment"
}
```

### After SpecialistAgent
```python
{
    # ... previous fields ...
    "specialist_recommendation": SpecialistRecommendation(
        specialist="General Physician",
        reasoning="Moderate risk with respiratory symptoms...",
        urgency="24-48 hours"
    ),
    "workflow_status": "specialist_recommendation_complete",
    "current_step": "specialist_recommendation"
}
```

### After ReportAgent (Final)
```python
{
    # ... all previous fields ...
    "health_report": HealthReport(
        summary="Based on analysis, respiratory infection suspected...",
        home_care=["Get rest", "Stay hydrated"],
        lifestyle=["Avoid strenuous activities"],
        monitoring=["Monitor temperature"],
        references=["WHO guidelines"]
    ),
    "workflow_status": "analysis_complete",
    "current_step": "health_report"
}
```

---

## Concurrent Request Handling

```
Request 1: User A symptoms
    │
    ├─ Session 1 (unique state)
    │   ├─ SymptomAgent (LLM call)
    │   └─ Other agents...
    │
    ▼ (3 seconds)
Response 1 returned

Request 2: User B symptoms (arrives during Request 1)
    │
    ├─ Session 2 (separate state, independent)
    │   ├─ SymptomAgent (parallel LLM call)
    │   └─ Other agents...
    │
    ▼ (3 seconds)
Response 2 returned

Key Points:
- Each request has unique session_id
- States don't interfere (separate dicts)
- LLM calls can run in parallel
- FastAPI handles concurrency naturally (async/await)
- No shared state between users
```

---

## Summary

The runtime flow is:
1. **Frontend** captures symptom input
2. **API Layer** validates and routes request
3. **Service Layer** orchestrates workflow
4. **LangGraph** executes agents sequentially with shared state
5. **SymptomAgent** makes real LLM call (v0.7.1) via OpenAI provider
6. **Other Agents** process results (currently mock)
7. **Result Extraction** converts final state to API response
8. **Frontend** displays results to user

Total latency: ~3-5 seconds (dominated by LLM API call)

The architecture supports:
- Concurrent requests from multiple users
- Graceful error handling at each layer
- Clear data flow through shared state
- Easy debugging (session_id traces entire request)
