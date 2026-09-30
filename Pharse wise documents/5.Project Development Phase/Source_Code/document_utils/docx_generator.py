import io
import os
import re
from typing import Optional, Union
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from utils.config import DEFAULT_LOGO_PATH


def _add_page_number(run):
    """Helper to add XML page number field into a DOCX run."""
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)


def format_docx(
    text: str,
    doc_type: str = "Legal Document",
    logo_path: Optional[Union[str, io.BytesIO]] = None,
    org_name: Optional[str] = None,
) -> bytes:
    """Format legal document into a professional Microsoft Word (.docx) document.

    Features:
    - 1-inch standard legal margins
    - Times New Roman typography
    - Optional embedded brand logo
    - Professional headings and title
    - Semicolon-separated terms table
    - Formal signature blocks
    - Running footer with draft notice & page numbers
    """
    doc = Document()

    # 1. Page Margins Setup
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Setup Footer
        footer = section.footer
        footer_p = footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        footer_run = footer_p.add_run(
            f"{org_name or 'LegalEase'} | {doc_type} (Draft)  |  Page "
        )
        footer_run.font.name = "Times New Roman"
        footer_run.font.size = Pt(9)
        footer_run.font.color.rgb = RGBColor(128, 128, 128)
        
        # Add dynamic page number
        page_run = footer_p.add_run()
        page_run.font.name = "Times New Roman"
        page_run.font.size = Pt(9)
        page_run.font.color.rgb = RGBColor(128, 128, 128)
        try:
            _add_page_number(page_run)
        except Exception:
            pass

    # 2. Add Logo (User-provided or Default)
    resolved_logo = None
    if logo_path is not None:
        resolved_logo = logo_path
    elif os.path.exists(DEFAULT_LOGO_PATH):
        resolved_logo = str(DEFAULT_LOGO_PATH)

    if resolved_logo is not None:
        try:
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_run = logo_p.add_run()
            logo_run.add_picture(resolved_logo, width=Inches(2.2))
            logo_p.paragraph_format.space_after = Pt(14)
        except Exception:
            # If image loading fails, continue gracefully
            pass

    # 3. Add Document Title
    title_text = doc_type
    lines = text.split("\n")
    first_heading = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("# "):
            first_heading = stripped.lstrip("#").strip()
            break

    if first_heading:
        title_text = first_heading

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(title_text.upper())
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(20, 30, 48)
    title_p.paragraph_format.space_after = Pt(18)
    title_p.paragraph_format.space_before = Pt(4)

    # 4. Parse & Process Body Content
    i = 0
    in_signature_section = False
    sig_lines = []

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue

        # Skip the title line since we already placed it
        if (line.startswith("## ") or line.startswith("# ")) and first_heading and first_heading in line:
            continue

        # Check for signature section marker
        if "IN WITNESS WHEREOF" in line.upper() or "SIGNATURE" in line.upper() and ("____" in line or (i < len(lines) and "____" in lines[i])):
            in_signature_section = True
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(10)
            run = p.add_run(line.replace("**", "").replace("##", "").replace("###", "").strip())
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.italic = True
            continue

        if in_signature_section:
            sig_lines.append(line)
            continue

        # Section Headings (Level 2/3)
        if line.startswith("### ") or line.startswith("## "):
            heading_content = line.lstrip("#").strip()
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(14)
            h_p.paragraph_format.space_after = Pt(4)
            h_run = h_p.add_run(heading_content)
            h_run.font.name = "Times New Roman"
            h_run.font.size = Pt(12)
            h_run.font.bold = True
            h_run.font.color.rgb = RGBColor(30, 41, 59)
            continue

        # Numbered items (e.g. 1. Obligations, 2. Terms)
        num_match = re.match(r'^(\d+[\.\)])\s+(.*)', line)
        if num_match:
            prefix = num_match.group(1)
            rest = num_match.group(2)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_after = Pt(5)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

            pref_run = p.add_run(f"{prefix} ")
            pref_run.font.name = "Times New Roman"
            pref_run.font.size = Pt(11)
            pref_run.font.bold = True

            # Process inline bold tags
            _add_formatted_runs(p, rest)
            continue

        # Bullet items (* or -)
        if re.match(r'^[\*\-]\s+', line):
            bullet_text = re.sub(r'^[\*\-]\s+', '', line)
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_after = Pt(4)
            _add_formatted_runs(p, bullet_text)
            continue

        # Regular legal paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _add_formatted_runs(p, line)

    # 5. Build Signature Block Table
    _build_docx_signature_table(doc, sig_lines)

    # Save to BytesIO buffer
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)
    return output_stream.getvalue()


def _add_formatted_runs(paragraph, text: str):
    """Parse inline **bold** markup into python-docx runs."""
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            clean = part[2:-2]
            run = paragraph.add_run(clean)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.bold = True
        else:
            run = paragraph.add_run(part)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)


def _build_docx_signature_table(doc: Document, sig_lines: list):
    """Construct a clean 2-column signature block in DOCX."""
    # Add spacing before signatures
    spacing_p = doc.add_paragraph()
    spacing_p.paragraph_format.space_before = Pt(18)

    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Width for each signature column
    for row in table.rows:
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.2)

    # Left Column (Party 1)
    table.cell(0, 0).paragraphs[0].text = "____________________________________"
    table.cell(1, 0).paragraphs[0].text = "Authorized Signature"
    table.cell(2, 0).paragraphs[0].text = "Print Name: _______________________"
    table.cell(3, 0).paragraphs[0].text = "Title: ____________________________"
    table.cell(4, 0).paragraphs[0].text = "Date: _____________________________"

    # Right Column (Party 2)
    table.cell(0, 1).paragraphs[0].text = "____________________________________"
    table.cell(1, 1).paragraphs[0].text = "Authorized Signature"
    table.cell(2, 1).paragraphs[0].text = "Print Name: _______________________"
    table.cell(3, 1).paragraphs[0].text = "Title: ____________________________"
    table.cell(4, 1).paragraphs[0].text = "Date: _____________________________"

    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
