# 3. Data Models & API Design Specification — LegalEase

This document details the Pydantic data models, REST endpoint definitions, HTTP status codes, and JSON schemas for LegalEase.

---

## 1. Pydantic Schemas

### A. DocumentRequest
```python
class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        description="Type of legal document (e.g. NDA, Employment Contract)",
        min_length=2,
        max_length=150,
        examples=["Non-Disclosure Agreement (NDA)"]
    )
    parties: str = Field(
        ...,
        description="Parties involved in the agreement with roles",
        min_length=2,
        max_length=2000,
        examples=["Jane Doe (Service Provider), TechNova Inc. (Client)"]
    )
    terms: str = Field(
        ...,
        description="Clauses, rules, or conditions (semicolon-separated)",
        min_length=2,
        max_length=10000,
        examples=["Payment within 30 days; Confidentiality must be maintained; 15 days notice"]
    )
    dates: str = Field(
        ...,
        description="Effective date or key dates",
        min_length=2,
        max_length=200,
        examples=["April 15, 2025"]
    )

    @field_validator("document_type", "parties", "terms", "dates")
    @classmethod
    def check_not_blank(cls, v: str) -> str:
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("Field cannot be empty or contain only whitespace.")
        return v_stripped
```

### B. DocumentResponse
```python
class DocumentResponse(BaseModel):
    success: bool = Field(..., description="Whether generation succeeded")
    document_type: str = Field(..., description="Document type generated")
    content: str = Field(..., description="Generated legal document text")
    is_demo: bool = Field(default=False, description="True if generated in fallback/demo mode")
    error: Optional[str] = Field(default=None, description="Error message if generation failed")
    message: Optional[str] = Field(default=None, description="Human-readable status or guidance note")
```

### C. HealthResponse
```python
class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    model: str
    demo_mode: bool
```

---

## 2. REST Endpoints Specification

### Endpoint 1: `GET /`
- **Purpose**: Root service status check and navigation guide.
- **Response**: `200 OK`
```json
{
  "message": "Welcome to LegalEase AI Legal Document Generator API",
  "status": "online",
  "docs": "/docs",
  "health": "/health"
}
```

### Endpoint 2: `GET /health`
- **Purpose**: Health check verifying AI configuration and operational status.
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "gemini_configured": false,
  "model": "gemini-1.5-pro",
  "demo_mode": true
}
```

### Endpoint 3: `POST /generate`
- **Purpose**: Accepts document parameters, sanitizes inputs, invokes Gemini or Demo Mode generator, and returns drafted contract.
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Delivery by May 15, 2025; Payment of $4,500 within 7 days; Confidentiality strictly preserved",
  "dates": "April 15, 2025"
}
```
- **Success Response**: `200 OK`
```json
{
  "success": true,
  "document_type": "Freelance Work Contract",
  "content": "## Freelance Work Contract\n\nThis Agreement is made as of April 15, 2025...",
  "is_demo": true,
  "error": null,
  "message": "Document generated successfully in Demo Mode."
}
```
- **Validation Failure Response**: `422 Unprocessable Entity` or `400 Bad Request`
```json
{
  "detail": "Document type cannot be empty after sanitization."
}
```
- **Server / AI Failure Response**: `500 Internal Server Error`
```json
{
  "detail": "Document generation failed. Please check your API configuration or try again."
}
```
