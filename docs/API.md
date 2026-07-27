# HealWell API Documentation - v1.0.0

Production-ready API for HealWell v1.0.0. Stateless health analysis platform with OpenAI-compatible LLM integration.

## Base URL

**Development:**
```
http://localhost:8000
```

**Production:**
```
https://api.healwell.app
```

## API Versioning

All endpoints use the `/api/v1/` prefix and follow semantic versioning.

---

## Authentication

No authentication required. HealWell is a stateless public API.

---

## Health & Information Endpoints

### GET /

API root endpoint with version and status.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "HealWell API is running",
  "data": {
    "api": "HealWell API",
    "version": "1.0.0",
    "status": "running"
  }
}
```

---

### GET /health

Health check endpoint for monitoring and load balancing.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "healthy",
    "environment": "production"
  }
}
```

---

## Analysis Endpoints

### POST /api/v1/analysis

Submit symptoms for comprehensive health analysis.

Executes the multi-stage LangGraph workflow:
1. Symptom Analysis
2. Risk Assessment
3. Specialist Recommendation
4. Emergency Detection
5. Health Report Generation

**Request:**

```http
POST /api/v1/analysis HTTP/1.1
Content-Type: application/json

{
  "symptoms": "I have had a severe headache and fever for two days"
}
```

**Request Body Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symptoms | string | Yes | Description of user's symptoms |
| user_id | string | No | Optional user identifier |
| medical_history | string | No | Optional medical history context |
| medications | string[] | No | Optional current medications |
| allergies | string[] | No | Optional known allergies |

**Example Request with Optional Fields:**

```json
{
  "symptoms": "Persistent dry cough and chest pain when breathing",
  "medical_history": "Asthma diagnosed 5 years ago",
  "medications": ["Albuterol inhaler", "Vitamin D"],
  "allergies": ["Penicillin"]
}
```

---

**Response (200 OK):**

```json
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
    "risk_level": "moderate",
    "confidence": 0.91,
    "specialist": "Pulmonologist",
    "emergency": false,
    "risk_assessment": {
      "level": "moderate",
      "confidence": 0.91,
      "reasoning": "Dry cough with chest pain suggests possible respiratory condition",
      "factors": [
        "Persistent dry cough",
        "Chest pain on breathing",
        "History of asthma"
      ],
      "recommendations": [
        "Avoid respiratory irritants",
        "Monitor symptoms for 48-72 hours",
        "Consider using humidifier"
      ]
    },
    "specialist_recommendation": {
      "specialist": "Pulmonologist",
      "reason": "Respiratory symptoms with history of asthma warrant specialist evaluation",
      "urgency": "moderate",
      "suggested_timeline": "Schedule within 2-3 days"
    },
    "health_report": {
      "summary": "Based on reported symptoms and medical history, a respiratory evaluation is recommended",
      "key_findings": [
        "Primary concern: Lower respiratory tract involvement",
        "Secondary consideration: Asthma exacerbation"
      ],
      "self_care": [
        "Rest and adequate hydration",
        "Warm fluids to soothe throat",
        "Avoid smoke and air pollution"
      ],
      "when_to_seek_care": "Seek immediate care if shortness of breath increases or chest pain worsens"
    },
    "emergency_message": null
  }
}
```

---

**Response (200 OK) - Emergency Detected:**

```json
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440001",
    "risk_level": "high",
    "confidence": 0.95,
    "specialist": "Emergency Medicine",
    "emergency": true,
    "risk_assessment": {
      "level": "high",
      "confidence": 0.95,
      "reasoning": "Symptoms indicate potential cardiac event"
    },
    "specialist_recommendation": {
      "specialist": "Emergency Medicine",
      "urgency": "critical",
      "suggested_timeline": "Immediate"
    },
    "health_report": {
      "summary": "Requires immediate medical attention"
    },
    "emergency_message": "🚨 EMERGENCY: Call 911 or your local emergency number immediately. Do not delay."
  }
}
```

---

**Error Response (400 Bad Request):**

```json
{
  "success": false,
  "message": "Invalid request data",
  "error": "symptoms field is required"
}
```

**Error Response (500 Internal Server Error):**

```json
{
  "success": false,
  "message": "An internal error occurred",
  "error": "LLM service timeout"
}
```

---

## Response Structure

All responses follow a consistent envelope structure:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Request success status |
| message | string | Human-readable message |
| data | object | Response payload (null on error) |
| error | string | Error details (null on success) |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently unlimited. Production deployments may implement rate limiting per client.

---

## CORS

CORS is configured per environment:

**Development:** Allows localhost and private networks

**Production:** Allows configured domains only

---

## Timeouts

- Request timeout: 30 seconds
- LLM processing: 30 seconds maximum

---

## Example cURL Request

```bash
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "I have a mild headache and sore throat"
  }'
```

---

## Example JavaScript Request

```javascript
const response = await fetch('http://localhost:8000/api/v1/analysis', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    symptoms: 'I have a mild headache and sore throat'
  })
});

const data = await response.json();
console.log(data);
```

---

## Example Python Request

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/analysis',
    json={
        'symptoms': 'I have a mild headache and sore throat'
    }
)

data = response.json()
print(data)
```

---

## OpenAPI Documentation

Interactive API documentation available at:

**Swagger UI:**
```
http://localhost:8000/docs
```

**ReDoc:**
```
http://localhost:8000/redoc
```

---

## Important Notes

⚠️ **Medical Disclaimer:**
- HealWell provides AI-generated health information for educational and informational purposes only
- Not a replacement for professional medical advice
- Always consult qualified healthcare professionals
- In case of medical emergency, call 911 or local emergency services immediately

✅ **Production Ready:**
- Full LangGraph workflow implementation
- Real OpenAI-compatible LLM integration
- Comprehensive analysis results
- Emergency detection capability
- Type-validated requests and responses
- Environment-specific configuration
- Production performance optimizations
