# HealWell Provider System

## Overview
The provider system abstracts LLM implementations, allowing multiple AI services (OpenAI, Gemini, Groq, etc.) to be used interchangeably.

---

## BaseProvider Interface

**Location**: `app/ai/providers/base.py`

```python
class BaseProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.is_initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider resources"""
        pass
    
    @abstractmethod
    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        """Analyze symptoms"""
        pass
    
    @abstractmethod
    async def generate_report(self, analysis_result: AnalysisResult) -> Dict:
        """Generate health report"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check provider health"""
        pass
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
```

---

## OpenAIProvider (ACTIVE - v0.7.1)

**Location**: `app/ai/providers/openai_provider.py`
**Status**: Production (v0.7.1) - Real LLM calls

### Initialization
```python
class OpenAIProvider(BaseProvider):
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
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self.is_initialized = True
```

### Real Symptom Analysis (v0.7.1)
```python
async def analyze_symptoms_structured(
    self,
    input_data: AnalysisInput
) -> SymptomAnalysis:
    """Make real LLM call for symptom analysis"""
    
    prompt = get_symptom_analysis_prompt(
        symptoms=input_data.symptoms,
        medical_history=input_data.medical_history,
        medications=input_data.medications,
        allergies=input_data.allergies,
    )
    
    response = await self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": "You are a medical AI..."},
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

### Mock Analysis (Other Methods)
```python
async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
    """Placeholder implementation - returns mock data"""
    # TODO: Implement real LLM calls for risk, specialist, report
    
    return AnalysisResult(
        analysis_id=str(uuid.uuid4()),
        risk_assessment=RiskAssessment(...),
        specialist_recommendation=SpecialistRecommendation(...),
        health_report=HealthReport(...),
        emergency_alert=False,
    )

async def generate_report(self, analysis_result: AnalysisResult) -> Dict:
    """Placeholder implementation"""
    # TODO: Implement real report generation
    pass

async def health_check(self) -> bool:
    """Check provider health"""
    if not self.is_initialized or not self.client:
        return False
    try:
        await self.client.models.list()
        return True
    except Exception:
        return False
```

### Configuration
```python
# .env
LLM_PROVIDER=openai
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=<groq-api-key>
LLM_MODEL=openai/gpt-oss-120b
LLM_TIMEOUT=30
```

---

## GeminiProvider (PLACEHOLDER)

**Location**: `app/ai/providers/gemini.py`
**Status**: Placeholder (v0.7.0)

```python
class GeminiProvider(BaseProvider):
    """Google Gemini provider implementation"""
    
    async def initialize(self) -> None:
        # TODO: Initialize Gemini SDK
        pass
    
    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        # TODO: Implement Gemini API calls
        pass
    
    async def generate_report(self, analysis_result: AnalysisResult) -> Dict:
        # TODO: Implement report generation
        pass
    
    async def health_check(self) -> bool:
        return self.is_initialized
```

**Future Implementation**:
- Initialize Gemini SDK
- Implement async API calls
- Handle Gemini-specific response format
- Add Gemini configuration to settings

---

## Provider Factory

**Location**: `app/ai/providers/factory.py`

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

**Usage**:
```python
provider = create_provider()  # Selected by LLM_PROVIDER env var
await provider.initialize()
result = await provider.analyze_symptoms(input_data)
```

---

## Configuration Management

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `openai` | Provider type (openai, gemini) |
| `LLM_BASE_URL` | `https://api.groq.com/openai/v1` | API base URL |
| `LLM_API_KEY` | `` | API authentication key |
| `LLM_MODEL` | `openai/gpt-oss-120b` | Model identifier |
| `LLM_TIMEOUT` | `30` | Request timeout (seconds) |
| `GEMINI_API_KEY` | `` | Gemini-specific API key (future) |

### Settings Integration

**Location**: `app/core/config.py`

```python
class Settings(BaseSettings):
    LLM_PROVIDER: str = "openai"
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "openai/gpt-oss-120b"
    LLM_TIMEOUT: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
```

---

## Groq API (Current Provider)

### What is Groq?
Groq provides OpenAI-compatible API endpoints but with different model names and potentially better latency.

### Configuration
```python
# Development
LLM_PROVIDER=openai
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_API_KEY=gsk_...
LLM_MODEL=openai/gpt-oss-120b
LLM_TIMEOUT=30
```

### API Endpoint
```
https://api.groq.com/openai/v1/chat/completions
```

### Usage Example
```python
client = AsyncOpenAI(
    api_key="gsk_...",
    base_url="https://api.groq.com/openai/v1",
    timeout=30,
)

response = await client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[...],
    temperature=0.7,
    max_tokens=1000,
)
```

---

## Provider Switching

### Change Provider at Runtime

**Method 1: Environment Variable**
```bash
export LLM_PROVIDER=gemini
export GEMINI_API_KEY=...
python -m uvicorn app.main:app
```

**Method 2: Docker**
```dockerfile
ENV LLM_PROVIDER=gemini
ENV GEMINI_API_KEY=...
```

**Method 3: Programmatic**
```python
# settings override (testing only)
settings.LLM_PROVIDER = "gemini"
provider = create_provider()
```

---

## Error Handling

### Provider Errors
```python
try:
    await provider.initialize()
except Exception as e:
    logger.error(f"Provider initialization failed: {e}")
    raise

try:
    result = await provider.analyze_symptoms(input_data)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON response: {e}")
    raise ValueError(f"Invalid JSON from LLM: {e}")
except Exception as e:
    logger.error(f"Analysis failed: {e}")
    raise
```

### Provider Health Check
```python
if await provider.health_check():
    # Provider is healthy
    pass
else:
    # Provider is unhealthy or not initialized
    logger.error("Provider health check failed")
```

---

## Future Providers

### Planned Implementations

| Provider | Status | Timeline |
|----------|--------|----------|
| OpenAI | 🔄 Partial (v0.7.1) | Real symptom analysis only |
| Groq | ✅ Active (v0.7.1) | Via OpenAI compatibility |
| Gemini | 📋 Planned | v0.8 |
| Claude | 📋 Planned | v0.8+ |
| Llama | 📋 Possible | v0.9+ |

### Adding a New Provider

1. **Create Provider Class**
```python
class NewProvider(BaseProvider):
    async def initialize(self) -> None:
        # Initialize SDK
        pass
    
    async def analyze_symptoms(self, input_data) -> AnalysisResult:
        # Implement analysis
        pass
    
    async def generate_report(self, analysis_result) -> Dict:
        # Implement report
        pass
    
    async def health_check(self) -> bool:
        # Check health
        pass
```

2. **Update Factory**
```python
def create_provider() -> BaseProvider:
    if provider_name == "new_provider":
        return NewProvider(api_key=settings.NEW_PROVIDER_API_KEY)
```

3. **Add Configuration**
```python
# settings
NEW_PROVIDER_API_KEY: str = ""
```

4. **Add Environment Variable**
```bash
NEW_PROVIDER_API_KEY=...
```

---

## Testing Providers

### Mock Provider for Testing
```python
class MockProvider(BaseProvider):
    async def initialize(self) -> None:
        self.is_initialized = True
    
    async def analyze_symptoms(self, input_data) -> AnalysisResult:
        return AnalysisResult(...)  # Predetermined response
    
    async def generate_report(self, analysis_result) -> Dict:
        return {}
    
    async def health_check(self) -> bool:
        return True
```

### Usage in Tests
```python
@pytest.fixture
def mock_provider():
    return MockProvider()

async def test_symptom_agent(mock_provider):
    agent = SymptomAgent()
    state = {"analysis_input": ..., "metadata": ...}
    # Can mock provider calls
```

---

## Summary

The provider system:
- Abstracts LLM implementations via BaseProvider interface
- Supports multiple providers (OpenAI, Gemini, Groq, etc.)
- Factory pattern for runtime provider selection
- Configuration-driven via environment variables
- Easy to add new providers
- Supports testing with mock providers

Current status:
- ✅ OpenAIProvider: Real symptom analysis (v0.7.1)
- 🔄 GeminiProvider: Placeholder (v0.8 planned)
- 🔄 Other providers: Future implementation
