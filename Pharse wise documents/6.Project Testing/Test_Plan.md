# 1. Software Test Plan (STP) — LegalEase

This document establishes the test strategy, scope, environment, and verification methodology for the LegalEase platform.

---

## 1. Testing Objectives
- Verify that FastAPI endpoints (`/`, `/health`, `/generate`) respond accurately and conform to OpenAPI data models.
- Validate that Pydantic schemas properly reject malformed or blank inputs.
- Ensure the sanitization pipeline neutralizes XSS vectors, smart quotes, and control characters without corrupting legal punctuation.
- Verify that document generation operates reliably in both live Gemini mode and deterministic Demo Mode.
- Validate that TXT, DOCX, and PDF exporters generate structurally valid, non-empty binaries across single-page and multi-page scenarios.

---

## 2. Test Scope & Categorization

```
                          ┌── test_root_endpoint
       ┌── API Testing ───┼── test_health_endpoint
       │                  ├── test_generate_valid_request
       │                  ├── test_generate_empty_inputs_validation
       │                  └── test_generate_demo_mode_indicator
       │
       │                  ┌── test_sanitize_text_normalizes_typographic_quotes
       ├── Sanitization ──┼── test_sanitize_text_strips_script_injection
       │   & Parsing      ├── test_sanitize_text_preserves_legal_brackets
TESTS ─┤                  ├── test_parse_terms_semicolon_separated
       │                  └── test_parse_terms_handles_bullets_and_newlines
       │
       │                  ┌── test_txt_export
       ├── Exporters ─────┼── test_docx_export (Paragraphs & tables)
       │                  ├── test_pdf_export (%PDF- header)
       │                  └── test_pdf_multipage_handling (Auto page breaks)
       │
       └── AI Core ───────┬── test_gemini_generator_prompt_builder
                          └── test_gemini_generator_demo_mode_document_types
```

---

## 3. Test Environment Specifications
- **Operating System**: Windows 11 / x64
- **Python Runtime**: Python 3.13.14 (Virtual Environment `.\venv`)
- **Testing Framework**: `pytest` 9.1.1, `Starlette TestClient`
- **Execution Command**: `.\venv\Scripts\pytest -v`
