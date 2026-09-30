# 2. UI/UX Design Specification — LegalEase

This document establishes the user interface design system, color palettes, typography, responsive wireframes, and interaction patterns for LegalEase.

---

## 1. Design System & Style Guidelines

### A. Color Palette
- **Primary Accent**: `#3B82F6` (Electric Legal Blue) — Used for primary buttons, active tabs, and section highlights.
- **Secondary Accent**: `#10B981` (Emerald Green) — Used for success toasts, live indicators, and verification badges.
- **Card Background**: `#0F172A` (Deep Slate / Dark Navy) — Formatted preview card background simulating modern legal dark-mode.
- **Application Canvas**: Streamlit native dark theme `#0E1117` with light contrast borders `#334155`.
- **Text Hierarchy**:
  - Headings: `#F8FAFC` (Pure Crisp White)
  - Subheadings & Titles: `#60A5FA` / `#93C5FD` (Soft Cyan Blue)
  - Body Text: `#CBD5E1` (Readable Light Slate)
  - Meta/Footnotes: `#64748B` / `#94A3B8` (Muted Steel Gray)
  - Disclaimer Warning: `#F59E0B` (Amber Warning)

### B. Typography
- **Headings & Legal Titles**: `Georgia`, `Times New Roman`, serif — Evokes formal legal documentation authority and clarity.
- **User Interface & Inputs**: `Inter`, `Segoe UI`, `System-UI`, sans-serif — Clean, modern, highly legible form fields.
- **Code & Signature Underscores**: `Monospace` — Clear character alignment for signature underlines.

---

## 2. Wireframe & Visual Layout

### Main Application Layout (Single-Column Centered, Max Width 860px)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        [  LOGO: LegalEase Scales  ]                     │
│                     AI-POWERED LEGAL DOCUMENT GENERATOR                │
│                                                                        │
│ [!] LEGAL NOTICE: LegalEase provides AI-generated draft documents...  │
│ [*] DEMO MODE / LIVE STATUS BADGE                                      │
│                                                                        │
│ ────────────────────────────────────────────────────────────────────── │
│ [ > ] ⚡ Load Pre-configured Sample Scenarios (Optional Expander)      │
│       [ Freelance ] [ NDA ] [ Employment ] [ Residential Lease ]        │
│ ────────────────────────────────────────────────────────────────────── │
│                                                                        │
│ ### 📋 Document Specifications                                         │
│ 1. Document Type: [ Selectbox: Non-Disclosure Agreement (NDA) ▼ ]      │
│                                                                        │
│ 2. Parties Involved:                                                   │
│    ┌──────────────────────────────────────────────────────────────┐    │
│    │ Jane Doe (Service Provider), TechNova Inc. (Client)          │    │
│    └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│ 3. Terms & Conditions (Use semicolons for bullet points):              │
│    ┌──────────────────────────────────────────────────────────────┐    │
│    │ Payment within 30 days; Confidentiality must be maintained;  │    │
│    │ Either party may terminate with 15 days written notice        │    │
│    └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│ 4. Effective Date: [ Date Picker: April 15, 2025 📅 ]                 │
│                                                                        │
│ [ > ] 🎨 Optional Branding & Customization (Expander)                  │
│       Org Name: [ TechNova Inc. ]   Upload Logo: [ Browse... ]         │
│                                                                        │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │                  🚀 GENERATE DOCUMENT (Button)                     │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ────────────────────────────────────────────────────────────────────── │
│ ### 📄 Generated Document                                              │
│ [ ✏️ Click to Edit Document ]               [ 🔄 Start New Document ]   │
│                                                                        │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │                  ## NON-DISCLOSURE AGREEMENT                       │ │
│ │ This Non-Disclosure Agreement is entered into on April 15, 2025... │ │
│ │                                                                    │ │
│ │ 1. Definition of Confidential Information                          │ │
│ │ 2. Agreed Terms:                                                   │ │
│ │    • Payment within 30 days                                        │ │
│ │    • Confidentiality must be maintained                            │ │
│ │                                                                    │ │
│ │ ___________________________          ___________________________   │ │
│ │ Authorized Signature                 Authorized Signature          │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ### 💾 Export & Download                                               │
│ [ 📄 Download as .TXT ]  [ 📘 Download as .DOCX ]  [ 📕 Download PDF ] │
│                                                                        │
│ ────────────────────────────────────────────────────────────────────── │
│ LegalEase Inc. | contact@legalease.com | All Rights Reserved           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Interaction Patterns & Micro-Interactions

1. **State Preservation**: Generated text and user modifications are held in `st.session_state["generated_text"]`, preventing accidental data loss upon widget re-renders.
2. **Duplicate Submission Protection**: Streamlit's reactive execution disables button re-clicks during ongoing spinner execution (`st.spinner("Drafting your legal document with AI...")`).
3. **Edit Mode Toggle**:
   - Preview Mode displays the styled card.
   - Clicking "✏️ Click to Edit Document" seamlessly swaps the card for a 420px height text area.
   - Clicking "💾 Save Changes" sanitizes input, updates state, and returns to preview mode.
4. **Preset Loaders**: Clicking any sample preset instantly populates Document Type, Parties, Terms, and Date without requiring manual keystrokes.
