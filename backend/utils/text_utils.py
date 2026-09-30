"""
LegalEase Text Utility Functions
Provides text sanitization, term parsing, word counting, and formatting helpers.
"""

import re
import unicodedata
from typing import List


def sanitize_text(text: str) -> str:
    """
    Cleans and normalizes text by replacing non-standard typographic characters,
    smart quotes, em-dashes, non-breaking spaces, and unprintable characters.
    Ensures safe compatibility across ASCII, UTF-8, DOCX, and PDF generators.
    """
    if not text:
        return ""

    # Normalize unicode characters
    cleaned = unicodedata.normalize("NFKC", text)

    # Replace smart quotes and apostrophes
    quote_replacements = {
        "\u2018": "'",  # Left single quotation mark
        "\u2019": "'",  # Right single quotation mark
        "\u201a": "'",  # Single low-9 quotation mark
        "\u201b": "'",  # Single high-reversed-9 quotation mark
        "\u201c": '"',  # Left double quotation mark
        "\u201d": '"',  # Right double quotation mark
        "\u201e": '"',  # Double low-9 quotation mark
        "\u201f": '"',  # Double high-reversed-9 quotation mark
        "\u00ab": '"',  # Left-pointing double angle quotation mark
        "\u00bb": '"',  # Right-pointing double angle quotation mark
        "\u2039": "'",  # Single left-pointing angle quotation mark
        "\u203a": "'",  # Single right-pointing angle quotation mark
        "`": "'",       # Backtick to single quote
        "´": "'",       # Acute accent
    }
    for old, new in quote_replacements.items():
        cleaned = cleaned.replace(old, new)

    # Replace dashes, bullets, and ellipses
    symbol_replacements = {
        "\u2013": "-",   # En dash
        "\u2014": " -- ", # Em dash
        "\u2015": " -- ", # Horizontal bar
        "\u2022": "*",   # Bullet
        "\u2023": "*",   # Triangular bullet
        "\u25aa": "*",   # Black small square
        "\u25cf": "*",   # Black circle
        "\u2026": "...", # Horizontal ellipsis
        "\u00a0": " ",   # Non-breaking space
        "\u200b": "",    # Zero-width space
        "\u200e": "",    # Left-to-right mark
        "\u200f": "",    # Right-to-left mark
        "\ufeff": "",    # Byte order mark (BOM)
        "\r\n": "\n",    # Windows newline normalization
        "\r": "\n",      # Mac OS classic newline
    }
    for old, new in symbol_replacements.items():
        cleaned = cleaned.replace(old, new)

    # Remove non-printable control characters (except newline, tab)
    cleaned = "".join(ch for ch in cleaned if ch in ("\n", "\t") or (unicodedata.category(ch)[0] != "C" and ord(ch) >= 32))

    # Clean markdown fences if model returned ```markdown ... ```
    cleaned = strip_markdown_fences(cleaned)

    # Remove trailing/leading excessive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


def strip_markdown_fences(text: str) -> str:
    """
    Strips wrapping markdown code fences (e.g. ```markdown ... ``` or ``` ...) if present.
    """
    if not text:
        return ""
    text_stripped = text.strip()
    if text_stripped.startswith("```"):
        # Remove opening fence like ```markdown or ```
        text_stripped = re.sub(r"^```[a-zA-Z]*\n?", "", text_stripped)
        # Remove closing fence
        text_stripped = re.sub(r"\n?```$", "", text_stripped.strip())
    return text_stripped.strip()


def parse_terms(terms_raw: str) -> List[str]:
    """
    Parses a string of raw terms (separated by semicolons, newlines, or numbered bullets)
    into a clean list of individual condition strings.
    """
    if not terms_raw:
        return []

    # Split by semicolon first or newline if no semicolons
    if ";" in terms_raw:
        chunks = [c.strip() for c in terms_raw.split(";")]
    else:
        chunks = [c.strip() for c in terms_raw.split("\n")]

    parsed: List[str] = []
    for chunk in chunks:
        # Strip numbering prefix like "1. ", "2) ", "- "
        cleaned_chunk = re.sub(r"^\s*(\d+[\.\)]|\-|\*)\s*", "", chunk).strip()
        if cleaned_chunk:
            # Ensure proper capitalization and punctuation
            if not cleaned_chunk.endswith((".", ";", ":")):
                cleaned_chunk += "."
            parsed.append(cleaned_chunk)

    return parsed


def count_words(text: str) -> int:
    """
    Returns the number of words in a given text.
    """
    if not text:
        return 0
    words = re.findall(r"\b\w+\b", text)
    return len(words)
