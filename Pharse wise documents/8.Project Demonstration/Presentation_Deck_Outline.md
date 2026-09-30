# 2. Presentation Deck Outline — LegalEase

This document outlines the slide-by-slide structure, talking points, visual assets, and key takeaways for presenting LegalEase.

---

## Slide 1: Title & Introduction
- **Title**: LegalEase: AI-Powered Legal Document Generator
- **Subtitle**: Automated, Customizable, and Professional Legal Drafting
- **Visual**: Scales of Justice Logo (`assets/logo/logo.png`)
- **Footer**: SmartBridge / Academic Internship Project Presentation

---

## Slide 2: The Problem
- High legal consultation costs ($300 - $1,500/contract).
- Rigid static templates failing to adapt to custom business terms.
- Dense legal terminology ("legalese") creating confusion.
- Formatting breakdowns across Word and PDF exports.

---

## Slide 3: The Solution — LegalEase
- Generative AI-driven drafting tailored to user inputs.
- Semicolon-delimited custom terms parsed into numbered clauses.
- Zero-crash deterministic **Demo Mode** for zero-key environments.
- In-browser preview, in-line editor, and multi-format exports (.txt, .docx, .pdf).

---

## Slide 4: System Architecture
- **Frontend**: Streamlit (Reactive UI, state management, download streams).
- **Backend**: FastAPI + Uvicorn (REST API, Pydantic validation, CORS).
- **AI Core**: Google Gemini 1.5 Pro + Strict Anti-Hallucination Prompting.
- **Exporters**: `python-docx` (Word) and `fpdf2` (PDF).

---

## Slide 5: Key Functional Capabilities
- Dropdown document type selection + Custom document titles.
- Multi-party role mapping (e.g. Disclosing/Receiving, Employer/Employee).
- Semicolon-separated terms conversion into distinct covenants.
- Optional brand logo uploader & custom organization names.

---

## Slide 6: Prompt Engineering & Anti-Hallucination
- Two-tier guardrails: System Instruction + Negative Prompting.
- Strict prohibition against fabricating case law, statutes, or personal data.
- Mandatory square-bracket placeholders (e.g., `[Address]`, `[Jurisdiction]`).

---

## Slide 7: Live UI Walkthrough
- Centered brand header with dark-slate preview card.
- 1-click sample presets (Freelance, NDA, Lease, Employment).
- In-line live editor with instant "Save Changes" synchronization.

---

## Slide 8: Multi-Format Document Compilation
- **TXT**: Plain text with ASCII section delimiters.
- **DOCX**: 1-inch margins, Times New Roman, embedded logo, 2-column signature table.
- **PDF**: Automatic page breaks, running headers, footers with `Page X of Y`.

---

## Slide 9: Security & Sanitization
- API keys isolated in `.env` and shielded from source control via `.gitignore`.
- Multi-stage regex sanitization (`sanitize_text()`) neutralizing script injection and smart quotes.
- Ephemeral in-memory data processing with zero permanent contract storage.

---

## Slide 10: Testing & Verification
- 17 automated tests implemented with `pytest`.
- 100% pass rate achieved in 2.11 seconds.
- Validated across API routes, sanitization, AI core, and multi-format exporters.

---

## Slide 11: Future Roadmap
- Multi-language legal document generation.
- Clause-by-clause contract risk assessment and summarization.
- DocuSign / Adobe Sign electronic signature API integration.

---

## Slide 12: Conclusion & Q&A
- LegalEase bridges the gap between accessibility and legal professionalism.
- Mandatory legal disclaimer: Informational drafting aid, not certified attorney counsel.
- Thank You / Open for Questions.
