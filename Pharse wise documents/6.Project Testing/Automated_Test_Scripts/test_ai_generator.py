import pytest
from ai_core.gemini_generator import GeminiDocumentGenerator, SYSTEM_INSTRUCTION


def test_gemini_generator_prompt_builder():
    gen = GeminiDocumentGenerator()
    prompt = gen.build_prompt(
        document_type="Service Agreement",
        parties="Dev Co (Provider), Client Inc (Client)",
        terms="Milestone 1 by June; Payment of $10,000",
        dates="June 1, 2025",
    )
    assert "Service Agreement" in prompt
    assert "Dev Co" in prompt
    assert "Payment of $10,000" in prompt
    assert "June 1, 2025" in prompt
    assert "DRAFTING INSTRUCTIONS" in prompt
    assert "DO NOT invent personal information" in prompt


def test_gemini_generator_demo_mode_document_types():
    gen = GeminiDocumentGenerator(api_key="")  # Force demo mode
    assert not gen.is_configured

    # Test NDA
    ok, nda, is_demo, err = gen.generate_document(
        document_type="Non-Disclosure Agreement (NDA)",
        parties="Party 1, Party 2",
        terms="Term A; Term B",
        dates="January 1, 2025",
    )
    assert ok is True
    assert is_demo is True
    assert err is None
    assert "Non-Disclosure Agreement" in nda
    assert "RECITALS" in nda
    assert "Party 1, Party 2" in nda

    # Test Lease
    ok, lease, is_demo, err = gen.generate_document(
        document_type="Residential Lease Agreement",
        parties="Landlord John, Tenant Jane",
        terms="Rent $1,500; No pets allowed",
        dates="Feb 1, 2025",
    )
    assert ok is True
    assert "Lease Agreement" in lease
    assert "Landlord John" in lease

    # Test Employment
    ok, emp, is_demo, err = gen.generate_document(
        document_type="Employment Contract",
        parties="Corp X, Alice",
        terms="Salary $90,000; 40 hours per week",
        dates="March 1, 2025",
    )
    assert ok is True
    assert "Employment Contract" in emp
    assert "Salary $90,000" in emp
