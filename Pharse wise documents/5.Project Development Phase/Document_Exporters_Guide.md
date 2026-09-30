# 3. Document Exporters Implementation Guide — LegalEase

This document details the binary formatting and compilation mechanisms for Word (`.docx`), PDF (`.pdf`), plain text (`.txt`), and HTML previews.

---

## 1. Microsoft Word Exporter (`document_utils/docx_generator.py`)
- **Page Geometry**: 1.0-inch margins applied on all four edges (`top_margin`, `bottom_margin`, `left_margin`, `right_margin = Inches(1.0)`).
- **Typography**: Times New Roman throughout:
  - Document Title: 16pt Bold, Center Aligned, Dark Slate `#141E30`.
  - Section Headings: 12pt Bold with 14pt before / 4pt after spacing.
  - Body Text: 11pt, 1.15 line spacing, Justified alignment.
- **Embedded Branding**: Reads user uploaded logo or default `assets/logo/logo.png`, inserting it centered at the top of page 1 (`doc.add_picture(..., width=Inches(2.2))`).
- **Signature Table**: Assembles a 2-column, 5-row table for party signatures, printed names, titles, and dates.
- **Running Footer & Page Numbers**: Implements OpenXML fields (`w:fldChar`, `w:instrText = "PAGE"`) to render dynamic page numbers alongside the draft notice.

---

## 2. PDF Exporter (`document_utils/pdf_generator.py`)
- **Custom Subclass**: `class LegalPDF(FPDF)` encapsulates header and footer logic.
- **Running Headers**: Renders a subtle running header line on pages 2 and onward (`Page > 1`).
- **Running Footers**: Prints the organizational draft disclaimer on the left and `Page {nb}` on the right with a thin horizontal separator rule.
- **Latin-1 Normalization**: `_safe_latin1()` ensures that special symbols (smart quotes, dashes, section symbols `§`) map smoothly into FPDF core fonts without throwing encoding errors.
- **Signature Blocks**: Renders 2-column signature lines, automatically adding a page break if remaining vertical space on the current page is less than 55mm.

---

## 3. Plain Text Exporter (`document_utils/txt_generator.py`)
- Transforms markdown headers (`## `, `### `) into clean, capitalized section titles bordered with ASCII separator lines (`====================` and `--- Section ---`).
- Normalizes bullet points to `  * `.
- Encodes output into clean UTF-8 bytes with an appended legal notice.

---

## 4. Semantic HTML Previewer (`document_utils/formatter.py`)
- Escapes raw text with `html.escape()` to neutralize script injection.
- Replaces markdown headings with colored HTML tags (`<h2 style='color: #60a5fa;'>`, `<h4 style='color: #93c5fd;'>`).
- Formats signature lines with styled monospace underscores.
