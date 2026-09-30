# 1. Project Development Overview — LegalEase

This document provides a comprehensive technical overview of the development phase, detailing the modular source code architecture, package dependencies, and file relationships.

---

## 1. Modular Source Code Architecture

LegalEase follows strict separation of concerns across presentation, routing, data contracts, AI processing, document compilation, and utilities:

```text
5.Project Development Phase/
├── app.py                      # Streamlit frontend presentation & state management
├── main.py                     # FastAPI application entry point, CORS, and server bootstrap
├── routes.py                   # REST routing definitions (/generate, /health)
├── requirements.txt            # Production dependencies specification
├── .env.example                # Environment variables template
├── .gitignore                  # Git exclusions
│
├── ai_core/                    # Artificial Intelligence & drafting engine
│   ├── __init__.py
│   └── gemini_generator.py     # Gemini client, anti-hallucination prompt, & demo mode
│
├── document_utils/             # Document formatting and binary compilation suite
│   ├── __init__.py
│   ├── docx_generator.py       # Microsoft Word (.docx) generator with tables & footers
│   ├── pdf_generator.py        # PDF generator with fpdf2, page numbering & headers
│   ├── txt_generator.py        # Clean UTF-8 plain text formatter
│   └── formatter.py            # Dark-theme HTML previewer & semicolon terms parser
│
├── models/                     # Data contracts & validation
│   ├── __init__.py
│   └── schemas.py              # Pydantic schemas (DocumentRequest, DocumentResponse)
│
├── utils/                      # Utilities and configuration
│   ├── __init__.py
│   ├── sanitizer.py            # Text sanitization, Unicode normalizer, XSS mitigation
│   └── config.py               # Centralized configuration & environment loader
│
└── assets/                     # Brand visual assets
    ├── generate_logos.py       # Script to programmatically generate logos
    └── logo/
        ├── logo.png            # Standard logo for Word/PDF
        └── inverseLogo.png     # Inverse logo for dark theme
```

---

## 2. Key Modules & Functional Responsibilities

| Module | Core File | Key Responsibilities |
| :--- | :--- | :--- |
| **Frontend** | `app.py` | Renders input forms, presets, dark-card preview, in-line editor, and download triggers. |
| **Backend API** | `main.py`, `routes.py` | Receives JSON, executes sanitization, invokes AI engine, handles HTTP error codes. |
| **AI Core** | `gemini_generator.py` | Builds legal drafting prompts, communicates with Gemini 1.5 Pro, houses Demo Mode fallback. |
| **DOCX Exporter** | `docx_generator.py` | Compiles Microsoft Word files with 1-inch margins, Times New Roman, and signature tables. |
| **PDF Exporter** | `pdf_generator.py` | Compiles multi-page PDFs using `fpdf2` with running headers, footers, and page numbers. |
| **TXT Exporter** | `txt_generator.py` | Produces clean UTF-8 plain text with ASCII section delimiters and legal disclaimers. |
| **HTML Formatter** | `formatter.py` | Transforms markdown headers, bullets, and signatures into dark-card semantic HTML. |
| **Data Models** | `schemas.py` | Pydantic models with field-level whitespace trimming and character-length constraints. |
| **Sanitizer** | `sanitizer.py` | Normalizes typographic quotes, removes control characters, strips executable scripts. |
| **Configuration**| `config.py` | Centralizes environment variables, API keys, server URLs, and asset paths. |
