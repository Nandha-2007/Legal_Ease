# 1. Work Breakdown Structure (WBS) — LegalEase

This document presents the hierarchical Work Breakdown Structure (WBS) for the end-to-end development of LegalEase, directly aligned with the project milestones established in `LegalEase.pdf`.

---

## 1. WBS Tree Diagram

```
1.0 LegalEase Project
├── 1.1 Milestone 1: Model Selection & System Architecture
│   ├── 1.1.1 Generative AI Model Evaluation (Gemini 1.5 Pro selection)
│   ├── 1.1.2 High-Level Architecture Definition (FastAPI + Streamlit + Exporters)
│   └── 1.1.3 Environment Setup (Python 3.13 venv, dependency baseline)
│
├── 1.2 Milestone 2: Core Functionalities Development
│   ├── 1.2.1 Text Sanitization Engine (Unicode, smart quotes, XSS neutralization)
│   ├── 1.2.2 Plain Text (.TXT) Formatting Module
│   ├── 1.2.3 Microsoft Word (.DOCX) Generation Module (python-docx)
│   ├── 1.2.4 PDF Generation Module (fpdf2 with headers & footers)
│   └── 1.2.5 Brand Assets Generation (logo.png & inverseLogo.png)
│
├── 1.3 Milestone 3: FastAPI Backend & API Logic
│   ├── 1.3.1 Pydantic Request & Response Data Contracts (models/schemas.py)
│   ├── 1.3.2 REST API Routing & Root/Health Endpoints (main.py, routes.py)
│   ├── 1.3.3 Gemini AI Prompt Engineering & Client Setup (ai_core/gemini_generator.py)
│   └── 1.3.4 Deterministic Fallback Engine for Zero-Key Demo Mode
│
├── 1.4 Milestone 4: Streamlit Frontend Development
│   ├── 1.4.1 Page Layout & Custom Styling (Centered layout, dark cards)
│   ├── 1.4.2 User Input Form (Type, Parties, Semicolon Terms, Date)
│   ├── 1.4.3 Sample Scenario Quick-Loader Presets
│   ├── 1.4.4 Dynamic Semantic HTML Document Preview
│   ├── 1.4.5 In-Browser Live Text Editor & State Management
│   └── 1.4.6 Multi-Format Download Action Hub
│
├── 1.5 Milestone 5: Verification & Testing
│   ├── 1.5.1 API Endpoint & Schema Validation Test Suite
│   ├── 1.5.2 Text Sanitizer & HTML Formatter Test Suite
│   ├── 1.5.3 Multi-Format Exporter Test Suite (.txt, .docx, .pdf)
│   ├── 1.5.4 AI Core Prompt & Demo Mode Test Suite
│   └── 1.5.5 End-to-End Live Integration Verification
│
└── 1.6 Milestone 6: Deployment & Documentation
    ├── 1.6.1 Comprehensive Project README.md & Setup Instructions
    ├── 1.6.2 Project Lifecycle Repository Structuring (Phases 1 - 8)
    └── 1.6.3 Final Quality Assurance & Demonstration Packaging
```

---

## 2. Activity & Work Package Dictionary

| WBS Code | Work Package | Responsible Role | Deliverable |
| :--- | :--- | :--- | :--- |
| **1.1.1** | Model Selection | AI Engineer | Model selection report (Gemini 1.5 Pro). |
| **1.1.2** | System Architecture | Lead Architect | Architecture diagrams, component specs. |
| **1.2.1** | Sanitization Engine | Backend Engineer | `utils/sanitizer.py` with 100% regex coverage. |
| **1.2.3** | DOCX Formatter | Document Specialist | `document_utils/docx_generator.py`. |
| **1.2.4** | PDF Formatter | Document Specialist | `document_utils/pdf_generator.py`. |
| **1.3.2** | FastAPI Endpoints | Backend Engineer | `main.py` and `routes.py` with `/generate`. |
| **1.3.3** | Prompt Builder | AI Engineer | `ai_core/gemini_generator.py` prompt system. |
| **1.4.1** | Streamlit UI | Frontend Engineer | `app.py` with responsive dark-theme design. |
| **1.5.1** | Pytest Automation | QA Engineer | 17 passing automated unit/integration tests. |
| **1.6.1** | Documentation | Technical Writer | Full `README.md` and lifecycle documentation. |
