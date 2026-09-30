import pytest
from utils.sanitizer import sanitize_text
from document_utils.formatter import parse_terms, format_html_preview


def test_sanitize_text_normalizes_typographic_quotes_and_dashes():
    raw = '“Agreement” between ‘Party A’ and ‘Party B’ — with terms – and… dots.'
    sanitized = sanitize_text(raw)
    assert '"Agreement"' in sanitized
    assert "'Party A'" in sanitized
    assert "'Party B'" in sanitized
    assert " - " in sanitized
    assert "..." in sanitized


def test_sanitize_text_strips_script_injection():
    malicious = 'Party A <script>alert("hacked")</script> and Party B'
    sanitized = sanitize_text(malicious)
    assert "<script>" not in sanitized
    assert "alert" not in sanitized
    assert "Party A and Party B" in sanitized


def test_sanitize_text_preserves_legal_brackets_and_punctuation():
    legal_text = (
        "Agreement made between [Company Name] (hereinafter referred to as \"Client\"); "
        "Fee: $10,000 (100% due upon completion); Section § 4.2 applies."
    )
    sanitized = sanitize_text(legal_text)
    assert "[Company Name]" in sanitized
    assert "$10,000" in sanitized
    assert ";" in sanitized
    assert "§" in sanitized


def test_parse_terms_semicolon_separated():
    terms_raw = "Payment within 30 days; Confidentiality strictly kept; 15 days notice"
    parsed = parse_terms(terms_raw)
    assert len(parsed) == 3
    assert parsed[0] == "Payment within 30 days"
    assert parsed[1] == "Confidentiality strictly kept"
    assert parsed[2] == "15 days notice"


def test_parse_terms_handles_bullets_and_newlines():
    terms_raw = "- First term here\n* Second term here\n3. Third term here"
    parsed = parse_terms(terms_raw)
    assert len(parsed) == 3
    assert "First term here" in parsed[0]
    assert "Second term here" in parsed[1]
    assert "Third term here" in parsed[2]


def test_format_html_preview():
    doc_markdown = (
        "## Non-Disclosure Agreement\n\n"
        "This Agreement is between Party A and Party B.\n\n"
        "### 1. Obligations\n"
        "* Keep information secret\n"
        "* Do not disclose\n\n"
        "____________________________________\n"
        "Authorized Signature"
    )
    html_output = format_html_preview(doc_markdown)
    assert "<h2" in html_output
    assert "NON-DISCLOSURE AGREEMENT" in html_output.upper()
    assert "<h4" in html_output
    assert "1. Obligations" in html_output
    assert "<li" in html_output
    assert "Keep information secret" in html_output
