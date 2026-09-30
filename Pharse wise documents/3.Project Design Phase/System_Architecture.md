# 1. System Architecture Design — LegalEase

This document specifies the technical architecture, component decomposition, data flow diagrams (DFD), and runtime sequence diagrams for LegalEase.

---

## 1. High-Level Architectural Diagram

```mermaid
flowchart TD
    Client["Browser / Client (User)"]
    
    subgraph UI ["Frontend Layer (Streamlit: app.py)"]
        Form["Input Form (Type, Parties, Terms, Dates)"]
        Brand["Branding Module (Logo Uploader, Org Name)"]
        PreviewCard["Preview Card (Dark-Themed HTML)"]
        Editor["In-Line Editor (st.text_area)"]
        Downloads["Download Hub (.TXT, .DOCX, .PDF)"]
    end
    
    subgraph Backend ["Backend Layer (FastAPI: main.py, routes.py)"]
        Router["APIRouter (/generate, /health)"]
        Validator["Pydantic Validation (DocumentRequest)"]
        Sanitizer["Sanitization Engine (sanitize_text)"]
    end
    
    subgraph AI ["AI Generation Engine (ai_core/)"]
        Decision{"API Key Configured?"}
        GeminiCall["Google Gemini 1.5 Pro API"]
        DemoGen["Deterministic Demo Engine"]
    end
    
    subgraph Exporters ["Document Formatting Suite (document_utils/)"]
        TXT["TXT Exporter (format_txt)"]
        DOCX["DOCX Exporter (format_docx)"]
        PDF["PDF Exporter (format_pdf)"]
        HTML["HTML Formatter (format_html_preview)"]
    end

    Client -->|User Inputs| Form
    Form -->|POST /generate JSON| Router
    Router --> Validator
    Validator --> Sanitizer
    Sanitizer --> Decision
    
    Decision -->|Yes| GeminiCall
    Decision -->|No| DemoGen
    
    GeminiCall -->|Generated Content| Router
    DemoGen -->|Structured Template| Router
    
    Router -->|JSON Response| UI
    UI --> HTML
    HTML --> PreviewCard
    PreviewCard <-->|Edit Toggle| Editor
    
    Editor --> Downloads
    Downloads --> TXT
    Downloads --> DOCX
    Downloads --> PDF
    
    TXT -->|File Stream| Client
    DOCX -->|File Stream| Client
    PDF -->|File Stream| Client
```

---

## 2. Component Decomposition

1. **Frontend Layer (`app.py`)**:
   - Manages UI components, state (`st.session_state`), and user interactions.
   - Dispatches HTTP requests to the FastAPI backend or triggers direct in-process generation if the server is starting.
   - Coordinates file downloads using in-memory byte streams (`io.BytesIO`).

2. **Backend API Layer (`main.py`, `routes.py`)**:
   - Built on FastAPI with ASGI server Uvicorn.
   - Enforces CORS policies, routing, and lifecycle logging.
   - Validates request payloads with Pydantic (`DocumentRequest`).

3. **AI Core Layer (`ai_core/gemini_generator.py`)**:
   - Configures the `google-generativeai` SDK.
   - Implements anti-hallucination prompt construction and negative constraints.
   - Houses the deterministic mock engine for zero-configuration Demo Mode.

4. **Document Formatting Layer (`document_utils/`)**:
   - `txt_generator.py`: Generates UTF-8 encoded plain text with capitalized headers.
   - `docx_generator.py`: Assembles Microsoft Word files with Times New Roman typography, 1-inch margins, signature tables, and footers.
   - `pdf_generator.py`: Builds multi-page PDFs using `fpdf2` with running headers, footers, and page numbers.
   - `formatter.py`: Converts markdown text to semantic, dark-themed HTML preview elements.

5. **Utility Layer (`utils/`)**:
   - `sanitizer.py`: Normalizes typographic quotes, removes control characters, and neutralizes XSS vectors.
   - `config.py`: Loads environment variables and provides central configuration access.

---

## 3. Data Flow Diagram (DFD Level 1)

```
[User] ──(1. Submit Inputs)──► [Frontend] ──(2. JSON Request)──► [Input Sanitizer]
                                                                        │
                                                                 (3. Clean Strings)
                                                                        ▼
[User] ◄──(7. Download Binary)── [Exporters] ◄──(6. Edited Text)── [Pydantic Validator]
                                     ▲                                  │
                                     │                           (4. Valid Model)
                              (5. Draft Text)                           ▼
                                     └────────────────────────── [AI / Demo Engine]
```

---

## 4. Runtime Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as Streamlit (app.py)
    participant Backend as FastAPI (routes.py)
    participant Sanitizer as utils.sanitizer
    participant AI as ai_core.gemini_generator
    participant Gemini as Google Gemini API
    participant Exporters as document_utils

    User->>Frontend: Enters doc type, parties, terms, date
    User->>Frontend: Clicks "Generate Document"
    Frontend->>Backend: POST /generate (JSON Payload)
    Backend->>Sanitizer: sanitize_text(inputs)
    Sanitizer-->>Backend: Cleaned strings
    Backend->>AI: generate_document(clean_inputs)
    
    alt API Key Configured
        AI->>Gemini: generate_content(prompt)
        Gemini-->>AI: Raw text response
    else Demo Mode (No Key)
        AI->>AI: _generate_demo_document()
    end
    
    AI-->>Backend: (success, content, is_demo)
    Backend-->>Frontend: HTTP 200 {success, document_type, content, is_demo}
    Frontend->>Exporters: format_html_preview(content)
    Exporters-->>Frontend: Styled HTML string
    Frontend-->>User: Renders dark-card preview

    opt User Edits Document
        User->>Frontend: Clicks "Edit Document"
        User->>Frontend: Modifies text & clicks "Save Changes"
        Frontend->>Frontend: Updates st.session_state.generated_text
    end

    User->>Frontend: Clicks "Download as .DOCX / .PDF / .TXT"
    Frontend->>Exporters: format_docx / format_pdf / format_txt
    Exporters-->>Frontend: Binary bytes stream
    Frontend-->>User: File downloaded to browser
```
