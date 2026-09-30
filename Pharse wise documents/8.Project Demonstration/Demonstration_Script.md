# 1. Project Demonstration Script — LegalEase

This script provides a structured narration guide for demonstrating LegalEase in live reviews, video recordings, or client showcases.

---

## 1. Demonstration Timing & Outline

| Timestamp | Segment | Key Talking Points & Actions |
| :--- | :--- | :--- |
| **00:00 - 01:00** | Introduction & Problem | Introduce LegalEase as an AI-powered legal document generator solving high legal fees and boilerplate rigidity. |
| **01:00 - 02:30** | Input Form & Presets | Walk through Step 1 (Document Type), Step 2 (Parties), Step 3 (Semicolon Terms), Step 4 (Date), and Step 5 (Branding). |
| **02:30 - 04:00** | Generation & Preview | Click "Generate Document", highlight loading spinner, show styled dark-card preview, and demonstrate live in-line editing. |
| **04:00 - 05:30** | Multi-Format Exports | Download and inspect `.TXT`, `.DOCX` (tables & logo), and `.PDF` (running headers, footers, page numbering). |
| **05:30 - 07:00** | Backend & AI Core | Explain FastAPI backend (`/generate`), Gemini anti-hallucination prompt, and zero-key Demo Mode. |
| **07:00 - 08:00** | Testing & Conclusion | Display passing 17-test suite (`pytest`), reiterate legal disclaimers, and summarize project outcomes. |

---

## 2. Speaker Narration Script

### Part 1: Introduction (00:00 - 01:00)
> *"Hello everyone! Welcome to the demonstration of **LegalEase — AI-Powered Legal Document Generator**. Every entrepreneur, freelancer, and small business owner understands the friction of drafting routine legal contracts. Hiring attorneys is expensive, while static online templates break when you need custom terms. LegalEase bridges this gap by combining modern Generative AI with a robust Python backend to draft personalized, professional-grade contracts in seconds."*

### Part 2: Input Configuration & Branding (01:00 - 02:30)
> *"Here on the home page, you see a clean, professional interface. Notice the prominent legal disclaimer reminding users that this is an informational drafting aid. We can choose from standard document types like NDAs, Employment Contracts, or Leases. To demonstrate, let's click our quick-load preset for a **Freelance Work Contract**. Notice how our parties and semicolon-separated terms populate automatically. We can also upload our custom company logo and set our entity name."*

### Part 3: Generation & Live Editing (02:30 - 04:00)
> *"Now we click **Generate Document**. The request is sent to our FastAPI backend, sanitized, and processed. Instantly, our contract appears in this elegant, dark-themed preview card with serif legal typography, recitals, numbered clauses, and signature blocks. If we need to modify a clause, we click **Click to Edit Document**, make our edits directly in the text area, and click **Save Changes**. The preview updates seamlessly."*

### Part 4: Multi-Format Downloads (04:00 - 05:30)
> *"Next, let's explore exports. LegalEase supports three distinct formats:
> 1. Plain text `.txt` with clean section borders and disclaimers.
> 2. Microsoft Word `.docx` featuring 1-inch margins, Times New Roman typography, our brand logo, running footers, and a 2-column signature table.
> 3. PDF `.pdf` generated using `fpdf2`, featuring running headers, dynamic `Page X of Y` page numbers, and clean multi-page flow."*

### Part 5: Testing & Conclusion (05:30 - 07:00)
> *"Under the hood, LegalEase is powered by FastAPI, Pydantic validation, and Google Gemini with strict anti-hallucination rules. And if no API key is provided, our deterministic Demo Mode ensures 100% functionality without crashes. Our automated test suite of 17 tests passes with a 100% success rate. Thank you!"*
