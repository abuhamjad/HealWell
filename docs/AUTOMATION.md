# HealWell Automation & AI Integration

## Status
✅ **v0.6 LangGraph Workflow Complete** - Full workflow orchestration with mock AI responses operational.

## AI Module Architecture

### Provider Layer (`app/ai/providers/`)

**Purpose**: Abstract interface for multiple AI service providers.

**Components**:
- `BaseProvider`: Abstract base class defining provider interface
  - `async initialize()`: Initialize provider resources
  - `async analyze_symptoms()`: Perform symptom analysis
  - `async generate_report()`: Generate health reports
  - `async health_check()`: Check provider status

- `GeminiProvider`: Google Gemini implementation (placeholder)
  - Implements BaseProvider interface
  - Ready for Gemini API integration
  - All methods return TODO placeholders currently

**Usage Pattern**:
```python
async with GeminiProvider(api_key="...") as provider:
    result = await provider.analyze_symptoms(input_data)
```

### Prompt Templates (`app/ai/prompts/`)

**Purpose**: Structured prompt generation for AI models.

**Components**:
- `symptom_prompt.py`: Generates symptom analysis prompts
- `risk_prompt.py`: Generates risk assessment prompts
- `specialist_prompt.py`: Generates specialist recommendation prompts
- `report_prompt.py`: Generates health report prompts

**Features**:
- Template-based prompt construction
- Context-aware prompt generation
- Extensible for multiple LLM types

### Agents (`app/ai/agents/`)

**Purpose**: Specialized agents for each analysis step.

**Components**:
- `BaseAgent`: Abstract agent interface
  - Execution via `async execute(state: dict[str, Any]) -> dict[str, Any]`
  - Receives complete HealthAnalysisState as input
  - Returns updated HealthAnalysisState as output
  - No agent overwrites unrelated state fields

- `SymptomAgent`: Analyzes patient symptoms
  - Input: user_input field from state
  - Output: Updates symptom_analysis field
  - Mock Data: Detected symptoms, confidence scores

- `RiskAgent`: Assesses health risk level
  - Input: symptom_analysis from previous step
  - Output: Updates risk_assessment field
  - Mock Data: risk_level (low/moderate/high), confidence, reasoning, warning_signs

- `SpecialistAgent`: Recommends appropriate specialists
  - Input: risk_assessment from previous step
  - Output: Updates specialist_recommendation field
  - Mock Data: specialist type, urgency, reasoning

- `ReportAgent`: Generates health reports
  - Input: All previous analysis results
  - Output: Updates health_report field
  - Mock Data: Summary, home care, lifestyle, monitoring, references

**Architecture**:
- Shared state pattern (no local state management)
- Async execution support
- Isolated responsibility (each agent updates one field)
- Ready for Gemini API replacement

### Workflow State (`app/ai/state/`)

**Purpose**: Shared state for entire workflow.

**Components**:
- `HealthAnalysisState` (TypedDict): Single source of truth
  - Contains all workflow data at any point in execution
  - Fields initialized progressively as agents execute
  - Passed between all agent nodes
  - No duplication of data

### Workflows (`app/ai/workflows/`)

**Purpose**: Orchestrates agent execution flow.

**Components**:
- `HealthGraph`: Graph visualization support
  - Node documentation for frontend visualization
  - Edge descriptions for workflow flow
  - Ready for UI integration

- `AnalysisWorkflow`: Orchestrates complete analysis via LangGraph
  - Initializes HealthAnalysisState with user input
  - Invokes compiled LangGraph (async via `ainvoke()`)
  - Extracts results from final state
  - Returns structured AnalysisResult

**Workflow Steps**:
1. Initialize HealthAnalysisState
2. Execute SymptomAgent (symptom analysis)
3. Execute RiskAgent (risk assessment)
4. Execute SpecialistAgent (specialist matching)
5. Execute ReportAgent (report generation)
6. Extract results from final state

### AI Models (`app/ai/models/`)

**Purpose**: Type definitions for AI operations.

**Models**:
- `AnalysisInput`: User input data structure
- `AnalysisResult`: Complete analysis output
- `RiskAssessment`: Risk evaluation result
- `SpecialistRecommendation`: Specialist matching output
- `HealthReport`: Generated health report

**Features**:
- Pydantic validation
- Type safety
- API contract definition

## Business Service Layer

The AI module integrates with the business service layer:

- `AnalysisService`: Orchestrates AI workflow
- `HistoryService`: Manages medical history
- `DoctorService`: Finds nearby doctors
- `ReportService`: Manages report generation

Services delegate to AI providers for actual processing.

## LangGraph Automation Workflow (v0.6 - Operational)

```
HealthAnalysisState (initialized with user input)
    ↓
SymptomAgent (analyzes symptoms, updates state)
    ↓
RiskAgent (assesses risk, updates state)
    ↓
SpecialistAgent (recommends specialist, updates state)
    ↓
ReportAgent (generates report, updates state)
    ↓
Final HealthAnalysisState (all results available)
```

## Workflow Architecture

**Execution Model**: Sequential agent execution with shared state
- Each agent is a node in the LangGraph workflow
- Each agent receives the complete HealthAnalysisState
- Each agent updates only its own output field(s)
- State flows from one agent to the next
- No data duplication across agents
- Each agent is independent and replaceable

**Data Flow**:
```
Initial State
├── session_id
├── user_input
├── analysis_input
├── metadata
└── empty fields for results

     ↓ (SymptomAgent)

Intermediate State
├── symptom_analysis (populated)
└── other fields unchanged

     ↓ (RiskAgent)

Intermediate State
├── symptom_analysis
├── risk_assessment (populated)
└── other fields unchanged

     ↓ (SpecialistAgent)

Intermediate State
├── symptom_analysis
├── risk_assessment
├── specialist_recommendation (populated)
└── other fields unchanged

     ↓ (ReportAgent)

Final State
├── symptom_analysis
├── risk_assessment
├── specialist_recommendation
├── health_report (populated)
└── other fields unchanged
```

## Implementation Status

### Completed (v0.5)
- ✅ Provider architecture and BaseProvider interface
- ✅ GeminiProvider placeholder implementation
- ✅ Prompt template modules
- ✅ Agent classes (SymptomAgent, RiskAgent, SpecialistAgent, ReportAgent)
- ✅ HealthGraph workflow structure
- ✅ AnalysisWorkflow orchestration
- ✅ AI models with Pydantic validation
- ✅ Service layer integration

### Completed (v0.6)
- ✅ LangGraph workflow orchestration
- ✅ HealthAnalysisState (TypedDict) shared workflow state
- ✅ Agent integration with shared state pattern
- ✅ Mock AI responses for all agents
- ✅ Async workflow execution via LangGraph
- ✅ Complete end-to-end workflow pipeline
- ✅ Service layer maintains API contract
- ✅ Workflow visualization documentation

### Pending (v0.7)
- ⏳ Gemini API integration (replace mock responses)
- ⏳ Prompt engineering and optimization
- ⏳ Structured JSON output from Gemini
- ⏳ Error handling and validation

## Architecture Integration

The AI module integrates into the FastAPI stack:

```
FastAPI Routes (api/routes/)
    ↓
Service Layer (services/)
    ↓
AI Module (ai/)
    ├── Workflows (coordinate execution)
    ├── Agents (process steps)
    ├── Providers (AI implementation)
    ├── Prompts (instruction templates)
    └── Models (type definitions)
    ↓
Response Layer (schemas/response.py)
```

## Future Roadmap (v0.7+)

1. **Gemini Integration (v0.7)**: Replace mock responses with Gemini API calls
   - Implement GeminiProvider.analyze_symptoms()
   - Implement GeminiProvider.generate_report()
   - Structured output parsing (JSON from LLM)
   
2. **Advanced Features (v0.8)**:
   - Medical history integration
   - Emergency detection logic
   - Parallel agent execution
   - Context management improvements

3. **Production (v0.9)**:
   - Database persistence
   - Error handling and resilience
   - Performance optimization
   - Logging and monitoring
