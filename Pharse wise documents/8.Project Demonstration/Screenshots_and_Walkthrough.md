# 3. Visual Walkthrough & Screenshots Guide — LegalEase

This document documents the end-to-end user experience, visual layouts, and screen representations of LegalEase.

---

## 1. Main Application Header & Disclaimer
- **URL**: `http://localhost:8501`
- **Visual Description**:
  - The application header displays the centered **LegalEase Scales of Justice** brand logo (`inverseLogo.png` on dark theme, `logo.png` on light theme).
  - Subtitle: *"AI-Powered Legal Document Generator"*.
  - **Legal Disclaimer Banner**: Amber-bordered banner reading:
    > *"LEGAL NOTICE: LegalEase provides AI-generated draft documents and legal information for general informational purposes. It does not constitute legal advice and should not replace review by a qualified legal professional."*
  - **Demo Mode Banner**: Blue-bordered status banner confirming:
    > *"💡 Demo Mode Active: No Gemini API key detected. Realistic document drafting templates will be generated deterministically without consuming API credits."*

---

## 2. Sample Presets & Document Configuration
- **Sample Presets Expander**:
  - Four 1-click preset buttons: `[ Freelance Work Contract ]`, `[ Non-Disclosure Agreement (NDA) ]`, `[ Employment Contract ]`, `[ Residential Lease Agreement ]`.
- **Form Controls**:
  - **1. Document Type**: Dropdown selectbox.
  - **2. Parties Involved**: Large text area with placeholder `Jane Doe (Service Provider), TechNova Inc. (Client)`.
  - **3. Terms & Conditions**: Large text area with instruction `(Use semicolons for bullet points)`.
  - **4. Effective Date**: Interactive date picker defaulting to current date.
  - **5. Optional Branding Expander**: Fields for Organization Name and Logo File Uploader (`.png`, `.jpg`, `.jpeg`).

---

## 3. Document Generation & Styled Preview
- **Action**: User clicks the primary button **"🚀 Generate Document"**.
- **Loading State**: Displays spinner `⚖️ LegalEase is drafting your legal document...`.
- **Generated Preview**:
  - Formatted inside a dark slate container (`background-color: #0f172a`, `border: 1px solid #334155`).
  - Section headings rendered in formal legal serif typography with blue/cyan accents.
  - Semicolon-separated terms presented as distinct numbered clauses.
  - Two-column signature block at the bottom.

---

## 4. In-Line Live Editing Mode
- **Action**: User clicks **"✏️ Click to Edit Document"**.
- **Editor**: Swaps the preview card for a 420px height text area containing the full draft.
- **Save Action**: User modifies wording and clicks **"💾 Save Changes"**. The preview updates immediately.

---

## 5. Multi-Format Downloads
- **Action Hub**: Three side-by-side action buttons:
  - `📄 Download as .TXT`: Downloads clean text file with section dividers.
  - `📘 Download as .DOCX`: Downloads Word document with 1-inch margins, Times New Roman, logo, and 2-column signature table.
  - `📕 Download as .PDF`: Downloads print-ready PDF with running headers, footers, and page numbers (`Page X of Y`).
- **Reset Button**: `🔄 Start New Document` clears session state for a fresh draft.
