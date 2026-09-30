import re
import unicodedata


def sanitize_text(text: str) -> str:
    """Sanitize and normalize user input and AI generated text.
    
    - Normalizes Unicode typographic characters (smart quotes, dashes, spaces).
    - Removes non-printable/malicious control characters.
    - Preserves all valid legal punctuation, bullets, brackets, and currency signs.
    - Prevents dangerous HTML/script injection while preserving valid angle brackets.
    - Normalizes line endings to standard Unix style (\\n).
    """
    if not text:
        return ""

    if not isinstance(text, str):
        text = str(text)

    # 1. Normalize unicode compatibility characters
    # We avoid NFKD because it can strip legal symbols (e.g. §, ©, ®, ™)
    # Instead, we do targeted character mapping.
    replacements = {
        # Smart double quotes
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u201e': '"',  # Double low-9 quotation mark
        '\u201f': '"',  # Double high-reversed-9 quotation mark
        '\u00ab': '"',  # Left-pointing double angle quotation mark
        '\u00bb': '"',  # Right-pointing double angle quotation mark
        
        # Smart single quotes and apostrophes
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201a': "'",  # Single low-9 quotation mark
        '\u201b': "'",  # Single high-reversed-9 quotation mark
        '\u0060': "'",  # Grave accent
        '\u00b4': "'",  # Acute accent
        
        # Dashes and hyphens
        '\u2013': '-',  # En dash
        '\u2014': ' - ',  # Em dash
        '\u2015': ' - ',  # Horizontal bar
        '\u2212': '-',  # Minus sign
        
        # Spaces and invisible characters
        '\u00a0': ' ',  # Non-breaking space
        '\u2002': ' ',  # En space
        '\u2003': ' ',  # Em space
        '\u2009': ' ',  # Thin space
        '\u202f': ' ',  # Narrow no-break space
        '\u200b': '',   # Zero-width space
        '\u200c': '',   # Zero-width non-joiner
        '\u200d': '',   # Zero-width joiner
        '\ufeff': '',   # Zero-width no-break space (BOM)
        
        # Bullets
        '\u2022': '*',  # Bullet
        '\u2023': '*',  # Triangular bullet
        '\u25e6': '*',  # White bullet
        '\u2043': '-',  # Hyphen bullet
        
        # Ellipsis
        '\u2026': '...', # Horizontal ellipsis
    }

    for orig, rep in replacements.items():
        text = text.replace(orig, rep)

    # 2. Normalize newlines (\r\n -> \n, \r -> \n)
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # 3. Strip null bytes and non-printable control characters (keep \n, \t)
    def clean_char(char: str) -> str:
        code = ord(char)
        # Keep newline (10), tab (9)
        if code in (10, 9):
            return char
        # Filter out other C0 and C1 control codes
        if (0 <= code < 32) or (127 <= code < 160):
            return ''
        return char

    text = ''.join(clean_char(c) for c in text)

    # 4. Remove dangerous executable HTML tags like <script> or <iframe or javascript:
    text = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript\s*:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)

    # 5. Trim trailing whitespace from lines, collapse multiple horizontal spaces, and limit excessive newlines
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    cleaned_text = '\n'.join(lines)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

    return cleaned_text.strip()

