# User Operating Manual — LegalEase

Welcome to **LegalEase: AI-Powered Legal Document Generator**. This manual guides you through generating, customizing, editing, and downloading legal documents.

---

## 1. Getting Started

### 1.1 Accessing the Application
1. Ensure the servers are running:
   - FastAPI Backend: `http://127.0.0.1:8000`
   - Streamlit Frontend: `http://localhost:8501`
2. Open your web browser and navigate to `http://localhost:8501`.

---

## 2. Generating a Document (Step-by-Step)

### Step 1: Choose Document Type
- Select a predefined document type from the dropdown:
  - `Freelance Work Contract`
  - `Non-Disclosure Agreement (NDA)`
  - `Employment Contract`
  - `Residential / Commercial Lease Agreement`
  - `Service Agreement`
  - `Employment Offer Letter`
  - `General Agreement`
- Or select `Custom Document` and specify your desired title.

### Step 2: Specify the Involved Parties
- In the **Parties Involved** text box, enter the full names and contractual designations of the parties:
  ```text
  Jane Doe (Service Provider), TechNova Inc. (Client)
  ```

### Step 3: Define Terms & Conditions
- Enter your agreed business terms into the **Terms & Conditions** box.
- **Tip**: Separate distinct points using **semicolons (`;`)**:
  ```text
  Work delivered by May 15, 2025; Payment of $4,500 within 7 days; Confidentiality strictly preserved; Either party may terminate with 15 days notice
  ```

### Step 4: Pick Effective Date
- Select the agreement's commencement date using the interactive date picker.

### Step 5: Optional Branding (Logo & Organization Name)
- Expand the **🎨 Optional Branding** section:
  - Enter your organization's legal name for headers and footers.
  - Upload your corporate logo (`.png`, `.jpg`, `.jpeg`).

### Step 6: Click "Generate Document"
- Click **🚀 Generate Document**. LegalEase will assemble and draft the contract.

---

## 3. Reviewing & Editing Your Document

### 3.1 Styled Preview
- Once generated, your document appears in a formatted dark-card preview container with section headings and signature lines.

### 3.2 In-Line Editing
1. Click **✏️ Click to Edit Document**.
2. Modify or add clauses directly inside the editor box.
3. Click **💾 Save Changes**. The preview and export files update immediately.

---

## 4. Downloading the Finalized Document

Under the **💾 Export & Download** section, select your desired format:
- **📄 Download as .TXT**: Clean plain text for quick copying or text archives.
- **📘 Download as .DOCX**: Formatted Microsoft Word file with 1-inch margins, embedded logo, and signature tables.
- **📕 Download as .PDF**: Print-ready PDF file with running headers, footers, and page numbers (`Page X of Y`).

To start a new draft, click **🔄 Start New Document**.
