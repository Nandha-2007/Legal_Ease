# 4. Demo Video Recording Guide — LegalEase

This guide outlines recommendations and recording checklists for producing an effective video demonstration of LegalEase.

---

## 1. Technical Recording Specifications
- **Recommended Tools**: OBS Studio, Loom, Camtasia, or Windows Game Bar (`Win + G`).
- **Resolution**: 1920x1080 (1080p Full HD) at 30 or 60 FPS.
- **Audio Quality**: External USB/headset microphone with background noise suppression.
- **Target Video Length**: 5 to 7 minutes.

---

## 2. Pre-Recording Preparation Checklist
- [ ] Both servers are running:
  - FastAPI: `http://127.0.0.1:8000`
  - Streamlit: `http://localhost:8501`
- [ ] Browser window is sized to 100% zoom with clean bookmarks/tabs hidden.
- [ ] Virtual environment is active in terminal.
- [ ] A sample logo (e.g. `assets/logo/logo.png`) is ready on the desktop for the branding demonstration.
- [ ] Pytest test suite has been run and terminal displays `17 passed`.

---

## 3. Recommended Video Storyboard & Flow

| Segment | Video Action | Narration Focus |
| :--- | :--- | :--- |
| **01. Intro** | Show LegalEase homepage with brand logo and legal disclaimer banner. | Introduce the problem (legal costs, boilerplate rigidity) and LegalEase's value proposition. |
| **02. Form Walkthrough** | Click sample preset "Freelance Work Contract"; show inputs populating. | Explain document types, parties format, and semicolon terms parsing. |
| **03. Branding** | Expand branding panel, upload custom logo, and enter company name. | Show how custom branding integrates with output documents. |
| **04. Generation** | Click "Generate Document"; show loading spinner and generated preview. | Point out structured recitals, numbered terms, and signature lines in the preview card. |
| **05. Live Editing** | Click "Edit Document", modify a term, and click "Save Changes". | Demonstrate in-browser editing and real-time state synchronization. |
| **06. Exports** | Download TXT, DOCX, and PDF; open each in Word and Acrobat/Browser. | Highlight 1-inch margins, Times New Roman, logo embedding, running headers, and page numbering. |
| **07. Architecture** | Switch to terminal or Swagger UI (`http://127.0.0.1:8000/docs`). | Explain FastAPI routing, Pydantic validation, Gemini AI, and zero-key Demo Mode. |
| **08. Testing** | Run `pytest -v` in terminal showing 17 passed tests. | Demonstrate test coverage and code reliability. |
| **09. Conclusion** | Return to browser, summarize disclaimer and concluding remarks. | Thank the audience and conclude. |
