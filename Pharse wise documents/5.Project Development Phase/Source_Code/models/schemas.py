from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    """Incoming request model for legal document generation."""
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


class DocumentResponse(BaseModel):
    """Response model for document generation."""
    success: bool = Field(..., description="Whether generation succeeded")
    document_type: str = Field(..., description="Document type generated")
    content: str = Field(..., description="Generated legal document text")
    is_demo: bool = Field(default=False, description="True if generated in fallback/demo mode")
    error: Optional[str] = Field(default=None, description="Error message if generation failed")
    message: Optional[str] = Field(default=None, description="Human-readable status or guidance note")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    gemini_configured: bool
    model: str
    demo_mode: bool
