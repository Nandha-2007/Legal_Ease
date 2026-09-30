# Developer Guide & Extension Manual — LegalEase

This document provides development instructions for extending the LegalEase platform, customizing document templates, configuring models, and adding new export features.

---

## 1. Development Environment Setup

### 1.1 Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate       # Windows PowerShell
source venv/bin/activate      # Linux / macOS
pip install -r requirements.txt
```

### 1.2 Environment Configuration
Copy `.env.example` to `.env`:
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
```

---

## 2. Extending Predefined Document Types
To add a new document type (e.g. "Partnership Agreement"):
1. In `app.py`, append the new title to `doc_types`:
   ```python
   doc_types = [
       ...,
       "Partnership Agreement",
       "Custom Document",
   ]
   ```
2. In `ai_core/gemini_generator.py`, update `_generate_demo_document()` to provide a deterministic fallback template for partnership agreements.

---

## 3. Customizing Prompt Instructions
To adjust anti-hallucination rules or clause structure:
1. Open `ai_core/gemini_generator.py`.
2. Edit `SYSTEM_INSTRUCTION` or `build_prompt()`.
3. Re-run tests:
   ```bash
   pytest tests/test_ai_generator.py -v
   ```

---

## 4. Modifying Document Styling
- **Word (.DOCX)**: Edit `document_utils/docx_generator.py` to adjust fonts, margin sizes (`Inches(1.0)`), and signature table styling.
- **PDF (.PDF)**: Edit `document_utils/pdf_generator.py` to customize headers, footers, margins, and page numbering.
