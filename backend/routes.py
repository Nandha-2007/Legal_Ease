"""
LegalEase API Endpoints
Defines the FastAPI routing logic for document generation, health checks, and exports.
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response

from .models import DocumentRequest, DocumentResponse, HealthResponse, ErrorResponse
from .ai_core.gemini_generator import GeminiDocumentGenerator
from .utils.text_utils import count_words
from .utils.document_formatter import generate_docx
from .utils.pdf_generator import generate_pdf

logger = logging.getLogger("legalease.routes")
router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="API Health Status",
    description="Returns the current operational status of the LegalEase API service.",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint returning system status.
    """
    return HealthResponse(
        status="running",
        service="LegalEase API",
        version="1.0.0",
    )


@router.post(
    "/generate",
    response_model=DocumentResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input parameters"},
        500: {"model": ErrorResponse, "description": "AI generation failure or internal error"},
    },
    summary="Generate Legal Document Draft",
    description="Generates a customized, structured legal document using Google Gemini AI.",
)
async def generate_document(payload: DocumentRequest) -> DocumentResponse:
    """
    Receives document parameters, sends prompt to Gemini AI core, and returns the generated text.
    """
    logger.info(f"Received generation request for document type: {payload.document_type}")

    try:
        generator = GeminiDocumentGenerator()
        generated_text = generator.generate(
            document_type=payload.document_type,
            parties=payload.parties,
            terms=payload.terms,
            effective_date=payload.effective_date,
        )

        words = count_words(generated_text)

        return DocumentResponse(
            success=True,
            document=generated_text,
            document_type=payload.document_type,
            word_count=words,
            effective_date=payload.effective_date,
            message="Document generated successfully",
        )

    except ValueError as val_err:
        logger.warning(f"Validation error in generation request: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(val_err),
        )
    except Exception as exc:
        logger.error(f"Error during document generation: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.post(
    "/export/docx",
    summary="Export Document to DOCX",
    description="Converts provided legal document text into a Microsoft Word (.docx) file.",
)
async def export_docx(
    document_text: str = Form(...),
    document_type: str = Form("Legal Document"),
    effective_date: str = Form(""),
    parties: str = Form(""),
    logo: Optional[UploadFile] = File(None),
):
    """
    Exports legal text to DOCX binary stream with optional uploaded logo.
    """
    try:
        logo_bytes = await logo.read() if logo else None
        docx_bytes = generate_docx(
            document_text=document_text,
            document_type=document_type,
            effective_date=effective_date,
            parties=parties,
            logo_bytes=logo_bytes,
        )

        safe_filename = f"{document_type.lower().replace(' ', '_')}.docx"
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'},
        )
    except Exception as exc:
        logger.error(f"Error exporting DOCX: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export DOCX: {exc}",
        )


@router.post(
    "/export/pdf",
    summary="Export Document to PDF",
    description="Converts provided legal document text into a PDF file.",
)
async def export_pdf(
    document_text: str = Form(...),
    document_type: str = Form("Legal Document"),
    effective_date: str = Form(""),
    parties: str = Form(""),
    logo: Optional[UploadFile] = File(None),
):
    """
    Exports legal text to PDF binary stream with optional uploaded logo.
    """
    try:
        logo_bytes = await logo.read() if logo else None
        pdf_bytes = generate_pdf(
            document_text=document_text,
            document_type=document_type,
            effective_date=effective_date,
            parties=parties,
            logo_bytes=logo_bytes,
        )

        safe_filename = f"{document_type.lower().replace(' ', '_')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'},
        )
    except Exception as exc:
        logger.error(f"Error exporting PDF: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF: {exc}",
        )
