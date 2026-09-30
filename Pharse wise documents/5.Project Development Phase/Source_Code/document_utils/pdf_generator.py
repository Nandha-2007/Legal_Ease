import io
import os
import re
from typing import Optional, Union
from fpdf import FPDF
from utils.config import DEFAULT_LOGO_PATH


class LegalPDF(FPDF):
    """Custom FPDF class tailored for professional legal document rendering."""

    def __init__(self, doc_type: str = "Legal Document", org_name: Optional[str] = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.doc_type = doc_type
        self.org_name = org_name or "LegalEase"
        self.set_margins(left=20, top=20, right=20)
        self.set_auto_page_break(auto=True, margin=22)
        self.alias_nb_pages()

    def header(self):
        # On subsequent pages, render a subtle top running header
        if self.page_no() > 1:
            self.set_font("Times", "I", 9)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, f"{self.doc_type}  |  Draft", border=0, align="L")
            self.ln(4)
            # Thin separator line
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.2)
            self.line(20, self.get_y(), 190, self.get_y())
            self.ln(6)

    def footer(self):
        # Professional bottom footer on all pages
        self.set_y(-18)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.2)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(2)

        self.set_font("Times", "I", 8)
        self.set_text_color(100, 116, 139)
        # Left: Legal notice
        notice = f"{self.org_name}  |  Informational Draft - Not Certified Legal Advice"
        self.cell(120, 8, notice, border=0, align="L")
        # Right: Page X of Y
        page_str = f"Page {self.page_no()} of {{nb}}"
        self.cell(50, 8, page_str, border=0, align="R")


def _safe_latin1(text: str) -> str:
    """Ensure text is safely encodable for FPDF's standard Times-Roman font."""
    replacements = {
        "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
        "\u2013": "-", "\u2014": " - ", "\u2026": "...",
        "\u00a0": " ", "\u2022": "*", "\u25e6": "*",
        "§": "Sec.", "©": "(c)", "®": "(R)", "™": "(TM)",
        "€": "EUR", "£": "GBP", "¥": "JPY",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Filter out anything above latin-1 range to avoid encoding crashes
    return text.encode("latin-1", "replace").decode("latin-1")


def format_pdf(
    text: str,
    doc_type: str = "Legal Document",
    logo_path: Optional[Union[str, io.BytesIO]] = None,
    org_name: Optional[str] = None,
) -> bytes:
    """Format legal document into a professional PDF and return as bytes."""
    pdf = LegalPDF(doc_type=doc_type, org_name=org_name)
    pdf.add_page()

    # 1. Embed Logo if available
    resolved_logo = None
    if logo_path is not None:
        resolved_logo = logo_path
    elif os.path.exists(DEFAULT_LOGO_PATH):
        resolved_logo = str(DEFAULT_LOGO_PATH)

    if resolved_logo is not None:
        try:
            # Place logo centered on page 1
            # A4 page width = 210mm. Logo width = 65mm -> X = (210 - 65) / 2 = 72.5mm
            pdf.image(resolved_logo, x=72.5, y=18, w=65)
            pdf.set_y(40)
        except Exception:
            pdf.set_y(22)
    else:
        pdf.set_y(22)

    # 2. Document Title
    lines = text.split("\n")
    title = doc_type
    first_heading = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("# "):
            first_heading = stripped.lstrip("#").strip()
            break
    if first_heading:
        title = first_heading

    safe_title = _safe_latin1(title).upper()
    pdf.set_font("Times", "B", 15)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, safe_title, border=0, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # 3. Parse and Render Document Body
    in_signature_section = False
    sig_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            pdf.ln(3)
            continue

        # Skip the title line since already rendered
        if (stripped.startswith("## ") or stripped.startswith("# ")) and first_heading and first_heading in stripped:
            continue

        # Check for signature section
        if "IN WITNESS WHEREOF" in stripped.upper() or ("SIGNATURE" in stripped.upper() and "___" in stripped):
            in_signature_section = True
            pdf.ln(4)
            pdf.set_font("Times", "BI", 11)
            pdf.set_text_color(30, 41, 59)
            clean_hdr = _safe_latin1(stripped.replace("**", "").replace("##", "").replace("###", "").strip())
            pdf.multi_cell(0, 6, clean_hdr)
            pdf.ln(4)
            continue

        if in_signature_section:
            sig_lines.append(stripped)
            continue

        # Section Heading
        if stripped.startswith("### ") or stripped.startswith("## "):
            pdf.ln(4)
            heading_txt = _safe_latin1(stripped.lstrip("#").strip())
            pdf.set_font("Times", "B", 12)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 6, heading_txt)
            pdf.ln(2)
            continue

        # Numbered list item
        num_match = re.match(r'^(\d+[\.\)])\s+(.*)', stripped)
        if num_match:
            prefix = num_match.group(1)
            item_text = _safe_latin1(num_match.group(2).replace("**", ""))
            pdf.set_font("Times", "", 10.5)
            pdf.set_text_color(30, 41, 59)
            # Indent numbered items
            pdf.set_x(26)
            full_text = f"{prefix}  {item_text}"
            pdf.multi_cell(160, 5.5, full_text, align="J")
            pdf.ln(2)
            continue

        # Bullet list item
        if re.match(r'^[\*\-]\s+', stripped):
            bullet_text = _safe_latin1(re.sub(r'^[\*\-]\s+', '', stripped).replace("**", ""))
            pdf.set_font("Times", "", 10.5)
            pdf.set_text_color(30, 41, 59)
            pdf.set_x(28)
            pdf.multi_cell(158, 5.5, f"-  {bullet_text}", align="J")
            pdf.ln(1.5)
            continue

        # Standard Paragraph
        pdf.set_font("Times", "", 10.5)
        pdf.set_text_color(30, 41, 59)
        clean_para = _safe_latin1(stripped.replace("**", ""))
        pdf.multi_cell(0, 5.5, clean_para, align="J")
        pdf.ln(2)

    # 4. Render Signature Block
    _build_pdf_signatures(pdf, sig_lines)

    return bytes(pdf.output())


def _build_pdf_signatures(pdf: LegalPDF, sig_lines: list):
    """Render a clean 2-column signature block in the PDF."""
    # Ensure there is enough space on page for signatures (at least 55mm)
    if pdf.get_y() > 220:
        pdf.add_page()
    else:
        pdf.ln(6)

    col_w = 78
    start_y = pdf.get_y()

    # Column 1 (Party 1)
    pdf.set_font("Times", "", 9.5)
    pdf.set_text_color(51, 65, 85)

    pdf.set_xy(22, start_y)
    pdf.cell(col_w, 5, "____________________________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(22)
    pdf.cell(col_w, 5, "Authorized Signature", new_x="LEFT", new_y="NEXT")
    pdf.set_x(22)
    pdf.cell(col_w, 5, "Print Name: _______________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(22)
    pdf.cell(col_w, 5, "Title: ____________________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(22)
    pdf.cell(col_w, 5, "Date: _____________________________", new_x="LEFT", new_y="NEXT")

    # Column 2 (Party 2)
    pdf.set_xy(108, start_y)
    pdf.cell(col_w, 5, "____________________________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(108)
    pdf.cell(col_w, 5, "Authorized Signature", new_x="LEFT", new_y="NEXT")
    pdf.set_x(108)
    pdf.cell(col_w, 5, "Print Name: _______________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(108)
    pdf.cell(col_w, 5, "Title: ____________________________", new_x="LEFT", new_y="NEXT")
    pdf.set_x(108)
    pdf.cell(col_w, 5, "Date: _____________________________", new_x="LEFT", new_y="NEXT")

    pdf.ln(8)
