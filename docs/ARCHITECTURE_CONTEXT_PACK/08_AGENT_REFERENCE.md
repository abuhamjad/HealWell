# HealWell Agent Reference

## BaseAgent Interface

**Location**: `app/ai/agents/base.py`

```python
class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute agent logic and return updated state"""
        pass
```

---

## SymptomAgent (REAL - v0.7.1)

**Location**: `app/ai/agents/symptom_agent.py`
**Status**: ✅ Production (v0.7.1)

### Purpose
Analyzes patient symptoms using real LLM (Groq/OpenAI API) to identify detected symptoms, assess confidence, and determine affected body systems.

### Inputs (from state)
- `analysis_input`: AnalysisInput (symptoms, medical_history, medications, allergies)
- `metadata`: Patient metadata
- `user_input`: Raw symptom text

### Outputs (to state)
- `symptom_analysis`: dict with detected_symptoms, confidence, summary, severity_indicators, affected_systems
- `current_step`: "symptom_analysis"
- `workflow_status`: "symptom_analysis_complete"
- `errors`: Any error messages

### Execution Flow
```python
async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
    try:
        # 1. Extract analysis input
        analysis_input = state.get("analysis_input")
        
        # 2. Initialize provider (Groq/OpenAI)
        provider = create_provider()
        await provider.initialize()
        
        # 3. Call real LLM for symptom analysis
        symptom_result = await provider.analyze_symptoms_structured(analysis_input)
        
        # 4. Update state with real LLM results
        state["symptom_analysis"] = symptom_result.model_dump()
        state["current_step"] = "symptom_analysis"
        state["workflow_status"] = "symptom_analysis_complete"
        
    except Exception as e:
        # 5. Error handling
        logger.error(f"Symptom analysis failed: {e}")
        state["errors"].append(f"Symptom analysis error: {str(e)}")
        state["current_step"] = "symptom_analysis_failed"
    
    return state
```

### Dependencies
- OpenAIProvider (for LLM calls)
- get_symptom_analysis_prompt (prompt generation)
- SymptomAnalysis (Pydantic model)

### Latency
~2-3 seconds (dominated by LLM API call)

### Example Output
```json
{
  "detected_symptoms": ["persistent cough", "fever", "chest pain"],
  "confidence": 92.0,
  "summary": "Patient presents with respiratory infection symptoms...",
  "severity_indicators": ["fever 38.5°C", "chest pain"],
  "affected_systems": ["respiratory", "cardiovascular", "immune"]
}
```

---

## RiskAgent (MOCK)

**Location**: `app/ai/agents/risk_agent.py`
**Status**: 🔄 Mock (Real LLM planned v0.7.2)

### Purpose
Assesses health risk level (low/moderate/high) based on detected symptoms.

### Inputs
- `symptom_analysis`: Previous agent's output
- `metadata`: Patient metadata

### Outputs
- `risk_assessment`: RiskAssessment model
- `current_step`: "risk_assessment"

### Execution (Current - Mock)
```python
async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
    risk_assessment = state.get("risk_assessment", {})
    
    state["risk_assessment"] = RiskAssessment(
        risk_level="moderate",  # Always moderate (mock)
        confidence=0.82,
        reasoning="Based on detected symptoms...",
        warning_signs=["persistent high fever"],
    )
    state["current_step"] = "risk_assessment"
    return state
```

### Future (v0.7.2 - Real LLM)
- Will call provider.analyze_risk_structured()
- Dynamic risk assessment based on symptoms
- Real confidence scores from LLM

---

## SpecialistAgent (MOCK)

**Location**: `app/ai/agents/specialist_agent.py`
**Status**: 🔄 Mock (Real LLM planned v0.7.3)

### Purpose
Recommends appropriate medical specialist based on risk assessment.

### Inputs
- `risk_assessment`: Previous agent's output

### Outputs
- `specialist_recommendation`: SpecialistRecommendation model
- `current_step`: "specialist_recommendation"

### Execution (Current - Mock)
```python
async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
    state["specialist_recommendation"] = SpecialistRecommendation(
        specialist="General Physician",  # Always GP (mock)
        reasoning="Moderate risk level...",
        urgency="24-48 hours",
    )
    state["current_step"] = "specialist_recommendation"
    return state
```

### Future (v0.7.3 - Real LLM)
- Will call provider.analyze_specialist_structured()
- Dynamic specialist selection
- Urgency assessment from LLM

---

## ReportAgent (MOCK)

**Location**: `app/ai/agents/report_agent.py`
**Status**: 🔄 Mock (Real LLM planned v0.7.4)

### Purpose
Generates comprehensive health guidance report from all previous analyses.

### Inputs
- All previous agent outputs (symptom_analysis, risk_assessment, specialist_recommendation)

### Outputs
- `health_report`: HealthReport model
- `current_step`: "health_report"

### Execution (Current - Mock)
```python
async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
    state["health_report"] = HealthReport(
        summary="Based on analysis, respiratory infection possible...",
        home_care=["Get rest", "Stay hydrated"],
        lifestyle=["Avoid strenuous activities"],
        monitoring=["Monitor temperature daily"],
        references=["WHO guidelines"],
    )
    state["current_step"] = "health_report"
    return state
```

### Future (v0.7.4 - Real LLM)
- Will call provider.generate_report_structured()
- Personalized report from LLM
- Medical reference integration

---

## Agent Development Pattern

### Creating a New Agent

1. **Define Purpose**
   - What medical analysis does it perform?
   - What are inputs and outputs?

2. **Extend BaseAgent**
```python
class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MyAgent")
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        # Implementation
        return state
```

3. **Implement Logic**
   - Read required fields from state
   - Perform analysis (LLM or mock)
   - Update state with results
   - Handle errors gracefully

4. **Add to LangGraph**
```python
# In langgraph_builder.py
async def my_node(state):
    agent = MyAgent()
    return await agent.execute(state)

workflow.add_node("my_agent", my_node)
workflow.add_edge("previous_agent", "my_agent")
```

5. **Test**
   - Unit test agent in isolation
   - Integration test in workflow
   - Test error paths

---

## Agent Error Handling

### Error Propagation
```python
# Agents catch errors and add to state
try:
    # Perform analysis
    result = await expensive_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    state["errors"].append(f"Error: {str(e)}")
    state["current_step"] = f"{agent_name}_failed"
    return state  # Workflow continues

# Downstream agents see error state
# They can:
# 1. Skip processing if error occurred
# 2. Use fallback logic
# 3. Return error state unchanged
```

### Error Best Practices
- Always log errors with context
- Add descriptive messages to state["errors"]
- Don't crash the workflow
- Allow graceful degradation
- Provide fallback responses when possible

---

## Agent Testing

### Unit Test Example
```python
async def test_symptom_agent():
    agent = SymptomAgent()
    
    analysis_input = AnalysisInput(
        symptoms="persistent cough and fever"
    )
    
    state = {
        "analysis_input": analysis_input,
        "metadata": {},
        "errors": [],
    }
    
    result = await agent.execute(state)
    
    assert "symptom_analysis" in result
    assert result["current_step"] == "symptom_analysis"
    assert len(result["errors"]) == 0
```

### Integration Test
```python
async def test_full_workflow():
    workflow = AnalysisWorkflow()
    
    input_data = AnalysisInput(symptoms="symptoms")
    result = await workflow.execute(input_data)
    
    assert result.analysis_id
    assert result.risk_assessment
    assert result.specialist_recommendation
    assert result.health_report
```

### Mock Provider Testing
```python
class MockProvider(BaseProvider):
    async def analyze_symptoms_structured(self, input_data):
        return SymptomAnalysis(
            detected_symptoms=["test symptom"],
            confidence=100.0,
            summary="Test summary",
        )
```

---

## Agent Execution Summary

| Agent | Status | Input | Output | Latency |
|-------|--------|-------|--------|---------|
| SymptomAgent | ✅ Real | symptoms | symptom_analysis | ~3s |
| RiskAgent | 🔄 Mock | symptom_analysis | risk_assessment | <10ms |
| SpecialistAgent | 🔄 Mock | risk_assessment | specialist_recommendation | <10ms |
| ReportAgent | 🔄 Mock | all previous | health_report | <10ms |

---

## Future Agents (Planned)

### v0.8+
- **EmergencyAgent**: Detect emergency symptoms (chest pain, difficulty breathing, etc.)
- **DrugInteractionAgent**: Check medication interactions
- **HistoryAgent**: Integrate patient medical history
- **DoctorMatchingAgent**: Find best specialists
- **AppointmentAgent**: Schedule appointments (future)

### Roadmap
```
v0.7.1: SymptomAgent (REAL)
v0.7.2: RiskAgent (REAL)
v0.7.3: SpecialistAgent (REAL)
v0.7.4: ReportAgent (REAL)
v0.8:   Additional agents + features
v0.9+:  Production hardening + new agents
```

---

## Summary

Agents are specialized components that:
- Receive HealthAnalysisState as input
- Update specific state fields
- Return modified state
- Are executed sequentially by LangGraph
- Have clear input/output contracts
- Handle errors gracefully
- Are testable in isolation
- Follow consistent patterns for new additions
