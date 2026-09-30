import datetime
import io
import os
import requests
import streamlit as st
from PIL import Image

from document_utils.docx_generator import format_docx
from document_utils.pdf_generator import format_pdf
from document_utils.txt_generator import format_txt
from document_utils.formatter import format_html_preview
from utils.sanitizer import sanitize_text
from utils.config import (
    APP_NAME,
    APP_SUBTITLE,
    BACKEND_URL,
    DEFAULT_LOGO_PATH,
    INVERSE_LOGO_PATH,
    LEGAL_DISCLAIMER,
    is_gemini_configured,
)
from ai_core.gemini_generator import GeminiDocumentGenerator

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_NAME} - {APP_SUBTITLE}",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom Styling to match the elegant legal aesthetic from specification
st.markdown(
    """
    <style>
    /* Global font and container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 860px;
    }
    
    /* Header typography */
    h1, h2, h3 {
        font-family: 'Georgia', serif;
    }
    
    /* Custom preview container */
    .legal-preview-card {
        background-color: #0f172a;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 28px 36px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        font-family: 'Georgia', serif;
        margin-top: 15px;
        margin-bottom: 25px;
        max-height: 600px;
        overflow-y: auto;
    }

    /* Disclaimer box */
    .disclaimer-banner {
        background-color: #1e293b;
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 20px;
        color: #cbd5e1;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* Demo badge */
    .demo-badge {
        background-color: #065f46;
        color: #a7f3d0;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }

    .live-badge {
        background-color: #1e3a8a;
        color: #bfdbfe;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Initialize Session State
# -----------------------------------------------------------------------------
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None
if "document_type" not in st.session_state:
    st.session_state.document_type = "Employment Contract"
if "is_demo" not in st.session_state:
    st.session_state.is_demo = False
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False
if "org_name" not in st.session_state:
    st.session_state.org_name = ""

# Check Backend Status
def check_backend_status():
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=1.5)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

health_info = check_backend_status()
is_live_gemini = health_info.get("gemini_configured", False) if health_info else is_gemini_configured()

# -----------------------------------------------------------------------------
# Header Section (Activity 4.1 Step 1 & 2)
# -----------------------------------------------------------------------------
logo_to_display = INVERSE_LOGO_PATH if os.path.exists(INVERSE_LOGO_PATH) else DEFAULT_LOGO_PATH
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(logo_to_display):
        st.image(str(logo_to_display), use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align: center;'>⚖️ {APP_NAME}</h1>", unsafe_allow_html=True)

st.markdown(
    f"<h3 style='text-align: center; color: #94a3b8; font-weight: normal; margin-top: -12px; margin-bottom: 18px;'>"
    f"{APP_SUBTITLE}</h3>",
    unsafe_allow_html=True,
)

# Mandatory Legal Disclaimer Banner
st.markdown(
    f"<div class='disclaimer-banner'><strong>LEGAL NOTICE:</strong> {LEGAL_DISCLAIMER}</div>",
    unsafe_allow_html=True,
)

# Demo Mode Indicator Banner
if not is_live_gemini:
    st.markdown(
        "<div style='background-color: #172554; border-left: 4px solid #3b82f6; padding: 10px 14px; border-radius: 4px; margin-bottom: 20px; font-size: 0.88rem; color: #bfdbfe;'>"
        "<strong>💡 Demo Mode Active:</strong> No Gemini API key detected. Realistic document drafting templates "
        "will be generated deterministically without consuming API credits. Configure <code>GEMINI_API_KEY</code> in <code>.env</code> to activate live Gemini AI."
        "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='background-color: #064e3b; border-left: 4px solid #10b981; padding: 10px 14px; border-radius: 4px; margin-bottom: 20px; font-size: 0.88rem; color: #a7f3d0;'>"
        f"<strong>✨ Live Gemini AI Active:</strong> Connected to model <code>{health_info.get('model', 'gemini-1.5-pro')}</code>."
        "</div>",
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Preset Samples Loader for Quick Testing
# -----------------------------------------------------------------------------
SAMPLE_PRESETS = {
    "Freelance Work Contract": {
        "doc_type": "Freelance Work Contract",
        "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
        "terms": "Work must be delivered by May 15, 2025; Payment of $4,500 will be made within 7 days of invoice; The client retains intellectual property rights upon full payment; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice",
        "date": datetime.date(2025, 4, 15),
    },
    "Non-Disclosure Agreement (NDA)": {
        "doc_type": "Non-Disclosure Agreement (NDA)",
        "parties": "Apex Innovations LLC (Disclosing Party), Nexus Software Solutions (Receiving Party)",
        "terms": "Confidential information includes proprietary algorithms, customer databases, and product roadmaps; Information shall not be disclosed to third parties without prior written consent; Confidentiality obligations shall endure for 3 years from effective date; Exclusions apply to public knowledge or court subpoenas",
        "date": datetime.date.today(),
    },
    "Employment Contract": {
        "doc_type": "Employment Contract",
        "parties": "John Smith (Employee), Cyberdyne Systems Corp. (Employer)",
        "terms": "Position of Senior Systems Architect; Base annual salary of $130,000 paid bi-weekly; Standard health insurance and 20 days paid annual leave; 30 days mutual written notice required for termination without cause; Strict non-solicitation of clients for 12 months post-employment",
        "date": datetime.date.today(),
    },
    "Residential Lease Agreement": {
        "doc_type": "Residential Lease Agreement",
        "parties": "Robert Miller (Landlord), Sarah Connor (Tenant)",
        "terms": "Premises located at 742 Evergreen Terrace; Monthly rent of $1,800 due on the 1st of each month; Security deposit of $1,800 refundable upon move-out; Pets permitted subject to $250 non-refundable fee; Tenant responsible for utility charges",
        "date": datetime.date.today(),
    },
}

with st.expander("⚡ Load Pre-configured Sample Scenarios (Optional)", expanded=False):
    preset_cols = st.columns(len(SAMPLE_PRESETS))
    for i, (name, data) in enumerate(SAMPLE_PRESETS.items()):
        if preset_cols[i].button(name, key=f"preset_{i}", use_container_width=True):
            st.session_state.selected_preset = data
            st.rerun()

# Apply preset if clicked
active_preset = st.session_state.pop("selected_preset", None)

# -----------------------------------------------------------------------------
# Input Form Section
# -----------------------------------------------------------------------------
st.markdown("### 📋 Document Specifications")

# Step 1: Document Type
doc_types = [
    "Freelance Work Contract",
    "Non-Disclosure Agreement (NDA)",
    "Employment Contract",
    "Residential Lease Agreement",
    "Service Agreement",
    "Employment Offer Letter",
    "General Agreement",
    "Custom Document",
]

default_doc_idx = 0
if active_preset and active_preset["doc_type"] in doc_types:
    default_doc_idx = doc_types.index(active_preset["doc_type"])

selected_type = st.selectbox(
    "1. Document Type",
    options=doc_types,
    index=default_doc_idx,
    help="Select the type of legal agreement you want to generate.",
)

if selected_type == "Custom Document":
    custom_title = st.text_input("Specify Document Title:", value="Consulting Agreement")
    final_doc_type = custom_title.strip() if custom_title.strip() else "Custom Legal Document"
else:
    final_doc_type = selected_type

# Step 2: Parties Involved
default_parties = active_preset["parties"] if active_preset else "Jane Doe (Service Provider), TechNova Inc. (Client)"
parties_input = st.text_area(
    "2. Parties Involved",
    value=default_parties,
    height=85,
    placeholder="e.g., Jane Doe (Service Provider), TechNova Inc. (Client)",
    help="Enter the names and contractual roles of all participating parties.",
)

# Step 3: Terms and Conditions
default_terms = (
    active_preset["terms"]
    if active_preset
    else "Payment to be made within 30 days of invoice; The provider agrees to deliver work by the agreed deadline; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice"
)
terms_input = st.text_area(
    "3. Terms & Conditions (Use semicolons for bullet points)",
    value=default_terms,
    height=120,
    placeholder="e.g., Payment within 30 days; Confidentiality must be maintained; 15 days written notice required",
    help="Enter agreed terms, clauses, or covenants. Separate individual points with semicolons (;).",
)

# Step 4: Effective Date
default_date = active_preset["date"] if active_preset else datetime.date.today()
effective_date_val = st.date_input(
    "4. Effective Date",
    value=default_date,
    help="The date on which the agreement takes legal effect.",
)
formatted_date = effective_date_val.strftime("%B %d, %Y")

# Step 5: Optional Branding & Customization
with st.expander("🎨 Optional Branding (Custom Logo & Organization Name)", expanded=False):
    brand_col1, brand_col2 = st.columns([1, 1])
    with brand_col1:
        org_name_input = st.text_input(
            "Organization / Company Name (for Header & Footer):",
            value=st.session_state.org_name,
            placeholder="e.g., TechNova Solutions LLC",
        )
        if org_name_input != st.session_state.org_name:
            st.session_state.org_name = org_name_input
    with brand_col2:
        uploaded_logo = st.file_uploader(
            "Upload Custom Logo (PNG / JPG):",
            type=["png", "jpg", "jpeg"],
            help="Your logo will be embedded at the top of DOCX and PDF exports.",
        )
        if uploaded_logo:
            st.image(uploaded_logo, caption="Preview of custom logo", width=180)

# -----------------------------------------------------------------------------
# Step 6: Generate Document
# -----------------------------------------------------------------------------
generate_btn = st.button("🚀 Generate Document", type="primary", use_container_width=True)

if generate_btn:
    # Validate fields
    if not parties_input.strip():
        st.error("Please enter the parties involved.")
    elif not terms_input.strip():
        st.error("Please enter terms and conditions.")
    else:
        with st.spinner("⚖️ LegalEase is drafting your legal document..."):
            # Call backend API
            payload = {
                "document_type": final_doc_type,
                "parties": parties_input.strip(),
                "terms": terms_input.strip(),
                "dates": formatted_date,
            }

            generated_content = None
            is_demo = False

            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=30,
                )
                if response.status_code == 200:
                    data = response.json()
                    generated_content = data.get("content")
                    is_demo = data.get("is_demo", False)
                else:
                    err_msg = response.json().get("detail", "API generation error")
                    st.error(f"Generation error: {err_msg}")
            except Exception as net_err:
                # Direct in-process fallback if backend server is not running
                st.warning("Backend API server not responding directly; using direct in-process generator.")
                gen = GeminiDocumentGenerator()
                ok, text, is_demo, err = gen.generate_document(
                    document_type=final_doc_type,
                    parties=parties_input.strip(),
                    terms=terms_input.strip(),
                    dates=formatted_date,
                )
                if ok:
                    generated_content = text
                else:
                    st.error(err or "Document generation failed.")

            if generated_content:
                st.session_state.generated_text = generated_content
                st.session_state.document_type = final_doc_type
                st.session_state.is_demo = is_demo
                st.session_state.show_edit = False
                st.success("✅ Document Generated Successfully!")
                st.rerun()

# -----------------------------------------------------------------------------
# Step 7: Document Preview & Edit Mode (Activity 4.2)
# -----------------------------------------------------------------------------
if st.session_state.generated_text:
    st.markdown("---")
    st.markdown("### 📄 Generated Document")

    # Status / Demo notification
    if st.session_state.is_demo:
        st.markdown(
            "<span class='demo-badge'>DEMO MODE GENERATION</span> "
            "<small style='color: #94a3b8;'>This document was generated using deterministic legal drafting templates.</small>",
            unsafe_allow_html=True,
        )

    # Edit toggle button
    edit_col1, edit_col2 = st.columns([1, 1])
    with edit_col1:
        edit_label = "🔒 View Styled Preview" if st.session_state.show_edit else "✏️ Click to Edit Document"
        if st.button(edit_label, use_container_width=True):
            st.session_state.show_edit = not st.session_state.show_edit
            st.rerun()
    with edit_col2:
        if st.button("🔄 Start New Document", use_container_width=True):
            st.session_state.generated_text = None
            st.session_state.show_edit = False
            st.rerun()

    # Edit Mode View
    if st.session_state.show_edit:
        st.markdown("#### Edit Document Below:")
        edited_content = st.text_area(
            "Document Editor",
            value=st.session_state.generated_text,
            height=420,
            label_visibility="collapsed",
            key="doc_editor_area",
        )
        if st.button("💾 Save Changes", type="secondary"):
            st.session_state.generated_text = sanitize_text(edited_content)
            st.session_state.show_edit = False
            st.success("Changes saved successfully!")
            st.rerun()
    else:
        # Styled HTML preview card (as specified in PDF page 14)
        styled_html = format_html_preview(st.session_state.generated_text)
        st.markdown(f"<div class='legal-preview-card'>{styled_html}</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Step 8: Multi-Format Download Options (Activity 4.2 Step 4)
    # -------------------------------------------------------------------------
    st.markdown("### 💾 Export & Download")

    clean_file_title = st.session_state.document_type.replace(" ", "_").replace("/", "_").lower()

    # Resolve logo for exports
    custom_logo_data = None
    if uploaded_logo is not None:
        custom_logo_data = io.BytesIO(uploaded_logo.getvalue())
    elif os.path.exists(DEFAULT_LOGO_PATH):
        custom_logo_data = str(DEFAULT_LOGO_PATH)

    org_to_use = st.session_state.org_name.strip() if st.session_state.org_name else None

    # Generate export binaries
    txt_data = format_txt(st.session_state.generated_text, st.session_state.document_type)
    
    try:
        docx_data = format_docx(
            text=st.session_state.generated_text,
            doc_type=st.session_state.document_type,
            logo_path=custom_logo_data,
            org_name=org_to_use,
        )
    except Exception as e:
        docx_data = None
        st.warning(f"DOCX preparation note: {e}")

    try:
        pdf_data = format_pdf(
            text=st.session_state.generated_text,
            doc_type=st.session_state.document_type,
            logo_path=custom_logo_data,
            org_name=org_to_use,
        )
    except Exception as e:
        pdf_data = None
        st.warning(f"PDF preparation note: {e}")

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        st.download_button(
            label="📄 Download as .TXT",
            data=txt_data,
            file_name=f"{clean_file_title}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with dl_col2:
        if docx_data:
            st.download_button(
                label="📘 Download as .DOCX",
                data=docx_data,
                file_name=f"{clean_file_title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

    with dl_col3:
        if pdf_data:
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_data,
                file_name=f"{clean_file_title}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
    "LegalEase Inc. | contact@legalease.com | All Rights Reserved.<br>"
    "Informational draft document generation platform. Consult certified legal counsel for jurisdictional validation."
    "</div>",
    unsafe_allow_html=True,
)
