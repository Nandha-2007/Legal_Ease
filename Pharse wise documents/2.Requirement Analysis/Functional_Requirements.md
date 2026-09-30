# 1. Functional Requirements Specification — LegalEase

This document details the functional capabilities of the LegalEase system, establishing the behavioral requirements for the frontend interface, backend API, AI generation pipeline, and document export engines.

---

## 1. System Feature Matrix

| ID | Feature Name | Priority | Module | Description |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Document Type Selection | High | Frontend | User selects from standard legal agreement types or inputs a custom title. |
| **FR-02** | Parties Specification | High | Frontend / API | User inputs parties and designated roles (e.g. Disclosing/Receiving, Employer/Employee). |
| **FR-03** | Terms & Conditions Parsing | High | Core Utility | User enters terms separated by semicolons; system parses and formats into distinct clauses. |
| **FR-04** | Effective Date Picker | Medium | Frontend | User selects an effective date via date picker; system converts to formal legal date format. |
| **FR-05** | Optional Branding & Logo | Medium | Frontend / Exporters | User uploads PNG/JPG logo and specifies custom organization name for headers/footers. |
| **FR-06** | Gemini AI Document Drafting | High | AI Core | Backend calls Gemini 1.5 Pro with anti-hallucination prompt to generate formal agreement. |
| **FR-07** | Deterministic Demo Fallback | High | AI Core | Operates without API key, generating structured, tailored legal drafts without crashing. |
| **FR-08** | Dark-Mode HTML Preview | High | Frontend | Renders generated text in an elegant, scrollable, dark-card container with legal styling. |
| **FR-09** | In-Browser Document Editor | High | Frontend | Allows live editing of generated text with instant "Save Changes" state synchronization. |
| **FR-10** | Plain Text (.TXT) Export | Medium | Exporters | Generates clean UTF-8 plain text with uppercase section headers and legal disclaimer. |
| **FR-11** | Word (.DOCX) Export | High | Exporters | Generates `.docx` with 1-inch margins, Times New Roman, logo, signature table, and footers. |
| **FR-12** | PDF (.PDF) Export | High | Exporters | Generates `.pdf` using `fpdf2` with running headers, footers, page numbering, and signatures. |
| **FR-13** | Input Sanitization & Security | High | Core Utility | Normalizes smart quotes, strips script tags, prevents XSS, and masks sensitive API keys. |
| **FR-14** | One-Click Sample Presets | Medium | Frontend | Expander enabling instant population of test scenarios (Freelance, NDA, Lease, Employment). |
| **FR-15** | Mandatory Legal Disclaimer | High | Frontend / Docs | Prominently displays notice that output is an informational drafting aid, not legal advice. |

---

## 2. Detailed Functional Specifications

### FR-01: Document Type Selection
- **Input**: Dropdown selectbox.
- **Predefined Options**:
  - `Freelance Work Contract`
  - `Non-Disclosure Agreement (NDA)`
  - `Employment Contract`
  - `Residential / Commercial Lease Agreement`
  - `Service Agreement`
  - `Employment Offer Letter`
  - `General Business Agreement`
  - `Custom Document`
- **Behavior**: When "Custom Document" is selected, an auxiliary text input appears to allow user-defined document titles (e.g., "Consulting Agreement").

### FR-02: Parties Involved Specification
- **Input**: Multi-line text area.
- **Validation**: Cannot be empty or contain solely whitespace. Maximum length 2,000 characters.
- **Example**: `Jane Doe (Service Provider), TechNova Inc. (Client)`.

### FR-03: Terms & Conditions Parsing
- **Input**: Multi-line text area.
- **Format**: Semicolon-delimited clauses (e.g., `Payment within 30 days; Confidentiality preserved; 15 days notice`).
- **Processing**: The `parse_terms` utility splits the string across `;` or `\n`, cleans leading bullets (`*`, `-`, numbers), and formats terms into distinct numbered clauses in the generated document.

### FR-04: Effective Date Configuration
- **Input**: Streamlit date input widget.
- **Processing**: Formatted into formal long-form legal date string (e.g., `April 15, 2025` or `October 10, 2025`).

### FR-05: Optional Branding & Customization
- **Inputs**:
  - Logo file uploader (supports `.png`, `.jpg`, `.jpeg`).
  - Organization Name text input.
- **Output**: Embeds uploaded image centered at the top of the Word document and PDF, and incorporates organization name into running headers and footers.

### FR-06 & FR-07: AI Core Generation & Demo Mode
- **API Call**: FastAPI endpoint `POST /generate`.
- **Primary Route**: If `GEMINI_API_KEY` is present and valid, sends structured prompt to `gemini-1.5-pro`.
- **Fallback Route**: If `GEMINI_API_KEY` is missing or empty, triggers deterministic template generation matching the selected document type, returning `is_demo = True`.
- **Anti-Hallucination Constraints**: Strictly forbids fabricating statutory citations, case law, or fake personal details. Requires square-bracket placeholders (e.g., `[Jurisdiction]`, `[Address]`) for unknown items.

### FR-08 & FR-09: Live Document Preview & Editing
- **Preview**: Rendered via `format_html_preview()` into styled semantic HTML within a dark-mode card container.
- **Editor**: Toggle button "✏️ Click to Edit Document" displays a large text area pre-populated with generated text. Clicking "💾 Save Changes" sanitizes and updates `st.session_state.generated_text`.

### FR-10, FR-11, FR-12: Multi-Format Exporters
- **TXT**: Plain text with ASCII section delimiters and footer notice.
- **DOCX**: 1-inch margins, Times New Roman 12pt body / 16pt title, embedded logo, 2-column signature table, dynamic page number XML field.
- **PDF**: Generated via `fpdf2`, custom `LegalPDF` class with automatic page breaks, running header on page > 1, running footer with `Page {nb}` on all pages, and signature section.
