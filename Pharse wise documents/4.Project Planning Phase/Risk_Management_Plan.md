# 3. Risk Management Plan — LegalEase

This document identifies potential project, technical, operational, and legal risks, along with severity evaluations and proactive mitigation actions.

---

## 1. Risk Evaluation Matrix

```
       ▲ High   │    [R-02]               [R-01]
       │        │  (API Limits)        (Missing Key)
IMPACT │ Medium │                         [R-03]
       │        │                   (Font Encoding)
       │ Low    │    [R-05]               [R-04]
       │        │  (XSS Script)       (Late Re-runs)
       └────────┼──────────────────────────────────►
                  Low       Medium       High
                         PROBABILITY
```

---

## 2. Risk Register & Mitigation Strategy

| Risk ID | Category | Description | Prob / Imp | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | Technical | Missing or unconfigured Gemini API key causes server crash or unhandled runtime exceptions. | High / High | Engineered deterministic zero-key **Demo Mode** with realistic contractual templates; app never crashes without key. |
| **R-02** | Operational | Gemini API quota exhaustion or network timeout during generation requests. | Medium / High | Implemented exception shields in `ai_core` returning graceful, user-friendly messages rather than stack traces. |
| **R-03** | Technical | Unicode / typographic characters (smart quotes, em-dashes) break FPDF latin-1 font rendering. | Medium / Med | Developed `_safe_latin1()` mapping dictionary in `document_utils/pdf_generator.py` normalizing all special symbols. |
| **R-04** | Technical | Python package deprecation warnings (e.g. FPDF `ln=1` deprecation). | High / Low | Modernized to `fpdf2` syntax using explicit `new_x="LEFT", new_y="NEXT"` positional parameters. |
| **R-05** | Security | Malicious script or HTML injection submitted in party names or term clauses. | Low / Low | Multi-stage regex sanitization (`sanitize_text()`) completely strips `<script>`, `<iframe>`, and event handlers. |
| **R-06** | Legal | End-users mistake AI-generated drafts for certified legal counsel or enforceable attorney work. | Medium / High | Mandatory prominent disclaimer banners rendered on UI, in plain text footers, and within Word/PDF templates. |

---

## 3. Contingency Protocols

1. **Network Disconnection Protocol**: If the local FastAPI backend becomes temporarily unreachable, `app.py` automatically initiates an in-process direct generation fallback via `GeminiDocumentGenerator()`, preventing user disruption.
2. **API Key Revocation Protocol**: If an API key is revoked during active use, the system smoothly reverts to Demo Mode and logs technical diagnostics to the server console without leaking bearer tokens to the browser.
