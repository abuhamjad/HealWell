# HealWell API Reference

## Overview
HealWell API v0.7.1 provides REST endpoints for health analysis and medical guidance. Base URL: `/api/v1`

---

## Endpoints

### POST /api/v1/analysis
**Purpose**: Perform health analysis on patient symptoms

**Request**:
```
POST /api/v1/analysis
Content-Type: application/json

{
  "symptoms": "I have a persistent cough, fever of 38.5°C for 3 days",
  "user_id": "user_123" (optional)
}
```

**Parameters**:
- `symptoms` (string, required): Patient symptom description
- `user_id` (string, optional): User identifier

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Health analysis created successfully",
  "data": {
    "analysis_id": "588b1d98-3fc6-463d-99bb-235649ded7bb",
    "risk_level": "moderate",
    "confidence": 82.0,
    "specialist": "General Physician",
    "emergency": false
  },
  "errors": null
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "message": "Invalid request data",
  "data": null,
  "errors": [
    {
      "field": "symptoms",
      "message": "symptoms is required"
    }
  ]
}
```

**Service Flow**:
1. AnalysisService.analyze()
2. AnalysisWorkflow.execute()
3. LangGraph agents process
4. AnalysisResult returned
5. Transformed to API response

**Latency**: 3-5 seconds (dominated by LLM call)

**Status**: Operational (v0.7.1)

---

### GET /api/v1/history
**Purpose**: Retrieve user's analysis history

**Request**:
```
GET /api/v1/history?user_id=user_123&limit=20
```

**Query Parameters**:
- `user_id` (string, required): User identifier
- `limit` (integer, optional, default=20): Number of records

**Response** (200 OK):
```json
{
  "success": true,
  "message": "History retrieved successfully",
  "data": {
    "analyses": [
      {
        "analysis_id": "...",
        "timestamp": "2024-07-24T10:30:00Z",
        "symptoms": "...",
        "risk_level": "moderate"
      }
    ],
    "total": 45
  },
  "errors": null
}
```

**Status**: Placeholder (returns mock data, database TBD)

---

### POST /api/v1/history
**Purpose**: Save medical history for user

**Request**:
```
POST /api/v1/history
Content-Type: application/json

{
  "user_id": "user_123",
  "medical_history": "No chronic conditions",
  "medications": ["vitamin D"],
  "allergies": ["penicillin"]
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Medical history saved successfully",
  "data": {
    "status": "saved"
  },
  "errors": null
}
```

**Status**: Placeholder (database TBD)

---

### GET /api/v1/doctors
**Purpose**: Find nearby healthcare providers

**Request**:
```
GET /api/v1/doctors?latitude=40.7128&longitude=-74.0060&specialty=General%20Physician&radius_km=5
```

**Query Parameters**:
- `latitude` (float, optional): Patient latitude
- `longitude` (float, optional): Patient longitude
- `specialty` (string, optional): Medical specialty
- `radius_km` (float, optional, default=5): Search radius

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Nearby doctors found successfully",
  "data": {
    "doctors": [
      {
        "id": "doctor_001",
        "name": "Dr. Sarah Chen",
        "specialty": "General Physician",
        "hospital": "Apollo Hospitals",
        "distance": "0.8 km",
        "rating": 4.9,
        "available": true
      }
    ],
    "count": 2
  },
  "errors": null
}
```

**Status**: Placeholder (geolocation TBD)

---

## Health Endpoints

### GET /
**Purpose**: API health check and info

**Response** (200 OK):
```json
{
  "success": true,
  "message": "HealWell API is running",
  "data": {
    "api": "HealWell API",
    "version": "0.7.1",
    "status": "running"
  },
  "errors": null
}
```

---

### GET /health
**Purpose**: Health check

**Response** (200 OK):
```json
{
  "success": true,
  "message": "API is healthy",
  "data": {
    "status": "healthy",
    "environment": "development"
  },
  "errors": null
}
```

---

## API Documentation

### OpenAPI/Swagger
- Available at: `http://localhost:8000/docs`
- ReDoc at: `http://localhost:8000/redoc`

### Authentication
- Not implemented (v0.7.1)
- Planned for v0.9+

### Rate Limiting
- Not implemented (v0.7.1)
- Planned for v0.9+

### CORS
- Configured for development
- Strict validation in production
- Header: `Access-Control-Allow-Origin`

### Error Codes

| Code | Message | Cause |
|------|---------|-------|
| 200 | Success | Operation succeeded |
| 400 | Bad Request | Invalid input data |
| 422 | Validation Error | Schema validation failed |
| 500 | Internal Error | Server error |

---

## Response Format

All API responses use standardized `ApiResponse` format:

```python
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "errors": array | null
}
```

- **success**: Operation result (true/false)
- **message**: Human-readable message
- **data**: Response data (null if error)
- **errors**: Error details (null if success)

---

## Status Indicators

| Endpoint | Status | Maturity | Notes |
|----------|--------|----------|-------|
| POST /analysis | ✅ Operational | Production | Real SymptomAgent (v0.7.1) |
| GET /history | ⚠️ Placeholder | Mock | Mock data returned |
| POST /history | ⚠️ Placeholder | Mock | No persistence |
| GET /doctors | ⚠️ Placeholder | Mock | Mock data returned |

---

## Usage Examples

### Example 1: Analyze Symptoms
```bash
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "I have a persistent cough and fever"
  }'
```

### Example 2: With User ID
```bash
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "Headache and neck stiffness",
    "user_id": "user_123"
  }'
```

### Example 3: Get History
```bash
curl http://localhost:8000/api/v1/history?user_id=user_123&limit=10
```

---

## Future Enhancements (v0.8+)

- Authentication & Authorization
- Rate limiting
- Request/Response logging
- Pagination for history
- Advanced filtering
- PDF report export
- Medical history lookup
- Doctor appointment booking
