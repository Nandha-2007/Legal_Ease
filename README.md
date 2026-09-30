# LegalEase — AI-Powered Legal Document Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LegalEase** is a full-stack, AI-powered web platform designed to streamline and automate the drafting of customizable, professional-grade legal agreements and contracts. Combining a **FastAPI** backend with **Google Gemini Generative AI** and an intuitive **Streamlit** user interface, LegalEase enables entrepreneurs, freelancers, landlords, and organizations to generate structured, formatted legal drafts in seconds.

---

## ⚖️ Important Legal Disclaimer

> **IMPORTANT:** LegalEase provides AI-generated draft documents and legal information for general informational and document-drafting purposes only. It **does not constitute legal advice** and should not replace consultation with or review by a qualified legal professional or licensed attorney in your jurisdiction.

---

## 🌟 Key Features

1. **Multi-Type Legal Document Drafting:**
   - Non-Disclosure Agreements (NDA)
   - Employment Contracts
   - Freelance Work Contracts
   - Service Agreements
   - Residential & Commercial Lease Agreements
   - Employment Offer Letters
   - General Business Agreements & Custom Documents

2. **Custom Input Specification:**
   - Dynamic party specification with explicit contractual roles.
   - Semicolon-separated terms automatically parsed into numbered/bulleted legal clauses.
   - Effective date picker with standard legal date formatting.

3. **Google Gemini Generative AI Core:**
   - Dedicated structured prompt engineering with strict anti-hallucination rules.
   - No fabrication of case laws, statutes, or false authorities.
   - Missing details marked with explicit placeholders (e.g., `[Jurisdiction]`, `[Address]`).

4. **Deterministic Demo Mode (Zero-Config Fallback):**
   - Automatically activates if no Gemini API key is configured.
   - Generates complete, highly realistic legal documents deterministically.
   - Clearly notifies the user that Demo Mode is active.

5. **Live In-Browser Document Preview & Editing:**
   - Semantic dark-mode HTML preview card styled with formal legal typography.
   - Full in-browser editor allowing users to modify text before exporting.
   - Real-time save and update workflow.

6. **Multi-Format Export Options:**
   - **TXT**: Clean, utf-8 plain text preserving sections, clauses, and disclaimers.
   - **DOCX**: Professional Microsoft Word document with 1-inch margins, Times New Roman typography, embedded brand logo, running footers, and structured signature tables.
   - **PDF**: Ready-to-use PDF document generated with `fpdf2`, featuring running headers, dynamic page numbering (`Page X of Y`), and signature blocks.

7. **Custom Branding:**
   - Support for custom logo upload (PNG/JPG) embedded automatically into PDF and DOCX exports.
   - Configurable organization name in document headers and footers.

---

## 🏗️ System Architecture

```
User (Browser)
     │
     ▼
Streamlit Frontend (app.py) ──────────────┐
     │ (REST JSON Payload)                │ Direct in-process fallback
     ▼                                    │ if backend offline
FastAPI Backend (main.py, routes.py) ◄────┘
     │
     ├── Input Sanitization (utils/sanitizer.py)
     ├── Pydantic Request Validation (models/schemas.py)
     │
     ▼
AI Core (ai_core/gemini_generator.py)
     ├── Configured? ──► [Yes] ──► Google Gemini API (gemini-1.5-pro)
     └── Configured? ──► [No]  ──► Deterministic Demo Mode Engine
     │
     ▼
Document Utility Suite (document_utils/)
     ├── TXT Generator (document_utils/txt_generator.py)
     ├── DOCX Generator (document_utils/docx_generator.py)
     ├── PDF Generator (document_utils/pdf_generator.py)
     └── HTML Previewer (document_utils/formatter.py)
```

---

## 📁 Project Directory Structure

```text
LegalEase/
│
├── 1.Brainstorming & Ideation/         # Problem statement, ideation canvas, use cases
│   ├── Problem_Statement.md
│   ├── Ideation_and_Concept.md
│   └── Use_Case_Scenarios.md
│
├── 2.Requirement Analysis/             # Functional, non-functional, tech stack, stories
│   ├── Functional_Requirements.md
│   ├── Non_Functional_Requirements.md
│   ├── Technology_Stack_Selection.md
│   └── User_Stories.md
│
├── 3.Project Design Phase/             # System architecture, DFDs, UI/UX, API specs
│   ├── System_Architecture.md
│   ├── UI_UX_Design.md
│   ├── Data_Models_and_API_Design.md
│   └── Security_and_Sanitization_Design.md
│
├── 4.Project Planning Phase/           # WBS, sprint timelines, risk management
│   ├── Work_Breakdown_Structure_WBS.md
│   ├── Sprint_Plan_and_Timeline.md
│   └── Risk_Management_Plan.md
│
├── 5.Project Development Phase/        # Complete source code & implementation guides
│   ├── Development_Overview.md
│   ├── API_Implementation_Guide.md
│   ├── Document_Exporters_Guide.md
│   └── Source_Code/                    # Full mirrored source repository
│
├── 6.Project Testing/                  # Test plan, execution reports, test scripts
│   ├── Test_Plan.md
│   ├── Test_Cases_and_Results.md
│   ├── Test_Execution_Report.md
│   └── Automated_Test_Scripts/
│
├── 7.Project Documentation/            # Academic report, user manual, API reference
│   ├── Project_Report.md
│   ├── User_Manual.md
│   ├── API_Documentation.md
│   └── Developer_Guide.md
│
└── 8.Project Demonstration/            # Demo script, presentation deck, walkthrough
    ├── Demonstration_Script.md
    ├── Presentation_Deck_Outline.md
    ├── Screenshots_and_Walkthrough.md
    └── Demo_Video_Guide.md
```

### Application Source Code Structure
```text
LegalEase/
├── app.py                              # Streamlit frontend application
├── main.py                             # FastAPI server entry point
├── routes.py                           # REST routes (/generate, /health)
├── requirements.txt                    # Production dependencies
├── pytest.ini                          # Pytest configuration
├── .env.example                        # Environment variables template
├── .env                                # Local configuration (API keys, ports)
├── .gitignore                          # Git ignore rules
│
├── ai_core/                            # AI drafting & prompt engineering
│   ├── __init__.py
│   └── gemini_generator.py             # Gemini client + Prompt builder + Demo mode
│
├── document_utils/                     # Document formatting and export engines
│   ├── __init__.py
│   ├── docx_generator.py               # Microsoft Word (.docx) export
│   ├── pdf_generator.py                # PDF export with headers/footers
│   ├── txt_generator.py                # Clean plain text (.txt) export
│   └── formatter.py                    # HTML previewer and terms parser
│
├── models/                             # Data schemas & validation
│   ├── __init__.py
│   └── schemas.py                      # Pydantic models (DocumentRequest, DocumentResponse)
│
├── utils/                              # Helper utilities
│   ├── __init__.py
│   ├── sanitizer.py                    # Text & input sanitization
│   └── config.py                       # Centralized configuration loader
│
├── assets/                             # Brand visual assets
│   ├── generate_logos.py               # Script to generate brand logos
│   └── logo/
│       ├── logo.png                    # Standard logo for DOCX/PDF
│       └── inverseLogo.png             # Inverse logo for dark-theme UI
│
└── tests/                              # Automated test suite (17 tests)
    ├── test_api.py                     # FastAPI endpoint and validation tests
    ├── test_formatter.py               # Sanitizer and HTML preview tests
    ├── test_exports.py                 # TXT, DOCX, and PDF export tests
    └── test_ai_generator.py            # AI Core prompt and demo mode tests
```


---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python **3.10** or higher (Python 3.13 supported)
- pip package manager

### 2. Clone or Navigate to Project
```bash
cd d:\Projects\NM
```

### 3. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux / macOS
```

Edit `.env` to configure your Gemini API Key and settings:
```env
# Google Gemini API Key (get from https://aistudio.google.com/)
# Leave blank to run in Demo Mode automatically
GEMINI_API_KEY=your_gemini_api_key_here

# Model name (default: gemini-1.5-pro, or gemini-1.5-flash)
GEMINI_MODEL=gemini-1.5-pro

# Server configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
BACKEND_URL=http://127.0.0.1:8000
```

---

## 🚀 Running the Application

LegalEase is designed to run with a separate backend API server and frontend UI.

### Step 1: Start the FastAPI Backend
Open a terminal with the virtual environment activated:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- API will be accessible at: `http://127.0.0.1:8000`
- Interactive Swagger API docs: `http://127.0.0.1:8000/docs`
- Health status check: `http://127.0.0.1:8000/health`

### Step 2: Start the Streamlit Frontend
Open a second terminal with the virtual environment activated:
```bash
streamlit run app.py
```
The Streamlit application will open in your default browser at:
`http://localhost:8501`

---

## 📡 REST API Reference

### Health Check
- **Endpoint:** `GET /health`
- **Response:**
```json
{
  "status": "ok",
  "gemini_configured": false,
  "model": "gemini-1.5-pro",
  "demo_mode": true
}
```

### Generate Document
- **Endpoint:** `POST /generate`
- **Request Headers:** `Content-Type: application/json`
- **Payload Example:**
```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Work delivered by May 15, 2025; Payment of $4,500 within 7 days of invoice; Client retains intellectual property; Either party may terminate with 15 days notice",
  "dates": "April 15, 2025"
}
```
- **Response Example:**
```json
{
  "success": true,
  "document_type": "Freelance Work Contract",
  "content": "## Freelance Work Contract\n\nThis Agreement is entered into...",
  "is_demo": true,
  "error": null,
  "message": "Document generated successfully in Demo Mode."
}
```

### Curl Test Command
```bash
curl -X POST "http://127.0.0.1:8000/generate" \
     -H "Content-Type: application/json" \
     -d "{\"document_type\": \"NDA\", \"parties\": \"Party A, Party B\", \"terms\": \"Strict confidentiality for 2 years\", \"dates\": \"October 1, 2025\"}"
```

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:

```bash
pytest -v
```

All 17 test cases test:
- FastAPI root (`/`) and health check (`/health`)
- Document generation requests (`POST /generate`)
- Input validation and empty field rejection
- Input sanitization (smart quotes, dashes, script tag stripping)
- HTML preview rendering
- Plain text (`.txt`) export
- Microsoft Word (`.docx`) formatting and signature table creation
- PDF (`.pdf`) multi-page rendering and headers/footers
- Deterministic fallback in Demo Mode

---

## 🔒 Security Best Practices

1. **API Keys**: Stored exclusively in `.env` and excluded from source control via `.gitignore`.
2. **Error Masking**: API tokens and stack traces are never returned to clients or logged in production.
3. **Input Sanitization**: Control characters, script tags, and event handlers are neutralized before passing to models or document renderers.
4. **Data Privacy**: LegalEase processes documents ephemerally in memory without persistent database logging of confidential contract details.

---

## 📄 License
This project is licensed under the MIT License.
