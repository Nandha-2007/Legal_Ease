# 4. User Stories & Acceptance Criteria — LegalEase

This document specifies the user stories, personas, acceptance criteria, and Definitions of Done for the LegalEase platform.

---

## Epic 1: Document Configuration & Input Specification

### US-1.1: Document Type Selection
- **As a** user drafting a contract,
- **I want to** select my target document type from a curated dropdown list or provide a custom title,
- **So that** the AI structures the clauses appropriate to that legal instrument.
- **Acceptance Criteria**:
  - Dropdown contains at least: NDA, Employment Contract, Freelance Work Contract, Lease Agreement, Service Agreement, Offer Letter, General Agreement, and Custom Document.
  - Selecting "Custom Document" renders a text input for specifying an arbitrary contract title.

### US-1.2: Semicolon-Separated Terms Input
- **As a** business operator,
- **I want to** input my specific conditions separated by semicolons,
- **So that** each term is automatically recognized and formatted into a distinct contractual clause.
- **Acceptance Criteria**:
  - The text area accepts inputs like: `Payment net 30; IP owned by client; 15 days notice`.
  - The terms parser cleans leading bullets and splits entries across semicolons or newlines.
  - Numbered or bulleted clauses appear properly formatted in the resulting document.

### US-1.3: Custom Branding & Logo Upload
- **As a** startup founder,
- **I want to** upload my company logo and enter our legal entity name,
- **So that** my generated contracts reflect professional company branding.
- **Acceptance Criteria**:
  - File uploader accepts `.png`, `.jpg`, and `.jpeg`.
  - Uploaded logo is rendered at the top center of Word and PDF exports.
  - Company name appears in the running footer and title headers.

---

## Epic 2: AI-Powered Legal Drafting & Fallback

### US-2.1: Gemini AI Document Drafting
- **As a** user,
- **I want to** generate a structured legal draft using Google Gemini,
- **So that** I obtain formal, comprehensive drafting tailored to my inputs in seconds.
- **Acceptance Criteria**:
  - Clicking "Generate Document" invokes the FastAPI `/generate` endpoint.
  - Output contains formal Recitals, Definitions, Obligations, Term/Termination, Governing Law, and Signatures.
  - No fake personal data or fabricated court statutes are created.
  - Placeholders like `[Address]` or `[State/Jurisdiction]` indicate missing details.

### US-2.2: Deterministic Demo Mode (Zero-Config)
- **As an** evaluator or developer running the system without an API key,
- **I want to** test all generation and export capabilities,
- **So that** the application never crashes due to missing credentials.
- **Acceptance Criteria**:
  - Missing or blank `GEMINI_API_KEY` triggers Demo Mode with realistic legal templates.
  - UI displays an amber/blue Demo Mode banner informing the user of the mock status.
  - Returns `is_demo: true` and generates valid documents matching the selected type.

---

## Epic 3: Document Preview, Editing & Multi-Format Export

### US-3.1: Dark-Themed Styled HTML Preview
- **As a** user,
- **I want to** review my generated agreement in a clear, formatted preview,
- **So that** I can inspect sections, clauses, and layout before downloading.
- **Acceptance Criteria**:
  - Formatted inside a dark-slate card container with Georgia/Times serif typography.
  - Section titles (`##`, `###`) are transformed into colored headings (`<h2>`, `<h4>`).
  - Lists and signature underscores are visually styled.

### US-3.2: In-Browser Live Editing
- **As a** legal officer,
- **I want to** edit clauses directly in the browser and save my modifications,
- **So that** the exported documents reflect my final exact wording.
- **Acceptance Criteria**:
  - Clicking "✏️ Click to Edit Document" opens an editable text area pre-filled with the draft.
  - Clicking "💾 Save Changes" updates session state with sanitized text and updates the preview.

### US-3.3: Multi-Format Downloads (.TXT, .DOCX, .PDF)
- **As a** user,
- **I want to** download the finalized document in TXT, DOCX, and PDF formats,
- **So that** I have editable source files for Word, read-only PDFs for signatures, and plain text for archives.
- **Acceptance Criteria**:
  - `.txt` download provides UTF-8 encoded plain text with headers and legal disclaimers.
  - `.docx` download provides formatted Word file with 1-inch margins, logo, and 2-column signature table.
  - `.pdf` download provides clean PDF with running headers, footers, and page numbers (`Page X of Y`).
