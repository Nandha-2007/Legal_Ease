import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import DocumentRequest, DocumentResponse, HealthResponse
from ai_core.gemini_generator import GeminiDocumentGenerator
from utils.sanitizer import sanitize_text
from utils.config import GEMINI_MODEL, is_gemini_configured

logger = logging.getLogger("legalease.routes")
router = APIRouter()

# Initialize document generator instance
generator = GeminiDocumentGenerator()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Verify backend status and AI configuration."""
    configured = is_gemini_configured()
    return HealthResponse(
        status="ok",
        gemini_configured=configured,
        model=GEMINI_MODEL,
        demo_mode=not configured,
    )


@router.post("/generate", response_model=DocumentResponse, tags=["Document Generation"])
def generate_document(request: DocumentRequest):
    """Process legal document generation request.
    
    1. Validates and sanitizes incoming fields.
    2. Calls Gemini AI or fallback Demo Mode generator.
    3. Returns structured document content.
    """
    # 1. Sanitize incoming inputs
    clean_doc_type = sanitize_text(request.document_type)
    clean_parties = sanitize_text(request.parties)
    clean_terms = sanitize_text(request.terms)
    clean_dates = sanitize_text(request.dates)

    # 2. Validate non-empty after sanitization
    if not clean_doc_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document type cannot be empty after sanitization.",
        )
    if not clean_parties:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parties involved cannot be empty after sanitization.",
        )
    if not clean_terms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Terms and conditions cannot be empty after sanitization.",
        )
    if not clean_dates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Effective date cannot be empty after sanitization.",
        )

    # 3. Call AI / Demo generation engine
    success, content, is_demo, error_msg = generator.generate_document(
        document_type=clean_doc_type,
        parties=clean_parties,
        terms=clean_terms,
        dates=clean_dates,
    )

    if not success:
        logger.error(f"Generation failure: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg or "Failed to generate legal document. Please try again.",
        )

    return DocumentResponse(
        success=True,
        document_type=clean_doc_type,
        content=content,
        is_demo=is_demo,
        message="Document generated successfully in Demo Mode." if is_demo else "Document generated successfully via Gemini AI.",
    )
