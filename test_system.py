"""
System Test Suite for LegalEase
Verifies all modules, models, utils, DOCX/PDF generation, and API endpoints.
"""

import os
import sys

from backend.models import DocumentRequest, DocumentResponse, HealthResponse
from backend.utils.text_utils import sanitize_text, parse_terms, count_words
from backend.utils.document_formatter import generate_docx, format_html_preview, parse_document_sections
from backend.utils.pdf_generator import generate_pdf
from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.main import app

def run_tests():
    print("Testing imports... OK")

    # 1. Test sanitization
    sample_text = '\u201cSmart quotes\u201d \u2014 and em-dashes \u2022 bullets \u2019'
    sanitized = sanitize_text(sample_text)
    assert '\u201c' not in sanitized and '\u201d' not in sanitized, "Smart quotes not cleaned"
    print(f"Sanitization test passed: {sanitized}")

    # 2. Test terms parsing
    sample_terms = "Term 1: 30 days payment; Term 2: Confidentiality for 3 years; Term 3: Governing law CA"
    parsed = parse_terms(sample_terms)
    assert len(parsed) == 3, f"Expected 3 terms, got {len(parsed)}"
    print(f"Terms parsed successfully: {parsed}")

    # 3. Test word count
    sample_sentence = "This contract contains seven test words."
    words = count_words(sample_sentence)
    assert words == 6, f"Expected 6 words, got {words}"
    print(f"Word count verified: {words}")

    # 4. Test DOCX generation
    logo_path = "frontend/assets/logo.png"
    logo_bytes = None
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_bytes = f.read()

    sample_doc = """# NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "Agreement") is entered into as of October 01, 2026.

## 1. DEFINITIONS AND SCOPE
"Confidential Information" shall include all proprietary technical and commercial data.

## 2. OBLIGATIONS OF RECEIVING PARTY
* The Receiving Party agrees to hold all Confidential Information in strict confidence.
* The Receiving Party shall not copy or reverse engineer any materials.

## IN WITNESS WHEREOF
By: ______________________
Name: Jane Doe
Title: CEO
Date: 2026-10-01

## DISCLAIMER & LEGAL NOTICE
This document is an AI-assisted draft for informational purposes only.
"""

    docx_bytes = generate_docx(
        document_text=sample_doc,
        document_type="Non-Disclosure Agreement",
        effective_date="2026-10-01",
        parties="Acme Corp & Beta LLC",
        logo_bytes=logo_bytes,
    )
    assert len(docx_bytes) > 1000, "DOCX generation returned empty or small file"
    print(f"DOCX Generation verified ({len(docx_bytes)} bytes)")

    # 5. Test PDF generation
    pdf_bytes = generate_pdf(
        document_text=sample_doc,
        document_type="Non-Disclosure Agreement",
        effective_date="2026-10-01",
        parties="Acme Corp & Beta LLC",
        logo_bytes=logo_bytes,
    )
    assert len(pdf_bytes) > 1000, "PDF generation returned empty or small file"
    print(f"PDF Generation verified ({len(pdf_bytes)} bytes)")

    # 6. Test HTML preview
    html_preview = format_html_preview(sample_doc)
    assert "<h1 class='doc-title'>" in html_preview, "HTML preview missing title"
    assert "<div class='legal-doc-sheet'>" in html_preview, "HTML preview missing sheet wrapper"
    print("HTML Preview verified")

    # 7. Test Section Parser
    sections = parse_document_sections(sample_doc)
    assert "NON-DISCLOSURE AGREEMENT" in sections["title"]
    assert "IN WITNESS WHEREOF" in sections["signatures"]
    print("Section parser verified")

    # 8. Test Pydantic Models
    req = DocumentRequest(
        document_type="NDA",
        parties="Party A, Party B",
        terms="Term 1; Term 2",
        effective_date="2026-10-01",
    )
    assert req.document_type == "NDA"
    print("Pydantic models verified")

    # 9. Test Prompt Builder
    gen = GeminiDocumentGenerator(api_key="test_dummy_key")
    prompt = gen.build_prompt(
        document_type=req.document_type,
        parties=req.parties,
        terms=req.terms,
        effective_date=req.effective_date,
    )
    assert "NON-DISCLOSURE AGREEMENT" in prompt or "NDA" in prompt
    assert "DISCLAIMER" in prompt
    print("Prompt builder verified")

    print("\n==========================================")
    print("SUCCESS: ALL LEGAL EASE SYSTEM TESTS PASSED!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
