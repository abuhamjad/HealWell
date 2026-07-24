# HealWell Development Guide

## Setup Development Environment

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- Groq API key (free tier available)

### Backend Setup
```bash
cd backend
python -m venv .venv

# PowerShell
.\.venv\Scripts\Activate.ps1

# bash
source .venv/bin/activate

pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your Groq API key
# LLM_API_KEY=gsk_...
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev  # Start dev server
```

### Run Both
```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Access at http://localhost:5173
```

---

## Implementing a New Agent

### Step 1: Define Agent Purpose
```python
# What does it analyze?
# What are inputs and outputs?
# What's the reasoning process?
```

### Step 2: Create Agent Class
**File**: `backend/app/ai/agents/new_agent.py`

```python
class NewAgent(BaseAgent):
    """Agent for specific medical analysis"""
    
    def __init__(self):
        super().__init__(name="NewAgent")
    
    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        try:
            # 1. Extract required inputs from state
            input_field = state.get("previous_result")
            
            # 2. Perform analysis (LLM or logic)
            result = await some_analysis(input_field)
            
            # 3. Update state
            state["new_field"] = result
            state["current_step"] = "new_step"
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            state["errors"].append(str(e))
        
        return state
```

### Step 3: Create Output Model
**File**: `backend/app/ai/models/new_output.py`

```python
class NewOutput(BaseModel):
    field1: str
    field2: float
    field3: List[str] = []
```

### Step 4: Add to LangGraph
**File**: `backend/app/ai/graphs/langgraph_builder.py`

```python
# Import agent
from app.ai.agents.new_agent import NewAgent

# In build_health_analysis_graph()
new_agent = NewAgent()

async def new_node(state: dict[str, Any]) -> dict[str, Any]:
    return await new_agent.execute(state)

workflow.add_node("new_agent", new_node)
workflow.add_edge("previous_agent", "new_agent")
workflow.add_edge("new_agent", "next_agent")
```

### Step 5: Test Agent
```python
async def test_new_agent():
    agent = NewAgent()
    state = {
        "previous_result": {...},
        "errors": [],
    }
    result = await agent.execute(state)
    assert "new_field" in result
    assert result["current_step"] == "new_step"
```

---

## Implementing LLM Calls in Agent

### Using Provider Pattern
```python
async def execute(self, state):
    try:
        # Get input
        analysis_input = state.get("analysis_input")
        
        # Create provider (factory pattern)
        provider = create_provider()
        await provider.initialize()
        
        # Call real LLM
        result = await provider.analyze_something(analysis_input)
        
        # Update state
        state["output"] = result.model_dump()
        
    except Exception as e:
        state["errors"].append(str(e))
    
    return state
```

### Adding Provider Method
**File**: `backend/app/ai/providers/openai_provider.py`

```python
async def analyze_something(self, input_data: AnalysisInput) -> OutputModel:
    """Analyze something using LLM"""
    
    # Generate prompt
    prompt = get_analysis_prompt(
        data=input_data.symptoms,
        context=input_data.medical_history,
    )
    
    # Call LLM
    response = await self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": "You are a medical AI..."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    
    # Parse response
    response_text = response.choices[0].message.content.strip()
    result_data = json.loads(response_text)
    
    # Validate
    return OutputModel(
        field1=result_data.get("field1", ""),
        field2=float(result_data.get("field2", 0)),
        field3=result_data.get("field3", []),
    )
```

---

## Implementing Prompts

### Create Prompt Function
**File**: `backend/app/ai/prompts/new_prompt.py`

```python
def get_analysis_prompt(
    data: str,
    context: Optional[str] = None
) -> str:
    """Generate prompt for specific analysis"""
    
    prompt = f"""Analyze the following data:

DATA:
{data}

"""
    
    if context:
        prompt += f"CONTEXT:\n{context}\n\n"
    
    prompt += """RESPONSE FORMAT (JSON ONLY):
{
  "field1": "value",
  "field2": 85,
  "field3": ["item1", "item2"]
}"""
    
    return prompt
```

### Use in Provider
```python
from app.ai.prompts.new_prompt import get_analysis_prompt

prompt = get_analysis_prompt(
    data=input_data.symptoms,
    context=input_data.medical_history,
)
```

---

## Adding New API Endpoint

### Step 1: Create Route Handler
**File**: `backend/app/api/routes/new_route.py`

```python
from fastapi import APIRouter
from app.schemas.response import success_response, ApiResponse
from app.services.new_service import NewService

router = APIRouter(prefix="/new", tags=["new"])
new_service = NewService()

@router.post("", response_model=ApiResponse)
async def create_new(request: NewRequest):
    """Create new resource"""
    result = await new_service.process(request.data)
    return success_response(message="Success", data=result)
```

### Step 2: Create Service
**File**: `backend/app/services/new_service.py`

```python
class NewService:
    async def process(self, data):
        # Business logic here
        return {...}
```

### Step 3: Add to Router
**File**: `backend/app/api/router.py`

```python
from app.api.routes import new_route

api_router.include_router(new_route.router)
```

### Step 4: Test Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/new \
  -H "Content-Type: application/json" \
  -d '{"data": "value"}'
```

---

## Coding Conventions

### Naming
- Classes: PascalCase (SymptomAgent, RiskAssessment)
- Functions: snake_case (execute_analysis, create_provider)
- Constants: UPPER_SNAKE_CASE (API_VERSION)
- Private methods: _snake_case (_initialize_provider)

### Type Hints
```python
# Always use type hints
def process(input_data: AnalysisInput) -> AnalysisResult:
    pass

# For async functions
async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
    pass
```

### Documentation
- Module docstring: """Purpose and overview"""
- Class docstring: """What does it do"""
- Method docstring: """What does it do and return"""
- No multi-line comments; use clear code instead

### Error Handling
```python
try:
    result = await operation()
except SpecificError as e:
    logger.error(f"Context: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    state["errors"].append(str(e))
```

---

## Testing Guidelines

### Unit Tests
```python
# Test agents independently
async def test_symptom_agent():
    agent = SymptomAgent()
    state = {"analysis_input": ..., "metadata": {}, "errors": []}
    result = await agent.execute(state)
    assert "symptom_analysis" in result
```

### Integration Tests
```python
# Test full workflow
async def test_analysis_workflow():
    workflow = AnalysisWorkflow()
    input_data = AnalysisInput(symptoms="test")
    result = await workflow.execute(input_data)
    assert result.analysis_id
```

### Mock Providers
```python
class MockProvider(BaseProvider):
    async def analyze_symptoms_structured(self, input_data):
        return SymptomAnalysis(
            detected_symptoms=["mock"],
            confidence=100.0,
            summary="Test",
        )
```

---

## Debugging Tips

### Enable Logging
```python
import logging
logger = logging.getLogger(__name__)

# In code
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Check Provider Health
```python
provider = create_provider()
await provider.initialize()
is_healthy = await provider.health_check()
```

### Inspect State
```python
# In agent
print("Current state:", json.dumps(state, indent=2, default=str))
```

### Test LLM Calls
```python
# Direct provider test
provider = create_provider()
await provider.initialize()
result = await provider.analyze_symptoms_structured(input_data)
print(result.model_dump())
```

---

## Performance Tips

### Optimize Prompts
- Keep prompts concise
- Remove unnecessary context
- Clear, specific instructions

### Cache Results
- Store identical analysis results
- Reuse for frequent queries
- Implement TTL-based cache

### Async Best Practices
- Use `await` for I/O operations
- Don't block event loop
- Run CPU-heavy work separately

---

## Security Best Practices

### Input Validation
- Use Pydantic models for all inputs
- Validate type and content
- Reject invalid data early

### Secret Management
- Never commit API keys
- Use .env files
- Rotate keys regularly

### Error Messages
- Don't expose internal details
- Log full errors, show generic messages
- Sanitize user-visible errors

---

## Code Review Checklist

Before submitting PR:
- [ ] Code follows naming conventions
- [ ] Type hints present
- [ ] No hardcoded secrets
- [ ] Error handling implemented
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Backward compatible

---

## Deployment Steps

### Development
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### Production
```bash
# Set environment
export ENVIRONMENT=production
export LLM_API_KEY=...

# Run with production settings
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Summary

HealWell development follows:
- **Modular architecture**: Easy to extend
- **Type safety**: Pydantic validation
- **Error handling**: Graceful degradation
- **Testing**: Unit + integration tests
- **Documentation**: Clear conventions
- **Security**: Input validation + secrets management

For new features, follow the patterns shown in existing code (SymptomAgent, OpenAIProvider, etc.)
