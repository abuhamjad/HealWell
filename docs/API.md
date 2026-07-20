# HealWell API Documentation

## Status
✅ **Milestone v0.3** - API foundation established with placeholder endpoints.

## Base URL
```
http://localhost:8000
```

## API Versioning
All business logic endpoints use `/api/v1/` prefix.

## Health & Information Endpoints

### GET /
API root endpoint with version and status information.

**Response (200 OK):**
```json
{
  "message": "HealWell API",
  "version": "0.1.0",
  "status": "running"
}
```

---

### GET /health
Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

## Analysis Endpoints

### POST /api/v1/analysis
Initiates symptom analysis workflow.

**Currently returns placeholder response.**

**Request Body:**
```json
{
  "symptoms": "string",
  "user_id": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "analysis_id": "analysis_001",
  "risk_level": "moderate",
  "confidence": 87.5,
  "specialist": "General Practitioner",
  "emergency": false,
  "status": "success"
}
```

---

## History Endpoints

### GET /api/v1/history
Retrieves user's analysis history.

**Currently returns placeholder response.**

**Query Parameters:**
- `user_id` (optional)
- `limit` (optional, default: 20)

**Response (200 OK):**
```json
{
  "analyses": [
    {
      "id": "analysis_001",
      "user_id": "user_123",
      "date": "2026-07-18",
      "symptoms": "Headache with light sensitivity",
      "risk_level": "moderate",
      "specialist": "Neurologist"
    }
  ],
  "count": 1
}
```

---

### POST /api/v1/history
Saves or updates user medical history.

**Currently returns placeholder response.**

**Request Body:**
```json
{
  "user_id": "string",
  "conditions": ["string (optional)"],
  "medications": ["string (optional)"],
  "allergies": ["string (optional)"]
}
```

**Response (200 OK):**
```json
{
  "history_id": "history_001",
  "user_id": "user_123",
  "saved_at": "2026-07-20T10:30:00Z",
  "status": "success"
}
```

---

## Doctor Endpoints

### GET /api/v1/doctors
Finds nearby healthcare providers.

**Currently returns placeholder response.**

**Query Parameters:**
- `latitude` (optional)
- `longitude` (optional)
- `specialty` (optional)
- `radius_km` (optional, default: 5.0)

**Response (200 OK):**
```json
{
  "doctors": [
    {
      "id": "doctor_001",
      "name": "Dr. Sarah Chen",
      "specialty": "General Physician",
      "hospital": "Apollo Hospitals",
      "distance": "0.8 km",
      "rating": 4.9,
      "available": true
    },
    {
      "id": "doctor_002",
      "name": "Dr. Rajesh Kumar",
      "specialty": "Internal Medicine",
      "hospital": "Fortis Healthcare",
      "distance": "1.4 km",
      "rating": 4.7,
      "available": true
    }
  ],
  "count": 2
}
```

---

## Important Notes

⚠️ **Current State:**
- All endpoints return placeholder/mock responses
- No business logic is implemented
- No database integration
- No AI or LangGraph processing
- No authentication required
- For Milestone v0.3 only

✅ **Available:**
- CORS configured for frontend at http://localhost:5173
- Automatic API documentation at /docs and /redoc
- Type validation via Pydantic schemas
- Environment configuration support
