"""
LegalEase Streamlit Frontend
AI-Powered Legal Document Generator Interface
Provides an interactive, high-fidelity legal document drafting, editing, previewing, and exporting experience.
"""

import os
import sys
import io
import datetime
import requests
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Ensure root workspace is in sys.path for direct utility access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.utils.text_utils import sanitize_text, count_words, parse_terms
from backend.utils.document_formatter import generate_docx, format_html_preview, parse_document_sections
from backend.utils.pdf_generator import generate_pdf

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="LegalEase – AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished Legal-Tech SaaS Aesthetic
CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

    /* Global Tweaks */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #fef3c7, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 0.4rem;
        font-weight: 400;
    }
    .hero-badge {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Disclaimer Alert Box */
    .disclaimer-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #92400e;
        padding: 0.9rem 1.2rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        line-height: 1.45;
        margin-bottom: 1.5rem;
    }

    /* Card styling for inputs */
    .form-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
    }

    /* Metric Cards */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.2rem;
    }
    .metric-pill {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1.2rem;
        flex: 1;
        text-align: center;
    }
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
    }

    /* Legal Paper HTML Preview */
    .legal-doc-sheet {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
        padding: 3rem 3.5rem;
        color: #1e293b;
        font-family: 'Merriweather', Georgia, serif;
        line-height: 1.8;
        font-size: 0.96rem;
        position: relative;
        max-height: 700px;
        overflow-y: auto;
    }
    .doc-watermark {
        position: absolute;
        top: 20px;
        right: 25px;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #94a3b8;
        border: 1px solid #cbd5e1;
        padding: 3px 8px;
        border-radius: 4px;
    }
    .doc-title {
        font-family: 'Cinzel', serif;
        font-size: 1.6rem;
        text-align: center;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.8rem;
    }
    .doc-h2 {
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .doc-h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #334155;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
    }
    .doc-p {
        margin-bottom: 0.9rem;
        text-align: justify;
    }
    .doc-bullet-list {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    .doc-bullet-list li {
        margin-bottom: 0.4rem;
    }
    .doc-spacer {
        height: 0.8rem;
    }
    .doc-sig-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.05rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #0f172a;
    }
    .doc-sig-line {
        font-family: monospace;
        color: #475569;
        margin: 0.5rem 0;
    }
    .doc-sig-p {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .doc-disclaimer-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #b45309;
        text-transform: uppercase;
        margin-top: 2.5rem;
        border-top: 1px dashed #cbd5e1;
        padding-top: 1rem;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Preset Templates for Fast Input
DOCUMENT_PRESETS = {
    "Non-Disclosure Agreement (NDA)": {
        "type": "NDA",
        "parties": "Apex Innovations LLC (Disclosing Party), Quantum Dynamics Inc. (Receiving Party)",
        "terms": "Confidentiality duration of 3 years from effective date; Use of proprietary data strictly limited to evaluating business partnership; Return or destruction of confidential materials within 14 days of written demand; Governing law of the State of Delaware; Injunction relief available upon breach without posting bond.",
    },
    "Employment Offer Letter": {
        "type": "Employment Offer Letter",
        "parties": "Summit Software Corp (Employer), Alex Mercer (Candidate / Employee)",
        "terms": "Position of Senior Full Stack Engineer; Annual base salary of $135,000 USD paid bi-weekly; Standard health, dental, and 401(k) benefits starting Day 1; At-will employment relationship; 15 days paid time off per calendar year; Offer valid for acceptance within 7 business days.",
    },
    "Employment Contract": {
        "type": "Employment Contract",
        "parties": "Vanguard Media Group (Employer), Sarah Jenkins (Executive Employee)",
        "terms": "Term of employment: 2 years renewable; Base salary of $160,000 plus 20% annual performance bonus; Non-solicitation of clients and staff for 12 months post-termination; 30 days written notice required for voluntary resignation; Intellectual property assignment clause for all work created during employment.",
    },
    "Freelance Work Contract": {
        "type": "Freelance Work Contract",
        "parties": "David Sterling (Independent Contractor / Designer), BrightPeak Labs (Client)",
        "terms": "Project scope: Complete Brand Identity & Design System; Fixed fee of $6,500 with 50% upfront deposit and 50% upon final delivery; Client receives full intellectual property rights upon receipt of full payment; Maximum of 3 revision rounds included; Contractor is an independent contractor and not an employee.",
    },
    "Lease Agreement": {
        "type": "Lease Agreement",
        "parties": "Oakridge Properties LLC (Landlord), Marcus Vance (Tenant)",
        "terms": "Premises: 742 Evergreen Terrace, Unit 4B; Lease term: 12 months; Monthly rent: $2,200 due on the 1st of each month; Security deposit: $2,200 refundable upon move-out inspection; No smoking allowed inside premises; Small pets allowed with $300 one-time pet deposit.",
    },
    "Agreement": {
        "type": "Agreement",
        "parties": "Skyline Logistics Inc. (Service Provider), Horizon Retail Group (Customer)",
        "terms": "Provision of nationwide warehousing and fulfillment services; Payment terms: Net 30 days upon invoice issuance; Standard service level agreement of 99.5% on-time dispatch; Either party may terminate with 60 days advance written notice.",
    },
    "Contract": {
        "type": "Contract",
        "parties": "Prime Builders Ltd. (General Contractor), Metro Realty Partners (Owner)",
        "terms": "Commercial building renovation project; Total contract price: $450,000 paid in monthly milestone disbursements; Completion deadline: 180 calendar days; Contractor to maintain comprehensive general liability insurance of $2,000,000.",
    },
    "Custom Legal Document": {
        "type": "Custom Legal Document",
        "parties": "Party A (First Party), Party B (Second Party)",
        "terms": "Mutual collaboration on designated initiative; Confidentiality of exchanged technical specifications; Equal split of gross revenue generated from joint products; Dispute resolution through binding arbitration.",
    },
}

DOCUMENT_TYPES_LIST = [
    "Agreement",
    "Contract",
    "NDA",
    "Lease Agreement",
    "Employment Offer Letter",
    "Employment Contract",
    "Freelance Work Contract",
    "Custom Legal Document",
]

# Initialize Session State
if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = ""
if "edited_doc" not in st.session_state:
    st.session_state.edited_doc = ""
if "doc_metadata" not in st.session_state:
    st.session_state.doc_metadata = {}
if "selected_preset" not in st.session_state:
    st.session_state.selected_preset = "Non-Disclosure Agreement (NDA)"


def main():
    # Render Hero Banner
    st.markdown(
        """
        <div class="hero-banner">
            <div>
                <h1 class="hero-title">LegalEase</h1>
                <div class="hero-subtitle">AI-Powered Legal Document Generator & Drafting Workspace</div>
            </div>
            <div>
                <span class="hero-badge">⚖️ Gemini Powered</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mandatory Legal Disclaimer
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>⚠️ Legal Safety Notice:</strong> LegalEase generates AI-assisted legal document drafts for informational purposes only. It does not provide legal advice. Please have the document reviewed and approved by a qualified legal professional before signing or using it.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Controls
    with st.sidebar:
        st.markdown("### ⚙️ Workspace Settings")

        # Preset Loader
        st.markdown("#### 📋 Quick Templates")
        selected_preset_key = st.selectbox(
            "Load Sample Template:",
            options=list(DOCUMENT_PRESETS.keys()),
            index=0,
            help="Choose a pre-filled sample template to quickly test document generation.",
        )
        preset_data = DOCUMENT_PRESETS[selected_preset_key]

        # Backend URL Configuration
        st.markdown("---")
        st.markdown("#### 🔗 API Connection")
        backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
        backend_input = st.text_input("FastAPI Backend URL:", value=backend_url)

        # Test API Connection Status
        api_status = "Unknown"
        try:
            res = requests.get(f"{backend_input.rstrip('/')}/", timeout=2)
            if res.status_code == 200:
                api_status = "🟢 Connected (FastAPI)"
            else:
                api_status = f"🟡 Status {res.status_code}"
        except Exception:
            api_status = "🔴 Offline (Using Direct AI Engine)"

        st.caption(f"Server Status: **{api_status}**")

        st.markdown("---")
        st.markdown("#### ℹ️ About LegalEase")
        st.caption(
            "LegalEase formats legal documents into high-resolution DOCX and PDF documents "
            "with customizable branding, smart formatting, and live in-browser editing."
        )

    # Main Input Form in Tabs or Columns
    st.markdown("### 📝 1. Document Specifications")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Document Type Selection
        default_type_idx = 0
        if preset_data["type"] in DOCUMENT_TYPES_LIST:
            default_type_idx = DOCUMENT_TYPES_LIST.index(preset_data["type"])

        doc_type = st.selectbox(
            "Document Type *",
            options=DOCUMENT_TYPES_LIST,
            index=default_type_idx,
            help="Select the category of legal document you need.",
        )

        # Effective Date Picker
        effective_date_val = st.date_input(
            "Effective Date *",
            value=datetime.date.today(),
            help="The legal effective start date of the agreement.",
        )
        effective_date_str = effective_date_val.strftime("%B %d, %Y")

        # Parties Involved
        parties_input = st.text_area(
            "Parties Involved *",
            value=preset_data["parties"],
            height=90,
            help="Specify the names, organizations, and legal capacities of all participating parties.",
            placeholder="e.g. Jane Doe (Service Provider), TechNova Inc. (Client)",
        )

    with col2:
        # Terms and Conditions
        terms_input = st.text_area(
            "Terms & Conditions (Semicolon or newline separated) *",
            value=preset_data["terms"],
            height=165,
            help="Enter specific clauses, milestones, payment terms, or conditions separated by semicolons (;).",
            placeholder="e.g. Payment within 30 days; Confidentiality for 3 years; Termination with 15 days notice.",
        )

        # Logo Upload
        logo_file = st.file_uploader(
            "Optional Organization Logo (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            help="Upload your company or firm logo to embed in generated DOCX and PDF documents.",
        )

        logo_bytes = None
        if logo_file is not None:
            logo_bytes = logo_file.getvalue()
            st.image(logo_bytes, caption="Uploaded Logo Preview", width=160)

    # Generation Button Action
    generate_btn = st.button("🚀 Generate Document Draft", type="primary", use_container_width=True)

    if generate_btn:
        if not parties_input.strip():
            st.error("Please specify the parties involved before generating.")
            return
        if not terms_input.strip():
            st.error("Please specify at least one term or condition before generating.")
            return

        with st.spinner("🤖 Consulting Gemini AI and drafting professional legal clauses..."):
            generated_content = ""
            error_encountered = None

            # Attempt 1: Call FastAPI Backend
            try:
                payload = {
                    "document_type": doc_type,
                    "parties": parties_input.strip(),
                    "terms": terms_input.strip(),
                    "effective_date": effective_date_str,
                }
                api_endpoint = f"{backend_input.rstrip('/')}/generate"
                response = requests.post(api_endpoint, json=payload, timeout=45)
                if response.status_code == 200:
                    data = response.json()
                    generated_content = data.get("document", "")
                else:
                    error_detail = response.json().get("detail", response.text)
                    error_encountered = f"Backend error ({response.status_code}): {error_detail}"
            except Exception as net_err:
                error_encountered = f"Backend connection issue ({net_err}). Attempting direct AI generation..."

            # Attempt 2: Direct AI Generator Fallback if backend wasn't reached or returned error
            if not generated_content:
                try:
                    from backend.ai_core.gemini_generator import GeminiDocumentGenerator
                    generator = GeminiDocumentGenerator()
                    generated_content = generator.generate(
                        document_type=doc_type,
                        parties=parties_input.strip(),
                        terms=terms_input.strip(),
                        effective_date=effective_date_str,
                    )
                except Exception as direct_err:
                    st.error(f"Generation Failed: {direct_err}")
                    if "GEMINI_API_KEY" in str(direct_err):
                        st.info("💡 Make sure to set `GEMINI_API_KEY` in your `.env` file.")
                    return

            # Save in session state
            st.session_state.generated_doc = generated_content
            st.session_state.edited_doc = generated_content
            st.session_state.doc_metadata = {
                "document_type": doc_type,
                "parties": parties_input.strip(),
                "terms": terms_input.strip(),
                "effective_date": effective_date_str,
                "logo_bytes": logo_bytes,
            }
            st.success("✨ Legal document draft generated successfully!")

    # Display Document Workspace if document exists
    if st.session_state.edited_doc:
        st.markdown("---")
        st.markdown("### 📄 2. Document Workspace & Export")

        # Metadata Metrics Bar
        current_text = st.session_state.edited_doc
        words = count_words(current_text)
        meta = st.session_state.doc_metadata
        doc_t = meta.get("document_type", "Legal Document")
        eff_d = meta.get("effective_date", "N/A")
        terms_count = len(parse_terms(meta.get("terms", "")))

        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-pill">
                    <div class="metric-label">Document Type</div>
                    <div class="metric-value">{doc_t}</div>
                </div>
                <div class="metric-pill">
                    <div class="metric-label">Effective Date</div>
                    <div class="metric-value">{eff_d}</div>
                </div>
                <div class="metric-pill">
                    <div class="metric-label">Word Count</div>
                    <div class="metric-value">{words:,}</div>
                </div>
                <div class="metric-pill">
                    <div class="metric-label">Key Terms Included</div>
                    <div class="metric-value">{terms_count}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tabbed Viewer: Formatted Preview vs Interactive Live Editor
        tab_preview, tab_editor, tab_analysis = st.tabs([
            "👁️ Formatted Document Preview",
            "✏️ Edit Document Text",
            "📊 Structured Analysis",
        ])

        with tab_preview:
            html_markup = format_html_preview(st.session_state.edited_doc)
            st.markdown(html_markup, unsafe_allow_html=True)

        with tab_editor:
            st.info("💡 You can edit the draft below in real time. All download buttons will use your EDITED text.")
            edited_area = st.text_area(
                "Document Text Editor",
                value=st.session_state.edited_doc,
                height=500,
                key="doc_editor_textarea",
                help="Make any changes or customizations directly here before exporting.",
            )
            # Update state if changed
            if edited_area != st.session_state.edited_doc:
                st.session_state.edited_doc = edited_area
                st.rerun()

        with tab_analysis:
            sections = parse_document_sections(st.session_state.edited_doc)
            st.markdown(f"**Document Title:** {sections['title']}")
            if sections['preamble']:
                st.markdown("**Preamble / Recitals:**")
                st.caption(sections['preamble'])
            if sections['clauses']:
                st.markdown("**Operative Clauses Summary:**")
                st.caption(f"{len(sections['clauses'].splitlines())} lines of contractual provisions.")
            if sections['signatures']:
                st.markdown("**Signature Block:**")
                st.text(sections['signatures'])

        # Export Actions Section
        st.markdown("#### 📥 3. Download Customized Document")

        # Export file name base
        base_filename = f"{doc_t.lower().replace(' ', '_')}_{datetime.date.today().strftime('%Y%m%d')}"

        col_txt, col_docx, col_pdf = st.columns(3)

        # 1. TXT Export
        with col_txt:
            txt_content = sanitize_text(st.session_state.edited_doc)
            st.download_button(
                label="📄 Download Plain Text (.txt)",
                data=txt_content.encode("utf-8"),
                file_name=f"{base_filename}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        # 2. DOCX Export
        with col_docx:
            try:
                docx_bytes = generate_docx(
                    document_text=st.session_state.edited_doc,
                    document_type=doc_t,
                    effective_date=eff_d,
                    parties=meta.get("parties", ""),
                    logo_bytes=meta.get("logo_bytes"),
                )
                st.download_button(
                    label="📘 Download Word (.docx)",
                    data=docx_bytes,
                    file_name=f"{base_filename}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            except Exception as docx_err:
                st.error(f"DOCX preparation error: {docx_err}")

        # 3. PDF Export
        with col_pdf:
            try:
                pdf_bytes = generate_pdf(
                    document_text=st.session_state.edited_doc,
                    document_type=doc_t,
                    effective_date=eff_d,
                    parties=meta.get("parties", ""),
                    logo_bytes=meta.get("logo_bytes"),
                )
                st.download_button(
                    label="📕 Download PDF (.pdf)",
                    data=pdf_bytes,
                    file_name=f"{base_filename}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as pdf_err:
                st.error(f"PDF preparation error: {pdf_err}")


if __name__ == "__main__":
    main()
