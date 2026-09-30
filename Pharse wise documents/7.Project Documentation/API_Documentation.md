# REST API Documentation — LegalEase

The LegalEase REST API provides programmatic access for automated legal document drafting.

---

## 1. Base URL & Interactive Documentation
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 2. API Endpoints

### 2.1 Root Health & Info
- **URL**: `GET /`
- **Description**: Returns general service status.
- **Response**: `200 OK`
```json
{
  "message": "Welcome to LegalEase AI Legal Document Generator API",
  "status": "online",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2.2 Health Check & AI Mode Status
- **URL**: `GET /health`
- **Description**: Returns operational status, model configuration, and whether Demo Mode is currently active.
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "gemini_configured": false,
  "model": "gemini-1.5-pro",
  "demo_mode": true
}
```

---

### 2.3 Generate Legal Document
- **URL**: `POST /generate`
- **Headers**: `Content-Type: application/json`
- **Request Body Parameters**:
  - `document_type` *(string, required)*: Name of agreement (e.g. "Non-Disclosure Agreement (NDA)").
  - `parties` *(string, required)*: Involved stakeholders and roles.
  - `terms` *(string, required)*: Semicolon-delimited conditions.
  - `dates` *(string, required)*: Effective date string.

#### Example Request:
```bash
curl -X POST "http://127.0.0.1:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "Freelance Work Contract",
       "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
       "terms": "Delivery by May 15, 2025; Payment of $4,500 within 7 days; Confidentiality strictly preserved",
       "dates": "April 15, 2025"
     }'
```

#### Example Success Response (`200 OK`):
```json
{
  "success": true,
  "document_type": "Freelance Work Contract",
  "content": "## Freelance Work Contract\n\nThis Freelance Work Contract is made as of April 15, 2025...",
  "is_demo": true,
  "error": null,
  "message": "Document generated successfully in Demo Mode."
}
```

#### Validation Error (`422 Unprocessable Entity` / `400 Bad Request`):
```json
{
  "detail": "Document type cannot be empty after sanitization."
}
```
