# 3. Technology Stack Selection & Trade-Off Analysis — LegalEase

This document provides technical justifications and trade-off evaluations for the software components, frameworks, and libraries selected for LegalEase.

---

## 1. Architectural Stack Overview

```
Layer                   Technology                     Version / Baseline
─────────────────────────────────────────────────────────────────────────────
Frontend Framework      Streamlit                      >= 1.32.0
Backend REST Server     FastAPI + Uvicorn              >= 0.110.0 / >= 0.28.0
Data Validation         Pydantic                       >= 2.6.0
Generative AI SDK       Google Generative AI SDK       >= 0.8.0
AI Model (Default)      Google Gemini 1.5 Pro          gemini-1.5-pro
DOCX Export Engine      python-docx                    >= 1.1.0
PDF Export Engine       fpdf2                          >= 2.7.8
Image & Logo Processing Pillow (PIL)                   >= 10.2.0
Environment Management  python-dotenv                  >= 1.0.1
Automated Test Engine   pytest                         >= 8.0.0
HTTP Client             requests / httpx               >= 2.31.0 / >= 0.27.0
─────────────────────────────────────────────────────────────────────────────
```

---

## 2. Component Trade-Off Analysis

### A. Frontend: Streamlit vs. React / Vue
- **Why Streamlit Won**:
  - Streamlit enables rapid development of reactive, Python-native interfaces without requiring separate JavaScript toolchains (Node, npm, Webpack).
  - Native support for file download buttons (`st.download_button`), image uploads (`st.file_uploader`), and state persistence (`st.session_state`).
  - Seamless layout configuration matching the centered single-column legal aesthetic required by the project specification.

### B. Backend: FastAPI vs. Flask vs. Django
- **Why FastAPI Won**:
  - High performance built on Starlette and Asynchronous Server Gateway Interface (ASGI).
  - Native integration with Pydantic for automated request parsing, type checking, and schema documentation.
  - Automatic generation of interactive OpenAPI Swagger documentation at `/docs` and ReDoc at `/redoc`.
  - Lightweight footprint compared to monolithic frameworks like Django.

### C. Generative AI Engine: Google Gemini 1.5 Pro vs. OpenAI GPT-4 vs. Local LLMs
- **Why Gemini 1.5 Pro Won**:
  - Specifically designated in project specification `LegalEase.pdf`.
  - Up to 1-million-token context window capable of ingesting extensive legal clauses and precedent texts.
  - Superior reasoning in formal legal tone, structured clause generation, and adherence to negative prompt constraints (anti-hallucination).
  - Fast response speed with low latency for interactive web applications.

### D. Word Export Engine: python-docx
- **Why python-docx Won**:
  - Python's premier library for programmatic `.docx` creation.
  - Native support for XML-based page numbering fields (`w:fldChar` / `w:instrText` = `PAGE`).
  - Precise control over paragraph styling, indentation, table alignment, and image embedding.

### E. PDF Export Engine: fpdf2 vs. ReportLab
- **Why fpdf2 Won**:
  - Maintained, modern, pure-Python PDF generator with zero external C-dependencies.
  - Clean subclassing model (`class LegalPDF(FPDF)`) providing fine-grained control over multi-page running headers and running footers with total page alias (`Page {nb}`).
  - Significantly simpler and more maintainable than ReportLab's complex canvas and platypus flowables.
