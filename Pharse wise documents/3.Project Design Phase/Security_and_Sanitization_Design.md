# 4. Security & Sanitization Design — LegalEase

This document outlines the threat modeling, defensive controls, sanitization pipeline, and privacy safeguards engineered into LegalEase.

---

## 1. Threat Modeling (STRIDE Analysis)

| Threat Category | Potential Risk Vector | Applied Mitigation in LegalEase |
| :--- | :--- | :--- |
| **Spoofing** | Attacker impersonating legitimate API clients. | CORS middleware restricted in production; request origin validation. |
| **Tampering** | Malicious injection of executable scripts or malformed HTML in legal fields. | Multi-stage regex sanitization (`sanitize_text()`) neutralizing script and iframe tags. |
| **Repudiation** | Disputes regarding terms entered by parties. | Mandatory legal disclaimer emphasizing draft status and need for attorney execution. |
| **Information Disclosure** | Leakage of Gemini API key through error stacks or client-side inspection. | Secret keys isolated in `.env`; errors masked to generic user-facing messages. |
| **Denial of Service** | Extremely large payloads designed to consume excessive RAM during generation. | Strict Pydantic max-length constraints (e.g. 10,000 char limit on terms). |
| **Elevation of Privilege** | Remote code execution via unsafe file deserialization or eval. | No dynamic code evaluation (`eval` / `exec`); safe memory-only byte streams. |

---

## 2. Text Sanitization Pipeline (`utils/sanitizer.py`)

```
   Raw User Input / AI Output
               │
               ▼
   [Stage 1: Unicode Normalization]
   • Smart double quotes (“ ” „ « ») ──────► Standard ASCII Quote (")
   • Smart single quotes (‘ ’ ‚ ` ´) ──────► Standard ASCII Apostrophe (')
   • Typographic dashes (— – ‒ −)   ──────► Standard Hyphen (-)
   • Non-breaking / Zero-width spaces ─────► Standard Single Space
               │
               ▼
   [Stage 2: Control Code Neutralization]
   • Null bytes (\x00) stripped
   • C0/C1 control codes removed (retains \n, \t)
   • Line breaks normalized (\r\n ──► \n)
               │
               ▼
   [Stage 3: XSS & Code Injection Neutralization]
   • <script>...</script> tags removed
   • <iframe>...</iframe> tags removed
   • javascript: pseudo-protocols stripped
   • on[event]= attributes removed
               │
               ▼
   [Stage 4: Legal Syntax Preservation]
   • Brackets preserved: [Party A], (Client), {Section}
   • Legal symbols preserved: §, ©, ®, ™, $, €, £
   • Punctuation preserved: ;, :, ,, ., -, *
               │
               ▼
   [Stage 5: Whitespace Normalization]
   • Consecutive horizontal whitespace collapsed
   • Excessive empty lines (>2) reduced
               │
               ▼
     Sanitized Clean String
```

---

## 3. Anti-Hallucination Prompt Architecture

To prevent generative models from inventing legal authorities, laws, or personal details, `ai_core/gemini_generator.py` enforces a two-tier defense:

1. **System Instruction**:
   > *"You are a legal document drafting assistant. Generate structured draft documents from the user's supplied information. Do not fabricate facts, statutes, case law, legal citations, or missing details. Clearly mark missing information with placeholders (such as [Address], [State/Jurisdiction], [Title]) instead of inventing it. This output is a draft for informational purposes and should be reviewed by a qualified legal professional where appropriate."*

2. **Negative Prompting Constraints**:
   - Explicit prohibition against generating fictitious addresses, phone numbers, or identification numbers.
   - Prohibition against quoting specific legal statutes or case citations.
   - Strict requirement to enclose unknown jurisdictional details in square brackets `[Jurisdiction]`.

---

## 4. Secret Isolation & Zero-Leakage Architecture

- **`.env` File**: Secrets are read exclusively at server startup via `utils/config.py`.
- **`.gitignore` Enforcement**: Standard rule-set guarantees that `.env` and local credentials can never be accidentally committed to public git repositories.
- **Error Shielding**: If Gemini API returns an authentication failure or quota exhaustion, internal stack traces and bearer tokens are intercepted by `routes.py`, and the client receives a clean, non-revealing error message.
