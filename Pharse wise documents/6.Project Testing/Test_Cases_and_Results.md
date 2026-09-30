# 2. Test Cases & Verification Results — LegalEase

This document catalogs the complete test case matrix, inputs, expected behaviors, actual outcomes, and pass/fail statuses for LegalEase.

---

## 1. Automated Test Cases Matrix (17 Automated Tests)

| Test ID | Module | Test Function Name | Tested Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | API | `test_root_endpoint` | `GET /` | Returns `200 OK`, `status="online"`. | `status="online"`, HTTP 200 | **PASS** |
| **TC-02** | API | `test_health_endpoint` | `GET /health` | Returns `200 OK`, status & model. | `status="ok"`, HTTP 200 | **PASS** |
| **TC-03** | API | `test_generate_valid_request` | `POST /generate` (Valid payload) | Returns `200 OK`, `success=True`. | `success=True`, length > 100 | **PASS** |
| **TC-04** | API | `test_generate_empty_inputs_validation` | `POST /generate` (Whitespace fields) | Returns `400` or `422` error. | Validation error returned | **PASS** |
| **TC-05** | API | `test_generate_demo_mode_indicator` | `POST /generate` (No API key) | Returns `is_demo=True`. | `is_demo=True` verified | **PASS** |
| **TC-06** | Exporters | `test_txt_export` | `format_txt(sample_doc)` | Clean UTF-8 bytes with header. | Title & disclaimer present | **PASS** |
| **TC-07** | Exporters | `test_docx_export` | `format_docx(sample_doc)` | Non-empty DOCX with table. | Signature table verified | **PASS** |
| **TC-08** | Exporters | `test_pdf_export` | `format_pdf(sample_doc)` | Non-empty PDF with `%PDF-`. | Valid `%PDF-` byte header | **PASS** |
| **TC-09** | Exporters | `test_pdf_multipage_handling` | Multi-page text (25 clauses) | Clean multi-page PDF generation. | Multi-page PDF rendered | **PASS** |
| **TC-10** | Sanitizer | `test_sanitize_text_normalizes_quotes` | Smart quotes: `“Agreement”` | Replaced with `"Agreement"`. | Clean ASCII quotes | **PASS** |
| **TC-11** | Sanitizer | `test_sanitize_text_strips_script_injection` | `<script>alert('xss')</script>` | Script tag completely stripped. | Malicious tags removed | **PASS** |
| **TC-12** | Sanitizer | `test_sanitize_text_preserves_legal_brackets` | `[Party Name]`, `§ 4.2`, `$10k` | Legal syntax preserved. | Brackets & symbols intact | **PASS** |
| **TC-13** | Formatter | `test_parse_terms_semicolon_separated` | `T1; T2; T3` | Array of 3 distinct term items. | 3 terms parsed cleanly | **PASS** |
| **TC-14** | Formatter | `test_parse_terms_handles_bullets` | `- Item 1\n* Item 2\n3. Item 3` | Array of 3 cleaned items. | Bullets stripped | **PASS** |
| **TC-15** | Formatter | `test_format_html_preview` | Markdown `## Title`, `* Bullet` | HTML with `<h2>`, `<h4>`, `<li>`. | Styled semantic HTML | **PASS** |
| **TC-16** | AI Core | `test_gemini_generator_prompt_builder` | Valid document parameters | Formats anti-hallucination prompt. | Negative constraints present | **PASS** |
| **TC-17** | AI Core | `test_gemini_generator_demo_types` | NDA, Lease, Employment inputs | Returns tailored contract text. | Valid tailored contracts | **PASS** |

---

## 2. Manual UI / Browser Verification Matrix

| UI Step | Action Performed | Expected Behavior | Actual Behavior | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Step 1** | Launch Streamlit at `http://localhost:8501`. | Page loads centered layout with brand logo. | Logo rendered centered via 3 columns. | **PASS** |
| **Step 2** | Click preset button "⚡ Non-Disclosure Agreement". | Input fields populate with sample NDA terms. | Inputs populated instantly. | **PASS** |
| **Step 3** | Click "🚀 Generate Document". | Loading spinner displays, document drafts. | Generated document preview card appears. | **PASS** |
| **Step 4** | Click "✏️ Click to Edit Document". | Text area opens with current draft. | Text area rendered with draft text. | **PASS** |
| **Step 5** | Modify wording & click "💾 Save Changes". | Preview updates with modified text. | Preview reflects updated text. | **PASS** |
| **Step 6** | Click "📄 Download as .TXT". | Browser downloads `.txt` file. | File downloaded; clean text verified. | **PASS** |
| **Step 7** | Click "📘 Download as .DOCX". | Browser downloads `.docx` file. | Word file opens; tables & logo present. | **PASS** |
| **Step 8** | Click "📕 Download as .PDF". | Browser downloads `.pdf` file. | PDF file opens; headers & footers present. | **PASS** |
