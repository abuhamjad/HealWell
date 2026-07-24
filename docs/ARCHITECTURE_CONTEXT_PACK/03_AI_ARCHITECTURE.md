# HealWell AI Architecture

## Overview

The AI layer orchestrates multi-step medical reasoning using LangGraph, with agent-based processing powered by LLM providers (OpenAI-compatible, Gemini, etc.). Each agent specializes in a specific medical analysis task.

---

## LangGraph Workflow

### What is LangGraph?

LangGraph is a framework for building stateful, multi-step agentic workflows. It provides:
- **StateGraph**: Defines nodes (agents) and edges (transitions)
- **TypedDict State**: Shared mutable state passed between nodes
- **Async Execution**: Non-blocking workflow orchestration
- **Clear Data Flow**: Explicit state transformations

### Why LangGraph for HealWell?

1. **Sequential Reasoning**: Medical analysis requires ordered steps
2. **Shared State**: All agents need access to previous results
3. **Clear Data Flow**: Easy to trace data transformations
4. **Extensible**: Simple to add new agents

### LangGraph in HealWell

```
Health Analysis Graph
├── Entrypoint: symptom_agent
├── Node 1: symptom_node → SymptomAgent
│   ├── Input: HealthAnalysisState (with user_input)
│   └── Output: HealthAnalysisState (with symptom_analysis)
├── Edge: symptom_agent → risk_agent
├── Node 2: risk_node → RiskAgent
│   ├── Input: HealthAnalysisState (with symptom_analysis)
│   └── Output: HealthAnalysisState (with risk_assessment)
├── Edge: risk_agent → specialist_agent
├── Node 3: specialist_node → SpecialistAgent
│   ├── Input: HealthAnalysisState (with risk_assessment)
│   └── Output: HealthAnalysisState (with specialist_recommendation)
├── Edge: specialist_agent → report_agent
├── Node 4: report_node → ReportAgent
│   ├── Input: HealthAnalysisState (with specialist_recommendation)
│   └── Output: HealthAnalysisState (with health_report)
└── Finish: report_agent
```

---

## Workflow State

### HealthAnalysisState (TypedDict)

```python
class HealthAnalysisState(TypedDict, total=False):
    """Shared workflow state for all agents"""
    
    # Identifiers
    session_id: str                          # Unique workflow session ID
    
    # Input Data
    user_input: str                          # Raw symptom description from user
    analysis_input: AnalysisInput           # Structured input data
    
    # Analysis Results (updated by agents)
    symptom_analysis: dict[str, Any]        # Updated by SymptomAgent (REAL v0.7.1)
    risk_assessment: RiskAssessment         # Updated by RiskAgent (mock)
    specialist_recommendation: SpecialistRecommendation  # Updated by SpecialistAgent (mock)
    doctor_recommendations: List[dict]      # Future: Updated by DoctorAgent
    health_report: HealthReport             # Updated by ReportAgent (mock)
    
    # Workflow Control
    workflow_status: str                     # "started", "symptom_analysis_complete", etc.
    current_step: str                        # Last executed agent name
    errors: List[str]                       # Accumulated errors
    
    # Metadata
    metadata: dict[str, Any]                # User metadata (medical history, medications, allergies)
```

### State Flow Diagram

```
Initial State (from AnalysisInput)
├── session_id: "uuid-123"
├── user_input: "I have a persistent cough..."
├── analysis_input: AnalysisInput(...)
├── symptom_analysis: {}
├── risk_assessment: None
├── specialist_recommendation: None
├── health_report: None
├── workflow_status: "started"
├── current_step: "initialization"
├── errors: []
└── metadata: {user_id, medical_history, medications, allergies}

    ↓ (SymptomAgent processes)

After SymptomAgent (REAL)
├── symptom_analysis: {
│   "detected_symptoms": ["persistent cough", "fever", "chest pain"],
│   "confidence": 92.0,
│   "summary": "Patient presents with respiratory infection symptoms...",
│   "severity_indicators": ["fever", "chest pain"],
│   "affected_systems": ["respiratory", "cardiovascular"]
│ }
├── workflow_status: "symptom_analysis_complete"
├── current_step: "symptom_analysis"
└── errors: []

    ↓ (RiskAgent processes)

After RiskAgent (MOCK)
├── risk_assessment: RiskAssessment(
│   risk_level="moderate",
│   confidence=82.0,
│   reasoning="Based on detected symptoms: fever and cough...",
│   warning_signs=["persistent high fever", "chest pain"]
│ )
├── workflow_status: "risk_assessment_complete"
└── current_step: "risk_assessment"

    ↓ (SpecialistAgent processes)

After SpecialistAgent (MOCK)
├── specialist_recommendation: SpecialistRecommendation(
│   specialist="General Physician",
│   reasoning="Moderate risk level with respiratory symptoms...",
│   urgency="24-48 hours"
│ )
├── workflow_status: "specialist_recommendation_complete"
└── current_step: "specialist_recommendation"

    ↓ (ReportAgent processes)

After ReportAgent (MOCK)
├── health_report: HealthReport(
│   summary="Based on symptom analysis and risk assessment...",
│   home_care=["Get plenty of rest", "Stay hydrated"],
│   lifestyle=["Avoid strenuous activities"],
│   monitoring=["Monitor temperature daily"],
│   references=["WHO guidelines"]
│ )
├── workflow_status: "analysis_complete"
└── current_step: "health_report"

Final State (returned to API)
→ AnalysisResult extracted from final state
```

---

## Provider Abstraction

### BaseProvider Interface

```python
class BaseProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.is_initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider (e.g., create SDK client)"""
        pass
    
    @abstractmethod
    async def analyze_symptoms(
        self, 
        input_data: AnalysisInput
    ) -> AnalysisResult:
        """Analyze symptoms and return complete analysis result"""
        pass
    
    @abstractmethod
    async def generate_report(
        self,
        analysis_result: AnalysisResult
    ) -> Dict[str, Any]:
        """Generate detailed health report"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if provider is healthy and accessible"""
        pass
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
```

**Benefits**:
- Multiple providers supported (OpenAI, Gemini, Groq, future providers)
- No provider-specific logic in agents
- Easy to switch providers via configuration
- Testable with mock providers

### OpenAIProvider Implementation

```python
class OpenAIProvider(BaseProvider):
    """OpenAI-compatible provider (Groq, OpenAI, etc.)"""
    
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None,
        timeout: int = None
    ):
        super().__init__(api_key)
        self.base_url = base_url or settings.LLM_BASE_URL
        self.model = model or settings.LLM_MODEL
        self.timeout = timeout or settings.LLM_TIMEOUT
        self.client = None
    
    async def initialize(self) -> None:
        """Create AsyncOpenAI client"""
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self.is_initialized = True
    
    async def analyze_symptoms_structured(
        self,
        input_data: AnalysisInput
    ) -> SymptomAnalysis:
        """
        Real LLM call for symptom analysis (v0.7.1)
        
        1. Generate prompt with medical context
        2. Call LLM API
        3. Parse JSON response
        4. Validate and return SymptomAnalysis
        """
        prompt = get_symptom_analysis_prompt(
            symptoms=input_data.symptoms,
            medical_history=input_data.medical_history,
            medications=input_data.medications,
            allergies=input_data.allergies,
        )
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a medical analysis assistant..."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        response_text = response.choices[0].message.content.strip()
        symptom_data = json.loads(response_text)
        
        return SymptomAnalysis(
            detected_symptoms=symptom_data.get("detected_symptoms", []),
            confidence=float(symptom_data.get("confidence", 75)),
            summary=symptom_data.get("summary", ""),
            severity_indicators=symptom_data.get("severity_indicators", []),
            affected_systems=symptom_data.get("affected_systems", []),
        )
```

**Key Features (v0.7.1)**:
- Real async LLM calls
- JSON response parsing
- Pydantic validation
- Error handling
- Configurable via environment

### GeminiProvider (Placeholder)

```python
class GeminiProvider(BaseProvider):
    """Google Gemini provider (placeholder)"""
    
    async def initialize(self) -> None:
        # TODO: Initialize Gemini SDK
        pass
    
    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        # TODO: Implement Gemini API calls
        pass
```

### Provider Factory

```python
def create_provider() -> BaseProvider:
    """Factory for provider instantiation"""
    provider_name = settings.LLM_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            timeout=settings.LLM_TIMEOUT,
        )
    elif provider_name == "gemini":
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
```

---

## Agents

### BaseAgent Interface

```python
class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Execute agent logic
        
        Args:
            state: HealthAnalysisState
        
        Returns:
            Updated HealthAnalysisState
        """
        pass
```

### SymptomAgent (REAL - v0.7.1)

```python
class SymptomAgent(BaseAgent):
    """Analyzes symptoms using real LLM provider"""
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        1. Extract AnalysisInput from state
        2. Initialize provider
        3. Call analyze_symptoms_structured()
        4. Update state with results
        5. Handle errors gracefully
        """
        try:
            analysis_input = state.get("analysis_input")
            
            provider = create_provider()
            await provider.initialize()
            
            symptom_result = await provider.analyze_symptoms_structured(analysis_input)
            
            state["symptom_analysis"] = symptom_result.model_dump()
            state["current_step"] = "symptom_analysis"
            state["workflow_status"] = "symptom_analysis_complete"
            
        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}")
            state["errors"].append(f"Symptom analysis error: {str(e)}")
            state["current_step"] = "symptom_analysis_failed"
        
        return state
```

**Status**: Real LLM calls via Groq API (implemented in v0.7.1)

### RiskAgent (MOCK)

```python
class RiskAgent(BaseAgent):
    """Assesses health risk level"""
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        1. Read symptom_analysis from state
        2. Assess risk based on symptoms
        3. Update state with RiskAssessment
        """
        state["risk_assessment"] = RiskAssessment(
            risk_level="moderate",
            confidence=0.82,
            reasoning="Based on detected symptoms: fever and cough...",
            warning_signs=["persistent high fever above 38.5°C"],
        )
        state["current_step"] = "risk_assessment"
        return state
```

**Status**: Mock implementation (will be replaced by real LLM in v0.7.2)

### SpecialistAgent (MOCK)

```python
class SpecialistAgent(BaseAgent):
    """Recommends appropriate specialist"""
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        1. Read risk_assessment from state
        2. Determine specialist based on risk
        3. Update state with recommendation
        """
        state["specialist_recommendation"] = SpecialistRecommendation(
            specialist="General Physician",
            reasoning="Moderate risk level with respiratory symptoms...",
            urgency="24-48 hours",
        )
        state["current_step"] = "specialist_recommendation"
        return state
```

**Status**: Mock implementation (will be replaced by real LLM in v0.7.3)

### ReportAgent (MOCK)

```python
class ReportAgent(BaseAgent):
    """Generates health report"""
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        1. Read all previous analysis results
        2. Generate comprehensive report
        3. Update state with HealthReport
        """
        state["health_report"] = HealthReport(
            summary="Based on symptom analysis and risk assessment...",
            home_care=["Get plenty of rest", "Stay hydrated"],
            lifestyle=["Avoid strenuous activities"],
            monitoring=["Monitor temperature daily"],
            references=["WHO guidelines"],
        )
        state["current_step"] = "health_report"
        return state
```

**Status**: Mock implementation (will be replaced by real LLM in v0.7.4)

---

## Prompts

### SymptomAnalysisPrompt (REAL - v0.7.1)

```python
def get_symptom_analysis_prompt(
    symptoms: str,
    medical_history: str = None,
    medications: list = None,
    allergies: list = None
) -> str:
    """
    Generate prompt for LLM symptom analysis
    
    Instructs LLM to:
    1. Identify specific symptoms
    2. Assess severity
    3. Identify affected body systems
    4. Provide confidence score
    5. Return structured JSON
    """
    
    prompt = f"""Analyze the following health symptoms:
    
PATIENT SYMPTOMS:
{symptoms}

"""
    
    if medical_history:
        prompt += f"MEDICAL HISTORY:\n{medical_history}\n\n"
    
    if medications:
        prompt += f"CURRENT MEDICATIONS:\n- " + "\n- ".join(medications) + "\n\n"
    
    if allergies:
        prompt += f"KNOWN ALLERGIES:\n- " + "\n- ".join(allergies) + "\n\n"
    
    prompt += """RESPONSE FORMAT (RETURN ONLY VALID JSON):
{
  "detected_symptoms": ["symptom1", "symptom2"],
  "confidence": 85,
  "summary": "Clinical summary",
  "severity_indicators": ["high fever"],
  "affected_systems": ["respiratory", "immune"]
}"""
    
    return prompt
```

**Output Format**:
```json
{
  "detected_symptoms": ["persistent cough", "fever", "chest pain", "difficulty breathing"],
  "confidence": 92.0,
  "summary": "The patient presents with acute respiratory infection symptoms...",
  "severity_indicators": ["fever 38.5°C", "chest pain", "difficulty breathing"],
  "affected_systems": ["respiratory", "cardiovascular", "immune"]
}
```

### RiskAssessmentPrompt (PLACEHOLDER)

```python
def get_risk_assessment_prompt(symptom_analysis: dict) -> str:
    """Generate prompt for risk assessment"""
    # TODO: Implement real prompt
    pass
```

### SpecialistPrompt (PLACEHOLDER)

```python
def get_specialist_recommendation_prompt(risk_assessment: dict) -> str:
    """Generate prompt for specialist recommendation"""
    # TODO: Implement real prompt
    pass
```

### ReportPrompt (PLACEHOLDER)

```python
def get_report_generation_prompt(analysis_result: dict) -> str:
    """Generate prompt for report generation"""
    # TODO: Implement real prompt
    pass
```

---

## Execution Lifecycle

### Step 1: User Input

```
Frontend: User enters symptoms
          "I have persistent cough, fever, and chest pain"
          
API: POST /api/v1/analysis
     {
       "symptoms": "I have persistent cough, fever, and chest pain"
     }
```

### Step 2: Service Initialization

```
AnalysisService.analyze(symptoms)
    └─ Create AnalysisInput
       {
         "symptoms": "I have persistent cough, fever, and chest pain",
         "user_id": None,
         "medical_history": None,
         "medications": None,
         "allergies": None
       }
```

### Step 3: Workflow Execution

```
AnalysisWorkflow.execute(input_data)
    └─ Create HealthAnalysisState
       {
         "session_id": "abc123",
         "user_input": "I have persistent cough...",
         "analysis_input": {...},
         "workflow_status": "started",
         ...
       }
    └─ Invoke compiled LangGraph
       await compiled_graph.ainvoke(initial_state)
```

### Step 4: LangGraph Execution

```
LangGraph Sequential Execution:

1. symptom_node (SymptomAgent - REAL)
   Input: Initial state
   Provider Call: OpenAI/Groq LLM
   Output: Updated state with symptom_analysis
   Duration: ~2-3 seconds

2. risk_node (RiskAgent - MOCK)
   Input: State with symptom_analysis
   Logic: Simple mock logic
   Output: Updated state with risk_assessment
   Duration: <10ms

3. specialist_node (SpecialistAgent - MOCK)
   Input: State with risk_assessment
   Logic: Simple mock logic
   Output: Updated state with specialist_recommendation
   Duration: <10ms

4. report_node (ReportAgent - MOCK)
   Input: State with specialist_recommendation
   Logic: Generate report from previous results
   Output: Final state with health_report
   Duration: <10ms

Total workflow time: ~3-5 seconds (dominated by LLM call)
```

### Step 5: Result Extraction

```
AnalysisWorkflow extracts results:
    AnalysisResult(
        analysis_id="abc123",
        risk_assessment=state["risk_assessment"],
        specialist_recommendation=state["specialist_recommendation"],
        health_report=state["health_report"],
        emergency_alert=False
    )
```

### Step 6: API Response

```
API transforms AnalysisResult:
    ApiResponse(
        success=True,
        message="Health analysis created successfully",
        data={
            "analysis_id": "abc123",
            "risk_level": "moderate",
            "confidence": 82.0,
            "specialist": "General Physician",
            "emergency": False
        },
        errors=None
    )

HTTP 200 Response
```

---

## Error Handling in Workflows

### Provider Error

```
SymptomAgent encounters error:
    try:
        symptom_result = await provider.analyze_symptoms_structured(input_data)
    except Exception as e:
        state["errors"].append(f"Symptom analysis error: {str(e)}")
        state["current_step"] = "symptom_analysis_failed"
    
Result:
    - State includes error message
    - Workflow continues (graceful degradation)
    - Other agents still execute
    - Final result includes error information
```

### JSON Parse Error

```
OpenAIProvider encounters JSON parse error:
    try:
        symptom_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response: {e}")
        raise ValueError(f"Invalid JSON response from LLM: {e}")
    
Result:
    - Error propagated to SymptomAgent
    - SymptomAgent catches and logs
    - State includes error message
    - Workflow can retry or continue
```

---

## Data Flow Summary

```
User Input
    ↓
API Request
    ↓
AnalysisService
    ├─ Create AnalysisInput
    ├─ Call AnalysisWorkflow
    └─ Return AnalysisResult
    ↓
AnalysisWorkflow
    ├─ Initialize HealthAnalysisState
    ├─ Invoke LangGraph
    └─ Extract results from final state
    ↓
LangGraph Execution (Sequential)
    ├─ SymptomAgent
    │   ├─ Initialize OpenAIProvider
    │   ├─ Call LLM with prompt
    │   ├─ Parse JSON response
    │   └─ Update symptom_analysis in state
    ├─ RiskAgent
    │   ├─ Read symptom_analysis
    │   ├─ Assess risk
    │   └─ Update risk_assessment in state
    ├─ SpecialistAgent
    │   ├─ Read risk_assessment
    │   ├─ Recommend specialist
    │   └─ Update specialist_recommendation in state
    └─ ReportAgent
        ├─ Read previous results
        ├─ Generate report
        └─ Update health_report in state
    ↓
AnalysisResult (extracted from final state)
    ├─ analysis_id
    ├─ risk_assessment
    ├─ specialist_recommendation
    └─ health_report
    ↓
API Response (transformed for HTTP)
    ├─ success: true
    ├─ message: "..."
    ├─ data: {...}
    └─ errors: null
    ↓
HTTP Response (JSON)
    ↓
Frontend Display
```

---

## Future Roadmap

### v0.7.2 - Real Risk Agent
- [ ] Implement RiskAssessmentPrompt
- [ ] Add OpenAIProvider.analyze_risk_structured()
- [ ] Replace RiskAgent mock with real LLM calls
- [ ] Test with various symptom combinations

### v0.7.3 - Real Specialist Agent
- [ ] Implement SpecialistPrompt
- [ ] Add OpenAIProvider.analyze_specialist_structured()
- [ ] Replace SpecialistAgent mock with real LLM calls
- [ ] Extend with doctor database integration

### v0.7.4 - Real Report Agent
- [ ] Implement ReportPrompt
- [ ] Add OpenAIProvider.generate_report_structured()
- [ ] Replace ReportAgent mock with real LLM calls
- [ ] Add PDF generation capability

### v0.8+ - Enhanced Agents
- [ ] Emergency detection agent
- [ ] Drug interaction checker
- [ ] Medical history integration agent
- [ ] Doctor matching agent

---

## Summary

HealWell's AI architecture combines:
- **LangGraph** for multi-step workflow orchestration
- **Agent pattern** for specialized medical reasoning
- **Provider abstraction** for flexible LLM integration
- **Shared state** for agent coordination
- **Type-safe models** for data validation

Current status:
- ✅ SymptomAgent: Real LLM calls (v0.7.1)
- 🔄 RiskAgent: Mock (v0.7.2 coming)
- 🔄 SpecialistAgent: Mock (v0.7.3 coming)
- 🔄 ReportAgent: Mock (v0.7.4 coming)

The architecture supports rapid agent implementation and provider additions without major refactoring.
