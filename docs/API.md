# HealWell API Documentation

## Endpoint Overview

### POST /analysis
Initiates symptom analysis workflow.

**Request Body:**
```json
{
  "symptoms": "string",
  "medical_history": "string",
  "user_id": "string"
}
```

**Response:**
```json
{
  "analysis_id": "string",
  "risk_level": "string",
  "recommendations": ["string"],
  "specialists": ["string"],
  "emergency_alert": "boolean"
}
```

---

### GET /history
Retrieves user's analysis history.

**Query Parameters:**
- `user_id` (required)
- `limit` (optional, default: 20)

**Response:**
```json
{
  "analyses": [
    {
      "analysis_id": "string",
      "date": "timestamp",
      "symptoms": "string",
      "risk_level": "string"
    }
  ]
}
```

---

### POST /history
Saves medical history record.

**Request Body:**
```json
{
  "user_id": "string",
  "conditions": ["string"],
  "medications": ["string"],
  "allergies": ["string"]
}
```

**Response:**
```json
{
  "history_id": "string",
  "saved_at": "timestamp"
}
```

---

### GET /doctors
Finds nearby healthcare providers.

**Query Parameters:**
- `latitude` (required)
- `longitude` (required)
- `specialty` (optional)
- `radius_km` (optional, default: 5)

**Response:**
```json
{
  "doctors": [
    {
      "doctor_id": "string",
      "name": "string",
      "specialty": "string",
      "distance_km": "number",
      "contact": "string"
    }
  ]
}
```
