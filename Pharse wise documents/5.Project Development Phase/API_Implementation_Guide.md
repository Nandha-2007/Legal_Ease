# 2. API & AI Core Implementation Guide — LegalEase

This document details the internal architecture and implementation logic of the FastAPI backend and AI Core.

---

## 1. FastAPI Application Bootstrap (`main.py`)
- Configures global application metadata (Title, Version, Docs URL).
- Implements `CORSMiddleware` with permissive origins for local Streamlit communication.
- Registers API routing modules from `routes.py`.
- Exposes root route `GET /` and health check `GET /health`.

---

## 2. Request Handling & Route Logic (`routes.py`)
```python
@router.post("/generate", response_model=DocumentResponse, tags=["Document Generation"])
def generate_document(request: DocumentRequest):
    # 1. Sanitize incoming inputs
    clean_doc_type = sanitize_text(request.document_type)
    clean_parties = sanitize_text(request.parties)
    clean_terms = sanitize_text(request.terms)
    clean_dates = sanitize_text(request.dates)

    # 2. Validate non-empty after sanitization
    if not clean_doc_type or not clean_parties or not clean_terms or not clean_dates:
        raise HTTPException(status_code=400, detail="Required fields cannot be empty.")

    # 3. Call AI / Demo generation engine
    success, content, is_demo, error_msg = generator.generate_document(
        document_type=clean_doc_type,
        parties=clean_parties,
        terms=clean_terms,
        dates=clean_dates,
    )
    ...
```

---

## 3. Gemini Prompt Engineering & Anti-Hallucination (`ai_core/gemini_generator.py`)
The generator applies a strict legal drafting instruction prompt:
- **System Instruction**: Explicitly forbids fabricating legal citations, court case law, or personal identifying data.
- **Missing Information**: Requires square-bracket placeholders like `[Address]`, `[City, State, Zip Code]`, and `[Jurisdiction]`.
- **Semicolon Expansion**: Semicolon-delimited terms are extracted, enumerated, and embedded into formal contract provisions.

---

## 4. Deterministic Demo Mode Engine
When `GEMINI_API_KEY` is not present, `_generate_demo_document()` triggers:
- Analyzes document type keywords (`nda`, `employment`, `lease`, `freelance`, `service`).
- Injects user parties, terms, and effective date into a formal contract framework.
- Generates realistic preambles, recitals, numbered terms, and a 2-column signature block.
- Sets `is_demo = True` to maintain full transparency.
