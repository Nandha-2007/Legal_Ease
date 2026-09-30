import re
from typing import Union


def format_txt(text: str, doc_type: str = "") -> bytes:
    """Format legal document into clean plain text and return as UTF-8 bytes.
    
    Preserves:
    - Title
    - Sections
    - Paragraphs
    - Bullet points
    - Signature information
    """
    if not text:
        return b""

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Headings: convert ## Heading to uppercase with separator
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            cleaned_lines.append("")
            cleaned_lines.append("=" * max(40, len(heading)))
            cleaned_lines.append(heading.upper())
            cleaned_lines.append("=" * max(40, len(heading)))
            cleaned_lines.append("")
        elif stripped.startswith("### "):
            heading = stripped[4:].strip()
            cleaned_lines.append("")
            cleaned_lines.append(f"--- {heading} ---")
            cleaned_lines.append("")
        elif stripped.startswith("# "):
            heading = stripped[2:].strip()
            cleaned_lines.append("")
            cleaned_lines.append("=" * max(40, len(heading)))
            cleaned_lines.append(heading.upper())
            cleaned_lines.append("=" * max(40, len(heading)))
            cleaned_lines.append("")
        else:
            # Strip bold markdown markers like **text**
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', stripped)
            # Normalize bullet points
            if re.match(r'^[\*\-]\s+', clean_line):
                clean_line = "  * " + re.sub(r'^[\*\-]\s+', '', clean_line)
            cleaned_lines.append(clean_line)

    result_text = "\n".join(cleaned_lines).strip() + "\n\n"
    # Append legal notice
    result_text += (
        "\n------------------------------------------------------------\n"
        "[LegalEase Draft Document - Informational & Drafting Purposes Only]\n"
    )

    return result_text.encode("utf-8")
