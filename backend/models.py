"""
LegalEase Data Models
Pydantic schemas for request validation and response formatting.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    """
    Request model for legal document generation.
    """
    document_type: str = Field(
        ...,
        description="Type of legal document (e.g., NDA, Employment Offer Letter, Lease Agreement)",
        example="Non-Disclosure Agreement (NDA)",
    )
    parties: str = Field(
        ...,
        description="Parties involved in the agreement with roles",
        example="Acme Corp (Disclosing Party), John Doe (Receiving Party)",
    )
    terms: str = Field(
        ...,
        description="Key terms and conditions, separated by semicolons or newlines",
        example="Duration: 2 years; Non-compete within 25 miles; Governing law: State of Delaware",
    )
    effective_date: str = Field(
        ...,
        description="Effective date of the document in YYYY-MM-DD or readable format",
        example="2026-10-01",
    )

    @field_validator("document_type", "parties", "terms", "effective_date")
    @classmethod
    def check_non_empty(cls, value: str, info) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError(f"Field '{info.field_name}' must not be empty.")
        return trimmed


class DocumentResponse(BaseModel):
    """
    Response model containing the generated legal document and metadata.
    """
    success: bool = True
    document: str = Field(..., description="Full text of the generated legal document")
    document_type: Optional[str] = None
    word_count: Optional[int] = None
    effective_date: Optional[str] = None
    message: Optional[str] = "Document generated successfully"


class HealthResponse(BaseModel):
    """
    Health check response model.
    """
    status: str = "running"
    service: str = "LegalEase API"
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    success: bool = False
    error: str = Field(..., description="Error summary")
    detail: Optional[str] = Field(None, description="Detailed error description")
