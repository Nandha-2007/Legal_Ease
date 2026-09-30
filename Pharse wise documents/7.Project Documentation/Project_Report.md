# LegalEase: Project Report — AI-Powered Legal Document Generator

---

## ABSTRACT
In modern commerce, formal contracts are indispensable for establishing trust, safeguarding intellectual property, and mitigating legal risks. However, traditional legal drafting is constrained by high attorney fees, while static online boilerplate forms lack custom adaptability. **LegalEase** is a full-stack, AI-powered web platform designed to automate the authoring of customizable, professional-grade legal agreements. Leveraging **FastAPI**, **Google Gemini Generative AI**, and **Streamlit**, LegalEase translates user-specified parties, effective dates, and semicolon-delimited business conditions into structured, formal legal instruments. The platform incorporates strict anti-hallucination prompt engineering, an offline deterministic **Demo Mode**, in-browser text editing, and multi-format compilation into **TXT**, **DOCX**, and **PDF** formats with embedded branding and legal typography.

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background
Small enterprises, independent contractors, startup founders, and property owners frequently require routine legal instruments such as Non-Disclosure Agreements, Employment Contracts, and Residential Leases. Commercial law firms charge hundreds of dollars per hour, creating an access barrier. Conversely, generic static forms online fail to integrate custom conditions without introducing legal inconsistencies.

### 1.2 Problem Statement
How can modern generative artificial intelligence be harnessed to generate customizable, formally structured, and formatted legal documents while strictly preventing factual hallucinations and preserving user privacy?

### 1.3 Project Objectives
1. Build an intuitive web application allowing non-lawyers to draft legal contracts.
2. Implement Google Gemini 1.5 Pro with anti-hallucination prompt architecture.
3. Provide an offline, zero-configuration Demo Mode for zero-key environments.
4. Support live in-browser preview and text editing.
5. Deliver instant exports in plain text, Microsoft Word (.docx), and PDF formats.

---

## CHAPTER 2: SYSTEM ARCHITECTURE & DESIGN

### 2.1 Architectural Overview
LegalEase adopts a modular microservice-style pattern:
- **Presentation Layer**: Streamlit (`app.py`) delivering centered UI, responsive input controls, dark-card previews, and download buttons.
- **API Routing Layer**: FastAPI (`main.py`, `routes.py`) processing requests via ASGI server Uvicorn.
- **AI Core Layer**: `GeminiDocumentGenerator` managing prompt synthesis, SDK interaction, and fallback logic.
- **Document Formatting Layer**: Dedicated modules compiling raw text into `.docx` (via `python-docx`) and `.pdf` (via `fpdf2`).

---

## CHAPTER 3: IMPLEMENTATION

### 3.1 AI Prompt Engineering & Anti-Hallucination
To eliminate risks of fabricated case citations, the prompt explicitly instructs the model to use neutral jurisdictional language (e.g. `[State/Jurisdiction]`) and place all missing facts in square brackets.

### 3.2 Semicolon Terms Engine
The terms input is parsed across semicolons (`;`) or line breaks, cleaned of extraneous bullets, and expanded into numbered contractual obligations.

### 3.3 Multi-Format Compilation
- **DOCX**: Applies 1-inch margins, Times New Roman 11pt/16pt font, 2-column signature tables, and running footers with page numbers.
- **PDF**: Employs `fpdf2` with running top headers and bottom footers (`Page X of Y`).

---

## CHAPTER 4: TESTING & RESULTS
The project was evaluated using 17 automated tests covering Pydantic validation, API routes, text sanitization, and export integrity. The suite attained a 100% pass rate in 2.11 seconds. Manual browser testing verified smooth end-to-end operation.

---

## CHAPTER 5: CONCLUSION & FUTURE ENHANCEMENTS
LegalEase demonstrates how generative AI can democratize access to foundational legal instruments safely. Future directions include multi-language drafting, clause risk analysis, and direct integration with digital signature APIs.
