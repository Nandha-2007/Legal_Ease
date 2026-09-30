import html
import re
from typing import List


def parse_terms(terms_raw: str) -> List[str]:
    """Parse raw terms input (semicolon or newline separated) into a clean list of terms."""
    if not terms_raw:
        return []
    # Replace newlines with semicolons first
    normalized = terms_raw.replace("\r\n", ";").replace("\n", ";")
    # Split by semicolon
    items = [item.strip() for item in normalized.split(";") if item.strip()]
    # Strip any leading bullets or numbers like '- ', '* ', '1. '
    cleaned = []
    for item in items:
        clean_item = re.sub(r'^\s*([*\-•]|\d+[\.)])\s*', '', item)
        if clean_item:
            cleaned.append(clean_item)
    return cleaned if cleaned else [terms_raw.strip()]


def format_html_preview(text: str) -> str:
    """Convert generated legal document markdown text into elegant semantic HTML

    suitable for inline Streamlit preview.
    """
    if not text:
        return "<p><em>No document content available.</em></p>"

    # Escape HTML to prevent XSS while allowing our controlled formatting
    escaped = html.escape(text)

    # Process line by line
    lines = escaped.split("\n")
    html_parts = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<div style='height: 12px;'></div>")
            continue

        # Check for Level 2 heading (Title or main section)
        if stripped.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            title = stripped[3:].strip()
            html_parts.append(
                f"<h2 style='color: #60a5fa; font-family: \"Georgia\", serif; text-align: center; "
                f"margin-top: 18px; margin-bottom: 12px; border-bottom: 2px solid #3b82f6; "
                f"padding-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;'>{title}</h2>"
            )
            continue

        # Check for Level 3 heading (Section headings)
        if stripped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            section = stripped[4:].strip()
            html_parts.append(
                f"<h4 style='color: #93c5fd; font-family: \"Georgia\", serif; margin-top: 16px; "
                f"margin-bottom: 6px; font-weight: bold; border-left: 3px solid #60a5fa; "
                f"padding-left: 8px;'>{section}</h4>"
            )
            continue

        # Check for Level 1 heading
        if stripped.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            title = stripped[2:].strip()
            html_parts.append(
                f"<h1 style='color: #60a5fa; font-family: \"Georgia\", serif; text-align: center; "
                f"margin-top: 20px; margin-bottom: 14px;'>{title}</h1>"
            )
            continue

        # Check for bullet points (* or -)
        if re.match(r'^[\*\-]\s+', stripped):
            if not in_list:
                html_parts.append("<ul style='margin-left: 20px; color: #e2e8f0; line-height: 1.6;'>")
                in_list = True
            bullet_text = re.sub(r'^[\*\-]\s+', '', stripped)
            # Format bold text
            bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #f8fafc;">\1</strong>', bullet_text)
            html_parts.append(f"<li style='margin-bottom: 6px;'>{bullet_text}</li>")
            continue

        # Check for numbered list (1. 2. etc.)
        if re.match(r'^\d+[\.\)]\s+', stripped):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            item_text = re.sub(r'^\d+[\.\)]\s+', '', stripped)
            match = re.match(r'^(\d+[\.\)])\s+', stripped)
            prefix = match.group(1) if match else "•"
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #f8fafc;">\1</strong>', item_text)
            html_parts.append(
                f"<div style='margin-left: 14px; margin-bottom: 8px; color: #e2e8f0; line-height: 1.6;'>"
                f"<strong style='color: #93c5fd;'>{prefix}</strong> {item_text}</div>"
            )
            continue

        # If we were in a list, close it
        if in_list:
            html_parts.append("</ul>")
            in_list = False

        # Regular paragraph or signature line
        p_text = stripped
        # Format bold tags
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #f8fafc;">\1</strong>', p_text)

        # Style signature underscores
        if "___" in p_text:
            p_text = re.sub(r'(_+)', r'<span style="color: #94a3b8; letter-spacing: -1px;">\1</span>', p_text)
            html_parts.append(f"<div style='font-family: monospace; margin-top: 10px; color: #cbd5e1;'>{p_text}</div>")
        else:
            html_parts.append(
                f"<p style='color: #cbd5e1; font-family: \"Georgia\", serif; line-height: 1.7; "
                f"margin-bottom: 8px; text-align: justify;'>{p_text}</p>"
            )

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)
