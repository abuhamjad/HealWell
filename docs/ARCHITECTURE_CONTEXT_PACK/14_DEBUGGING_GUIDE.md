# HealWell Debugging Guide

## Common Issues & Solutions

### Issue 1: LLM API Call Fails

**Symptoms**:
- "Error: Invalid API key"
- "Error: Connection timeout"
- "Error: Rate limit exceeded"

**Causes**:
1. Invalid or missing `LLM_API_KEY` in .env
2. Groq API is down
3. Exceeded API rate limits
4. Network connectivity issue

**Debugging Steps**:
```bash
# 1. Check .env file
cat .env | grep LLM_

# 2. Verify API key format
# Should start with "gsk_"

# 3. Test API connectivity directly
curl -X POST https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 4. Check logs for full error
# Enable debug logging in config.py
```

**Solution**:
1. Get API key from https://console.groq.com/keys
2. Update .env file
3. Restart backend server
4. Test with curl request

---

### Issue 2: JSON Parse Error from LLM

**Symptoms**:
- "ValueError: Invalid JSON response from LLM"
- Analysis fails completely
- State includes "JSON decode error"

**Causes**:
1. LLM returned malformed JSON
2. LLM didn't follow prompt instructions
3. Prompt needs adjustment

**Debugging Steps**:
```python
# In openai_provider.py, add debug output
response_text = response.choices[0].message.content.strip()
print(f"DEBUG: Raw response: {response_text[:500]}")  # Print first 500 chars

try:
    symptom_data = json.loads(response_text)
except json.JSONDecodeError as e:
    print(f"DEBUG: JSON parse error: {e}")
    print(f"DEBUG: Response text: {response_text}")
    raise
```

**Solution**:
1. Check prompt in symptom_prompt.py
2. Make JSON schema more explicit
3. Add temperature adjustment (0.7 → 0.3 for more deterministic)
4. Add retry logic with different prompt

---

### Issue 3: Empty Symptom Analysis

**Symptoms**:
- `symptom_analysis` field is empty {}
- No detected symptoms
- Agent didn't populate state

**Causes**:
1. Provider initialization failed
2. LLM call returned empty
3. Exception caught but not logged

**Debugging Steps**:
```python
# In symptom_agent.py, add logging
logger.info(f"Analysis input: {analysis_input.model_dump()}")
logger.info(f"Provider created: {type(provider).__name__}")
logger.info(f"Symptom result: {symptom_result.model_dump()}")

# Check state errors
if state.get("errors"):
    print(f"DEBUG: Workflow errors: {state['errors']}")
```

**Solution**:
1. Check error logs
2. Verify provider initialization
3. Test provider directly
4. Check LLM response

---

### Issue 4: Frontend Timeout

**Symptoms**:
- Frontend shows "loading..." for >10 seconds
- Request eventually fails
- Browser console shows network error

**Causes**:
1. LLM API slow (normal, 2-3 seconds expected)
2. Backend crashed
3. Network issue
4. LLM timeout setting too short

**Debugging Steps**:
```bash
# 1. Check backend is running
curl http://localhost:8000/health

# 2. Check timeout setting
grep LLM_TIMEOUT backend/.env
# Should be at least 30 seconds

# 3. Check frontend network tab
# Look at request duration
# Add console.log in frontend service

# 4. Check server logs for errors
```

**Solution**:
1. Increase `LLM_TIMEOUT` to 60 seconds
2. Show loading indicator in UI
3. Implement request timeout handling
4. Add retry logic

---

### Issue 5: CORS Errors

**Symptoms**:
- "Access to XMLHttpRequest blocked by CORS policy"
- Frontend can't reach backend
- Chrome console shows CORS error

**Causes**:
1. Frontend URL not in CORS_ORIGINS
2. CORS middleware not configured
3. Wrong environment setting

**Debugging Steps**:
```bash
# Check CORS configuration
grep CORS backend/.env

# In browser console
# Check request headers
# Look for Access-Control headers in response

# Check if frontend URL matches
# localhost:5173 vs 127.0.0.1:5173
```

**Solution**:
```bash
# Update .env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Or add wildcard for dev (NOT PRODUCTION)
# Edit main.py to allow "*"
```

---

## Debugging Workflow Issues

### Trace Request Through Workflow

**Goal**: Follow data from API request to LLM response

**Steps**:

1. **API Layer**
   ```bash
   # Check request reaches API
   curl -X POST http://localhost:8000/api/v1/analysis \
     -H "Content-Type: application/json" \
     -d '{"symptoms": "test"}'
   ```

2. **Service Layer**
   ```python
   # Add logging in AnalysisService.analyze()
   logger.info(f"Analyzing symptoms: {symptoms[:50]}...")
   result = await self.workflow.execute(input_data)
   logger.info(f"Workflow returned: {result.analysis_id}")
   ```

3. **Workflow Layer**
   ```python
   # Add logging in AnalysisWorkflow.execute()
   logger.info(f"Session {session_id}: Starting workflow")
   final_state = await self.compiled_graph.ainvoke(initial_state)
   logger.info(f"Session {session_id}: Workflow complete")
   ```

4. **Agent Layer**
   ```python
   # Add logging in SymptomAgent.execute()
   logger.info("SymptomAgent: Starting")
   symptom_result = await provider.analyze_symptoms_structured(analysis_input)
   logger.info(f"SymptomAgent: Got {len(symptom_result.detected_symptoms)} symptoms")
   ```

5. **Provider Layer**
   ```python
   # Add logging in OpenAIProvider
   logger.info(f"Calling LLM with model: {self.model}")
   response = await self.client.chat.completions.create(...)
   logger.info(f"LLM response length: {len(response.choices[0].message.content)}")
   ```

---

## Logging Best Practices

### Enable Debug Logging

**config.py**:
```python
LOG_LEVEL = "DEBUG"  # Change from INFO to DEBUG
```

**main.py**:
```python
import logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Add Contextual Logging

```python
# Good
logger.info(f"Analysis started for user {user_id}, symptom count: {len(symptoms)}")

# Bad
logger.info("Starting analysis")
```

### Log at Right Level

```python
# DEBUG: Detailed info for developers
logger.debug(f"State keys: {list(state.keys())}")

# INFO: General information
logger.info(f"Analysis complete: {analysis_id}")

# ERROR: Something went wrong
logger.error(f"LLM call failed: {e}", exc_info=True)

# WARNING: Something unexpected
logger.warning(f"Confidence below threshold: {confidence}")
```

---

## Testing Providers

### Test OpenAI Provider Directly

**Script**: `backend/test_provider.py`

```python
import asyncio
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.models import AnalysisInput

async def test_provider():
    provider = OpenAIProvider()
    await provider.initialize()
    
    input_data = AnalysisInput(
        symptoms="I have a persistent cough and fever"
    )
    
    try:
        result = await provider.analyze_symptoms_structured(input_data)
        print(f"✓ Success!")
        print(f"  Detected: {result.detected_symptoms}")
        print(f"  Confidence: {result.confidence}%")
        print(f"  Summary: {result.summary}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_provider())
```

**Run**:
```bash
cd backend
python test_provider.py
```

---

## Testing Agents

### Test Agent Independently

**Script**: `backend/test_agent.py`

```python
import asyncio
from app.ai.agents.symptom_agent import SymptomAgent
from app.ai.models import AnalysisInput
from app.ai.state import HealthAnalysisState

async def test_agent():
    agent = SymptomAgent()
    
    input_data = AnalysisInput(
        symptoms="I have a cough and fever"
    )
    
    state = {
        "analysis_input": input_data,
        "metadata": {},
        "errors": [],
        "user_input": input_data.symptoms,
    }
    
    result = await agent.execute(state)
    
    if "symptom_analysis" in result:
        print(f"✓ Agent executed successfully")
        print(f"  Symptoms: {result['symptom_analysis'].get('detected_symptoms', [])}")
    else:
        print(f"✗ Agent failed")
        print(f"  Errors: {result.get('errors', [])}")

asyncio.run(test_agent())
```

---

## Testing Workflow

### Test Full Workflow

**Script**: `backend/test_workflow.py`

```python
import asyncio
from app.ai.workflows.analysis_workflow import AnalysisWorkflow
from app.ai.models import AnalysisInput

async def test_workflow():
    workflow = AnalysisWorkflow()
    
    input_data = AnalysisInput(
        symptoms="I have fever and cough for 3 days"
    )
    
    try:
        result = await workflow.execute(input_data)
        print(f"✓ Workflow complete!")
        print(f"  Analysis ID: {result.analysis_id}")
        print(f"  Risk Level: {result.risk_assessment.risk_level}")
        print(f"  Specialist: {result.specialist_recommendation.specialist}")
    except Exception as e:
        print(f"✗ Workflow failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_workflow())
```

---

## Browser Console Debugging

### Frontend Debugging

**Check Network Requests**:
1. Open DevTools (F12)
2. Network tab
3. Find POST /api/v1/analysis
4. Check:
   - Status code (200 = success)
   - Request/Response headers
   - Response body

**Check Frontend Logs**:
1. Console tab
2. Look for errors or warnings
3. Add `console.log()` in React components

```javascript
// In AnalysisPage.tsx
async handleSubmit(symptoms) {
    console.log("Submitting symptoms:", symptoms);
    try {
        const response = await api.analyze(symptoms);
        console.log("Response:", response);
    } catch (error) {
        console.error("Error:", error);
    }
}
```

---

## Performance Profiling

### Measure Response Times

```python
# In backend
import time

async def analyze(self, symptoms: str):
    start = time.time()
    
    # ... analysis code ...
    
    duration = time.time() - start
    logger.info(f"Analysis took {duration:.2f}s")
```

### Identify Bottlenecks

```
Expected breakdown:
- API setup: <10ms
- Service setup: <5ms
- Workflow init: <10ms
- SymptomAgent LLM: ~2800ms (main bottleneck)
- Other agents: <50ms
- Response formatting: <5ms
Total: ~3s (acceptable for medical analysis)
```

---

## State Inspection

### Print Full State

```python
# In any agent
import json
logger.info(f"Current state:\n{json.dumps(state, indent=2, default=str)}")
```

### Trace State Changes

```python
# Before
state_before = state.copy()

# Agent modifies state
state = await agent.execute(state)

# After
changes = {k: state[k] for k in state if state.get(k) != state_before.get(k)}
logger.info(f"State changes: {changes}")
```

---

## Common Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid API key | Wrong Groq key | Update LLM_API_KEY in .env |
| Connection timeout | LLM slow/down | Increase LLM_TIMEOUT to 60s |
| CORS error | Frontend URL missing | Add to CORS_ORIGINS in .env |
| JSON parse error | LLM output malformed | Adjust prompt in symptom_prompt.py |
| Empty results | Agent failed silently | Check state["errors"] |
| 500 server error | Backend exception | Check server logs |
| Validation error | Invalid input | Check request schema |

---

## Summary

Debugging approach:
1. **Identify layer**: API, service, workflow, agent, provider
2. **Add logging**: Log at each layer to trace flow
3. **Test component**: Test component independently
4. **Check data**: Inspect state and responses
5. **Review logs**: Look for error messages
6. **Try workaround**: Adjust settings or add retry
7. **Report issue**: If bug, document for team

Key files to add logging:
- main.py (startup)
- routes (requests)
- services (orchestration)
- agents (processing)
- providers (LLM calls)

Remember: Enable DEBUG logging, add print statements, and always check .env configuration first!
