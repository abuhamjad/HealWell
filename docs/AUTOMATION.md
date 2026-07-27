# HealWell AI Workflow - v1.0.0

Complete LangGraph-based AI automation workflow with OpenAI-compatible LLM integration.

## Status

✅ **v1.0.0 Complete** - Full workflow orchestration with real OpenAI LLM integration operational.

## Architecture Overview

```
FastAPI Route (/api/v1/analysis)
    ↓
AnalysisService
    ↓
AnalysisWorkflow
    ↓
Compiled LangGraph
    ↓
[SymptomAgent] → [RiskAgent] → [SpecialistAgent] → [EmergencyAgent] → [ReportAgent]
    ↓
OpenAI API (via Provider)
    ↓
AnalysisResult
    ↓
Frontend
```

## LangGraph Workflow

### Workflow State (`app/ai/state/health_state.py`)

**HealthAnalysisState** (TypedDict):

```python
{
    "session_id": str,                              # Unique workflow ID
    "user_input": str,                              # Raw symptoms
    "analysis_input": AnalysisInput,                # Parsed input
    "symptom_analysis": dict,                       # Detected symptoms
    "risk_assessment": RiskAssessment,              # Risk evaluation
    "specialist_recommendation": SpecialistRecommendation,  # Specialist type
    "health_report": HealthReport,                  # Recommendations
    "workflow_status": str,                         # Execution status
    "current_step": str,                            # Last executed agent
    "errors": List[str],                            # Error tracking
    "metadata": dict,                               # Medical context
}
```

### Workflow Graph (`app/ai/graphs/langgraph_builder.py`)

```python
def compile_health_analysis_graph() -> CompiledStateGraph:
    graph = StateGraph(HealthAnalysisState)
    
    # Add agent nodes
    graph.add_node("symptom_analysis", symptom_agent)
    graph.add_node("risk_assessment", risk_agent)
    graph.add_node("specialist_recommendation", specialist_agent)
    graph.add_node("emergency_detection", emergency_agent)
    graph.add_node("health_report", report_agent)
    
    # Sequential execution
    graph.add_edge("START", "symptom_analysis")
    graph.add_edge("symptom_analysis", "risk_assessment")
    graph.add_edge("risk_assessment", "specialist_recommendation")
    graph.add_edge("specialist_recommendation", "emergency_detection")
    graph.add_edge("emergency_detection", "health_report")
    graph.add_edge("health_report", "END")
    
    return graph.compile()
```

### Workflow Execution

```python
async def execute(analysis_input: AnalysisInput) -> AnalysisResult:
    # Initialize state
    initial_state = HealthAnalysisState(
        session_id=str(uuid.uuid4()),
        user_input=analysis_input.symptoms,
        analysis_input=analysis_input,
        # ... other fields
    )
    
    # Execute compiled graph
    final_state = await compiled_graph.ainvoke(initial_state)
    
    # Extract results
    return AnalysisResult(
        analysis_id=final_state["session_id"],
        risk_level=final_state["risk_assessment"]["level"],
        # ...
    )
```

## AI Agents

### 1. Symptom Analysis Agent

**Purpose:** Parse and normalize symptoms

**Input:**
- `user_input` - Raw symptom description
- `metadata` - Optional medical history, medications, allergies

**Output:**
- `symptom_analysis` - Detected symptoms with confidence scores

**Implementation:**

```python
async def symptom_agent(state: HealthAnalysisState) -> HealthAnalysisState:
    prompt = generate_symptom_prompt(state["user_input"], state["metadata"])
    response = await llm_provider.structured_call(prompt, SYMPTOM_SCHEMA)
    state["symptom_analysis"] = response
    return state
```

### 2. Risk Assessment Agent

**Purpose:** Evaluate medical risk level

**Input:**
- `symptom_analysis` - Detected symptoms
- `metadata` - Medical history context

**Output:**
- `risk_assessment` - RiskAssessment with level, confidence, reasoning

**Risk Levels:**
- `low` - No immediate concern
- `moderate` - Warrants specialist evaluation
- `high` - Urgent attention needed

**Implementation:**

```python
async def risk_agent(state: HealthAnalysisState) -> HealthAnalysisState:
    prompt = generate_risk_prompt(state["symptom_analysis"])
    response = await llm_provider.structured_call(prompt, RISK_SCHEMA)
    state["risk_assessment"] = response
    return state
```

### 3. Specialist Recommendation Agent

**Purpose:** Determine appropriate specialist

**Input:**
- `risk_assessment` - Risk level and factors
- `symptom_analysis` - Detected symptoms

**Output:**
- `specialist_recommendation` - SpecialistRecommendation with specialist type, urgency

**Supported Specialists:**
- General Physician
- Cardiologist
- Neurologist
- Pulmonologist
- Gastroenterologist
- Orthopedic Surgeon
- Dermatologist
- Psychiatrist

**Implementation:**

```python
async def specialist_agent(state: HealthAnalysisState) -> HealthAnalysisState:
    prompt = generate_specialist_prompt(state["risk_assessment"])
    response = await llm_provider.structured_call(prompt, SPECIALIST_SCHEMA)
    state["specialist_recommendation"] = response
    return state
```

### 4. Emergency Detection Agent

**Purpose:** Identify emergency conditions

**Input:**
- `symptom_analysis` - Detected symptoms
- `risk_assessment` - Risk evaluation

**Output:**
- Updates state with emergency flag
- Returns emergency message if detected

**Detects:**
- Severe chest pain
- Difficulty breathing
- Severe allergic reactions
- Stroke symptoms
- Severe bleeding
- Severe trauma
- Other life-threatening conditions

**Implementation:**

```python
async def emergency_agent(state: HealthAnalysisState) -> HealthAnalysisState:
    prompt = generate_emergency_prompt(state["symptom_analysis"])
    response = await llm_provider.structured_call(prompt, EMERGENCY_SCHEMA)
    if response["is_emergency"]:
        state["emergency_message"] = "🚨 EMERGENCY: Call 911 or local emergency number"
    return state
```

### 5. Health Report Agent

**Purpose:** Generate personalized health recommendations

**Input:**
- `risk_assessment` - Risk evaluation
- `specialist_recommendation` - Specialist type
- `symptom_analysis` - Detected symptoms
- `metadata` - Medical history context

**Output:**
- `health_report` - HealthReport with recommendations

**Includes:**
- Summary of findings
- Key findings list
- Self-care recommendations
- When to seek care guidance
- Lifestyle modifications
- Monitoring instructions

**Implementation:**

```python
async def report_agent(state: HealthAnalysisState) -> HealthAnalysisState:
    prompt = generate_report_prompt(
        state["symptom_analysis"],
        state["risk_assessment"],
        state["specialist_recommendation"]
    )
    response = await llm_provider.structured_call(prompt, REPORT_SCHEMA)
    state["health_report"] = response
    return state
```

## LLM Provider Layer

### Provider Interface (`app/ai/providers/base.py`)

```python
class BaseProvider(ABC):
    @abstractmethod
    async def call_llm(self, prompt: str) -> str:
        """Call LLM with prompt"""
        pass
    
    @abstractmethod
    async def structured_call(self, prompt: str, schema: dict) -> dict:
        """Call LLM and parse structured output"""
        pass
```

### OpenAI Provider (`app/ai/providers/openai_provider.py`)

```python
class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str, base_url: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    async def call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return response.choices[0].message.content
    
    async def structured_call(self, prompt: str, schema: dict) -> dict:
        # Call LLM
        response_text = await self.call_llm(prompt)
        # Parse JSON response
        return json.loads(response_text)
```

### Provider Factory

```python
def create_provider() -> BaseProvider:
    return OpenAIProvider(
        api_key=settings.LLM_API_KEY,
        model=settings.LLM_MODEL,
        base_url=settings.LLM_BASE_URL
    )
```

## Prompt Templates

### Symptom Analysis Prompt (`app/ai/prompts/symptom_prompt.py`)

```python
def generate_symptom_prompt(symptoms: str, metadata: dict) -> str:
    return f"""
    Analyze the following symptoms and provide a structured response:
    
    Symptoms: {symptoms}
    Medical History: {metadata.get('medical_history', 'None')}
    Current Medications: {metadata.get('medications', 'None')}
    Allergies: {metadata.get('allergies', 'None')}
    
    Respond with JSON:
    {{
        "detected_symptoms": ["symptom1", "symptom2", ...],
        "symptom_severity": "mild|moderate|severe",
        "confidence": 0.0-1.0,
        "reasoning": "explanation"
    }}
    """
```

Similar templates for:
- `risk_prompt.py` - Risk assessment
- `specialist_prompt.py` - Specialist recommendation
- `emergency_prompt.py` - Emergency detection
- `report_prompt.py` - Health report generation

## Data Models

### AnalysisInput

```python
class AnalysisInput(BaseModel):
    symptoms: str
    user_id: Optional[str] = None
    medical_history: Optional[str] = None
    medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
```

### RiskAssessment

```python
class RiskAssessment(BaseModel):
    level: Literal["low", "moderate", "high"]
    confidence: float
    reasoning: str
    factors: List[str]
    recommendations: List[str]
```

### SpecialistRecommendation

```python
class SpecialistRecommendation(BaseModel):
    specialist: str
    reason: str
    urgency: Literal["low", "moderate", "high"]
    suggested_timeline: str
```

### HealthReport

```python
class HealthReport(BaseModel):
    summary: str
    key_findings: List[str]
    self_care: List[str]
    when_to_seek_care: str
```

### AnalysisResult

```python
class AnalysisResult(BaseModel):
    analysis_id: str
    risk_level: str
    confidence: float
    specialist: str
    emergency: bool
    risk_assessment: RiskAssessment
    specialist_recommendation: SpecialistRecommendation
    health_report: HealthReport
    emergency_message: Optional[str] = None
```

## Workflow Execution Flow

```
1. User submits symptoms
   ↓
2. AnalysisService.analyze() called
   ↓
3. AnalysisWorkflow.execute() initializes state
   ↓
4. LangGraph executes compiled workflow:
   
   a) SymptomAgent:
      - Calls LLM with symptom prompt
      - Parses detected symptoms
      - Updates state["symptom_analysis"]
   
   b) RiskAgent:
      - Calls LLM with risk assessment prompt
      - Evaluates medical risk
      - Updates state["risk_assessment"]
   
   c) SpecialistAgent:
      - Calls LLM with specialist prompt
      - Recommends appropriate specialist
      - Updates state["specialist_recommendation"]
   
   d) EmergencyAgent:
      - Calls LLM with emergency prompt
      - Detects emergency conditions
      - Sets emergency flag if needed
   
   e) ReportAgent:
      - Calls LLM with report prompt
      - Generates recommendations
      - Updates state["health_report"]
   
   ↓
5. Final state extracted
   ↓
6. AnalysisResult created
   ↓
7. Response returned to frontend
   ↓
8. User sees results and recommendations
```

## Performance Characteristics

- **Sequential Execution:** Agents execute one after another
- **Total Latency:** 5-10 seconds (5 LLM calls × 1-2 seconds each)
- **Timeout:** 30 seconds maximum
- **Scalability:** Stateless - infinite horizontal scaling
- **Reliability:** Retry logic at provider level

## Error Handling

- Invalid symptom input → 400 Bad Request
- LLM timeout → 500 Internal Server Error
- Invalid JSON response → Retry or 500 error
- Medical safety issues → Emergency detection

## Production Features

✅ **Robust:**
- Timeout handling (30s max)
- Retry logic for transient failures
- JSON schema validation
- Error tracking in state

✅ **Scalable:**
- Stateless workflow
- Async execution
- LangGraph optimization
- No database dependencies

✅ **Observable:**
- Session IDs for tracking
- Workflow status logging
- Step-by-step progress
- Error tracking

## Testing

```python
# Unit test example
async def test_symptom_agent():
    state = HealthAnalysisState(user_input="fever and cough")
    result = await symptom_agent(state)
    assert "symptom_analysis" in result
    assert len(result["symptom_analysis"]["detected_symptoms"]) > 0

# Integration test example
async def test_full_workflow():
    workflow = AnalysisWorkflow()
    result = await workflow.execute(
        AnalysisInput(symptoms="severe chest pain")
    )
    assert result.emergency == True
    assert result.emergency_message is not None
```

## Future Enhancements

- Parallel agent execution for non-dependent stages
- Multi-model provider support
- Advanced medical reasoning
- Integration with medical databases
- Real-time workflow monitoring dashboard
- Agent performance analytics

---

**HealWell AI: Powered by LangGraph and OpenAI.**
