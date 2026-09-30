"""
LegalEase PDF Generator
Generates clean, professional legal document PDFs using fpdf2.
Features customizable headers, footers, page numbering, dynamic logos, and legal styling.
"""

import io
import os
import re
import tempfile
from typing import Optional
from fpdf import FPDF
from .text_utils import sanitize_text


class LegalEasePDF(FPDF):
    """
    Custom FPDF class tailored for formal legal documents.
    """

    def __init__(self, document_title: str = "LEGAL DOCUMENT", logo_path: Optional[str] = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.document_title = document_title
        self.logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(left=20, top=20, right=20)
        # Enable total page count placeholder
        self.alias_nb_pages()

    def header(self):
        # Draw header only if not suppressed
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(120, 144, 156)  # Slate grey

        # Left header text
        self.cell(100, 6, "LEGALEASE | AI LEGAL DRAFT", align="L")

        # Right logo or small label
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                # Add logo in top-right corner
                self.image(self.logo_path, x=165, y=8, w=25)
            except Exception:
                pass

        self.ln(8)
        # Decorative divider line
        self.set_draw_color(220, 226, 235)
        self.set_line_width(0.3)
        self.line(20, 16, 190, 16)
        self.ln(6)

    def footer(self):
        # Position at 18 mm from bottom
        self.set_y(-18)
        # Decorative divider line
        self.set_draw_color(220, 226, 235)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(2)

        # Footer disclaimer
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(140, 150, 160)
        self.cell(
            130,
            4,
            "LegalEase Draft - Informational only. Consult legal counsel prior to execution.",
            align="L",
        )
        # Page numbering
        page_str = f"Page {self.page_no()} of {{nb}}"
        self.cell(40, 4, page_str, align="R")


def generate_pdf(
    document_text: str,
    document_type: str = "Legal Document",
    effective_date: str = "",
    parties: str = "",
    logo_bytes: Optional[bytes] = None,
) -> bytes:
    """
    Renders document_text into a high quality PDF byte stream.
    """
    sanitized_text = sanitize_text(document_text)

    temp_logo_path = None
    if logo_bytes:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(logo_bytes)
                temp_logo_path = tmp.name
        except Exception:
            temp_logo_path = None

    try:
        pdf = LegalEasePDF(
            document_title=document_type.upper(),
            logo_path=temp_logo_path,
        )
        pdf.add_page()

        # Document Title
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(15, 23, 42)  # Dark navy/slate
        title_text = document_type.upper() if document_type else "LEGAL DOCUMENT"
        pdf.cell(0, 10, title_text, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Metadata banner if available
        if effective_date or parties:
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(71, 85, 105)

            meta_lines = []
            if effective_date:
                meta_lines.append(f"Effective Date: {effective_date}")
            if parties:
                meta_lines.append(f"Parties: {parties}")

            meta_content = "  |  ".join(meta_lines)
            pdf.multi_cell(0, 6, meta_content, border=1, align="C", fill=True)
            pdf.ln(4)

        # Process lines and render sections
        lines = sanitized_text.split("\n")
        in_signature_block = False

        for line in lines:
            line_str = line.strip()

            if not line_str:
                pdf.ln(3)
                continue

            # Check for Major Section Headings (e.g. ## Heading, SECTION 1, ARTICLE I, etc.)
            is_main_heading = (
                line_str.startswith("# ")
                or line_str.startswith("## ")
                or line_str.isupper() and len(line_str) < 50
                or re.match(r"^(SECTION|ARTICLE|CLAUSE)\s+\d+", line_str, re.IGNORECASE)
            )

            is_sub_heading = (
                line_str.startswith("### ")
                or line_str.startswith("#### ")
                or (re.match(r"^\d+\.\s+[A-Z]", line_str) and len(line_str) < 60)
            )

            # Check if signature section
            if any(term in line_str.upper() for term in ["SIGNATURES", "IN WITNESS WHEREOF", "FOR AND ON BEHALF"]):
                in_signature_block = True

            if is_main_heading:
                clean_heading = re.sub(r"^#+\s*", "", line_str)
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(15, 23, 42)
                pdf.multi_cell(0, 7, clean_heading, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            elif is_sub_heading:
                clean_sub = re.sub(r"^#+\s*", "", line_str)
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10.5)
                pdf.set_text_color(30, 41, 59)
                pdf.multi_cell(0, 6, clean_sub, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            elif line_str.startswith("* ") or line_str.startswith("- ") or line_str.startswith("• "):
                # Bullet list item
                bullet_content = re.sub(r"^[\*\-•]\s*", "", line_str)
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(51, 65, 85)
                # Print bullet symbol
                pdf.set_x(25)
                pdf.multi_cell(145, 5.5, f"-  {bullet_content}", new_x="LMARGIN", new_y="NEXT")
            elif in_signature_block and ("___" in line_str or "Date:" in line_str or "By:" in line_str or "Name:" in line_str):
                # Signature line formatting
                pdf.set_font("Helvetica", "", 9.5)
                pdf.set_text_color(30, 41, 59)
                pdf.multi_cell(0, 5, line_str, new_x="LMARGIN", new_y="NEXT")
            else:
                # Regular paragraph text
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(51, 65, 85)
                pdf.multi_cell(0, 5.5, line_str, new_x="LMARGIN", new_y="NEXT")

        output_buffer = io.BytesIO()
        pdf.output(output_buffer)
        return output_buffer.getvalue()

    finally:
        if temp_logo_path and os.path.exists(temp_logo_path):
            try:
                os.remove(temp_logo_path)
            except Exception:
                pass
