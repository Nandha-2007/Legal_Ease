import logging
import os
from typing import Tuple, Optional
from utils.config import GEMINI_API_KEY, GEMINI_MODEL, is_gemini_configured
from utils.sanitizer import sanitize_text

logger = logging.getLogger("legalease.ai_core")

SYSTEM_INSTRUCTION = (
    "You are a legal document drafting assistant. Generate structured draft documents "
    "from the user's supplied information. Do not fabricate facts, statutes, case law, "
    "legal citations, or missing details. Clearly mark missing information with placeholders "
    "(such as [Address], [State/Jurisdiction], [Title]) instead of inventing it. "
    "This output is a draft for informational purposes and should be reviewed by a qualified "
    "legal professional where appropriate."
)


class GeminiDocumentGenerator:
    """Handles AI-powered legal document generation with Google Gemini,

    including an intelligent fallback Demo Mode when no API key is provided.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model_name = (model_name or GEMINI_MODEL or "gemini-1.5-pro").strip()
        self._is_configured = bool(self.api_key and len(self.api_key) > 5)
        self._model = None

        if self._is_configured:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                try:
                    self._model = genai.GenerativeModel(
                        model_name=self.model_name,
                        system_instruction=SYSTEM_INSTRUCTION,
                    )
                except Exception:
                    # Fallback for older SDK or models without system_instruction param
                    self._model = genai.GenerativeModel(model_name=self.model_name)
                logger.info(f"Gemini client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self._model = None

    @property
    def is_configured(self) -> bool:
        return self._is_configured and self._model is not None

    def build_prompt(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """Build a strict, structured legal drafting prompt for Gemini."""
        return (
            f"Generate a comprehensive, formal legal document titled '{document_type}'.\n\n"
            f"DETAILS PROVIDED BY THE USER:\n"
            f"- Document Type: {document_type}\n"
            f"- Involved Parties: {parties}\n"
            f"- Effective Date / Key Dates: {dates}\n"
            f"- Terms and Conditions: {terms}\n\n"
            f"DRAFTING INSTRUCTIONS:\n"
            f"1. Generate formal, unambiguous, and readable legal drafting tailored specifically to a '{document_type}'.\n"
            f"2. Structure the document with professional sections appropriate to this document type:\n"
            f"   - Title (formatted as: '## {document_type}')\n"
            f"   - Preamble / Recitals (stating agreement date and full party details)\n"
            f"   - Relevant numbered clauses (e.g., 1. Scope / Services / Purpose, 2. Terms and Obligations, "
            f"3. Consideration / Payment where relevant, 4. Confidentiality where relevant, "
            f"5. Term and Termination, 6. Governing Law, 7. Miscellaneous / Severability)\n"
            f"   - Signature Block (clearly labeled lines for each named party to sign, print name, date, and title)\n"
            f"3. Accurately integrate ALL user-provided terms. If the user provided semicolon-separated clauses, "
            f"expand and format each into clear, enforceable contractual terms.\n"
            f"4. DO NOT invent personal information (like fake home addresses, phone numbers, SSNs, or IDs).\n"
            f"5. DO NOT invent specific laws, court cases, statutory citations, or regulatory codes. "
            f"Use neutral standard phrasing like 'under the laws of [State/Jurisdiction]'.\n"
            f"6. Clearly mark any missing details requiring completion using square bracket placeholders like "
            f"[City, State, Zip Code] or [Insert Amount].\n"
            f"7. Return clean, structured plain text with standard Markdown headings (e.g. ## Title, 1. Section Name, - bullet points) "
            f"that formats cleanly for DOCX and PDF conversion.\n"
            f"8. Do not include markdown code block backticks (like ```markdown) around your entire response.\n"
        )

    def generate_document(
        self, document_type: str, parties: str, terms: str, dates: str
    ) -> Tuple[bool, str, bool, Optional[str]]:
        """Generate a legal document.

        Returns:
            Tuple of (success: bool, content: str, is_demo: bool, error: Optional[str])
        """
        # If API key is not configured, generate via structured Demo Mode
        if not self.is_configured:
            logger.info("Generating document via Demo Mode (no Gemini API key configured).")
            content = self._generate_demo_document(document_type, parties, terms, dates)
            return True, content, True, None

        prompt = self.build_prompt(document_type, parties, terms, dates)

        try:
            response = self._model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "max_output_tokens": 4096,
                },
            )

            if not response or not response.text:
                logger.error("Gemini returned empty response text.")
                return False, "", False, "Gemini returned an empty response. Please try again."

            cleaned = sanitize_text(response.text)
            # Remove enclosing markdown code fences if model wrapped the whole document
            if cleaned.startswith("```markdown"):
                cleaned = cleaned[len("```markdown"):].strip()
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()

            return True, cleaned, False, None

        except Exception as e:
            err_msg = str(e)
            logger.error(f"Error during Gemini generation: {err_msg}")
            # Sanitize error to avoid leaking keys
            safe_msg = "Document generation failed. Please check your API configuration or try again."
            if "quota" in err_msg.lower():
                safe_msg = "Gemini API quota exceeded. Please check your API quota or try again later."
            elif "api_key" in err_msg.lower() or "invalid argument" in err_msg.lower():
                safe_msg = "Invalid Gemini API key or configuration. Please check your .env settings."
            
            return False, "", False, safe_msg

    def _generate_demo_document(
        self, document_type: str, parties: str, terms: str, dates: str
    ) -> str:
        """Deterministic, highly realistic fallback generator for Demo Mode.

        Incorporates the user's inputs seamlessly into standard legal structures.
        """
        doc_type_clean = document_type.strip()
        parties_clean = parties.strip()
        dates_clean = dates.strip()

        # Parse terms into bulleted clauses
        term_items = [t.strip() for t in terms.replace("\n", ";").split(";") if t.strip()]
        if not term_items:
            term_items = [terms.strip()]

        terms_formatted = "\n".join(
            f"{i+1}. {item if item.endswith('.') else item + '.'}"
            for i, item in enumerate(term_items)
        )

        # Tailor document title and preamble based on document type
        lower_type = doc_type_clean.lower()

        if "nda" in lower_type or "non-disclosure" in lower_type:
            doc = (
                f"## Non-Disclosure Agreement (NDA)\n\n"
                f"This Non-Disclosure Agreement (the \"Agreement\") is entered into and made effective as of {dates_clean} "
                f"(the \"Effective Date\"), by and between the following parties:\n\n"
                f"**Parties Involved:**\n"
                f"{parties_clean}\n\n"
                f"(Collectively referred to as the \"Parties\" or individually as a \"Party\").\n\n"
                f"### RECITALS\n"
                f"WHEREAS, the Parties wish to explore potential business relationships, collaborative opportunities, "
                f"or transactional dealings; and\n"
                f"WHEREAS, in connection with said relationship, Disclosing Party may share confidential and proprietary "
                f"information with Receiving Party subject to the terms and protections set forth herein.\n\n"
                f"NOW, THEREFORE, in consideration of the mutual covenants contained herein and other good and valuable "
                f"consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:\n\n"
                f"### 1. Definition of Confidential Information\n"
                f"For purposes of this Agreement, \"Confidential Information\" shall include all information or material that has "
                f"or could have commercial value or other utility in the business in which Disclosing Party is engaged, whether "
                f"disclosed orally, visually, in writing, or electronically, including technical data, trade secrets, software, "
                f"financial data, business plans, and customer lists.\n\n"
                f"### 2. Obligations & Key Terms\n"
                f"{terms_formatted}\n\n"
                f"### 3. Exclusions from Confidential Information\n"
                f"Confidential Information does not include information that: (a) is or becomes publicly known through no breach of this "
                f"Agreement; (b) was already known to the Receiving Party prior to disclosure; (c) is independently developed without reference "
                f"to Disclosing Party's Confidential Information; or (d) is required to be disclosed by applicable law or court order.\n\n"
                f"### 4. Term and Termination\n"
                f"This Agreement shall commence on {dates_clean} and shall remain in effect until terminated in writing by either Party, "
                f"or for a period of two (2) years from the Effective Date, whichever occurs first. The duty to protect trade secrets shall "
                f"survive indefinitely.\n\n"
                f"### 5. Governing Law and Severability\n"
                f"This Agreement shall be construed and governed in accordance with the laws of [State/Jurisdiction], without regard to "
                f"its conflict of laws principles. If any provision is deemed unenforceable, the remaining provisions shall remain in full force.\n\n"
                f"### 6. Entire Agreement\n"
                f"This Agreement constitutes the entire understanding between the Parties concerning the subject matter hereof and supersedes "
                f"all prior agreements, negotiations, and discussions.\n\n"
                f"IN WITNESS WHEREOF, the Parties have executed this Non-Disclosure Agreement as of the Effective Date written above.\n\n"
                f"______________________________________            ______________________________________\n"
                f"Authorized Signature                              Authorized Signature\n\n"
                f"Name: [Authorized Representative]                 Name: [Authorized Representative]\n"
                f"Title: [Title]                                    Title: [Title]\n"
                f"Date: {dates_clean}                               Date: {dates_clean}\n"
            )
        elif "employment" in lower_type or "offer" in lower_type:
            doc = (
                f"## {doc_type_clean}\n\n"
                f"This {doc_type_clean} (the \"Agreement\") is entered into on {dates_clean} (the \"Effective Date\"), "
                f"by and between:\n\n"
                f"**Parties Involved:**\n"
                f"{parties_clean}\n\n"
                f"### RECITALS\n"
                f"WHEREAS, Employer desires to retain the professional services of Employee, and Employee desires to render "
                f"services to Employer upon the terms and conditions set forth herein.\n\n"
                f"NOW, THEREFORE, the Parties agree as follows:\n\n"
                f"### 1. Position and Duties\n"
                f"Employee shall serve in the designated capacity and faithfully perform all duties and responsibilities assigned "
                f"by Employer consistent with this role. Employee agrees to devote full business time and best efforts to the business "
                f"of Employer.\n\n"
                f"### 2. Agreed Terms and Compensation\n"
                f"{terms_formatted}\n\n"
                f"### 3. Confidentiality and Intellectual Property\n"
                f"Employee agrees to keep strictly confidential all proprietary, business, and technical information of Employer. "
                f"All works, discoveries, and intellectual property developed by Employee within the scope of employment shall belong "
                f"solely and exclusively to Employer.\n\n"
                f"### 4. Termination\n"
                f"Either party may terminate the employment relationship in accordance with applicable notice requirements or immediately "
                f"for cause as permitted under applicable law.\n\n"
                f"### 5. Governing Law\n"
                f"This Agreement shall be interpreted and enforced in accordance with the laws of [State/Jurisdiction].\n\n"
                f"IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.\n\n"
                f"______________________________________            ______________________________________\n"
                f"Employer Signature                                Employee Signature\n\n"
                f"Print Name: [Employer Representative]             Print Name: [Employee Name]\n"
                f"Date: {dates_clean}                               Date: {dates_clean}\n"
            )
        elif "lease" in lower_type:
            doc = (
                f"## Residential / Commercial Lease Agreement\n\n"
                f"This Lease Agreement (the \"Lease\") is made and entered into on {dates_clean} (the \"Effective Date\"), "
                f"by and between the following parties:\n\n"
                f"**Parties Involved:**\n"
                f"{parties_clean}\n\n"
                f"### 1. Leased Premises\n"
                f"Landlord hereby leases to Tenant, and Tenant hereby leases from Landlord, the real property located at "
                f"[Insert Property Address] (the \"Premises\").\n\n"
                f"### 2. Lease Terms and Covenants\n"
                f"{terms_formatted}\n\n"
                f"### 3. Maintenance and Alterations\n"
                f"Tenant shall keep the Premises in clean, sanitary, and good condition. Tenant shall not make structural changes "
                f"or alterations without prior written consent from Landlord.\n\n"
                f"### 4. Default and Surrender\n"
                f"Upon expiration or earlier termination of this Lease, Tenant shall surrender the Premises in as good condition "
                f"as when received, reasonable wear and tear excepted.\n\n"
                f"### 5. Governing Law\n"
                f"This Lease shall be governed and construed pursuant to the real property laws of [State/Jurisdiction].\n\n"
                f"IN WITNESS WHEREOF, the Parties have signed and delivered this Lease Agreement as of {dates_clean}.\n\n"
                f"______________________________________            ______________________________________\n"
                f"Landlord Signature                                Tenant Signature\n\n"
                f"Print Name: [Landlord Name]                       Print Name: [Tenant Name]\n"
                f"Date: {dates_clean}                               Date: {dates_clean}\n"
            )
        else:
            # Generic Contract / Agreement / Freelance Contract / Service Agreement
            doc = (
                f"## {doc_type_clean}\n\n"
                f"This {doc_type_clean} (the \"Agreement\") is made and executed as of {dates_clean} (the \"Effective Date\"), "
                f"by and between:\n\n"
                f"**Parties Involved:**\n"
                f"{parties_clean}\n\n"
                f"### RECITALS\n"
                f"WHEREAS, the Parties desire to formalize an agreement outlining their respective rights, responsibilities, "
                f"and obligations as set forth herein;\n\n"
                f"NOW, THEREFORE, for good and valuable consideration, the receipt and adequacy of which are hereby acknowledged, "
                f"the Parties agree as follows:\n\n"
                f"### 1. Scope of Agreement and Purpose\n"
                f"The Parties hereby agree to perform the mutual responsibilities, deliverables, and commitments established under "
                f"this Agreement in a diligent and professional manner.\n\n"
                f"### 2. Terms and Conditions\n"
                f"{terms_formatted}\n\n"
                f"### 3. Representations and Warranties\n"
                f"Each Party represents and warrants that it has the full legal power and authority to enter into and perform "
                f"its obligations under this Agreement.\n\n"
                f"### 4. Term and Termination\n"
                f"This Agreement shall commence on {dates_clean} and shall remain in full force and effect until completed or "
                f"terminated by mutual written consent or as specified in the agreed terms.\n\n"
                f"### 5. Governing Law and Severability\n"
                f"This Agreement shall be construed and governed in accordance with the laws of [State/Jurisdiction]. If any provision "
                f"is held invalid or unenforceable, such provision shall be severed without invalidating remaining provisions.\n\n"
                f"IN WITNESS WHEREOF, the Parties have executed this {doc_type_clean} as of the Effective Date.\n\n"
                f"______________________________________            ______________________________________\n"
                f"Party A Signature                                 Party B Signature\n\n"
                f"Print Name: [Authorized Name]                     Print Name: [Authorized Name]\n"
                f"Title: [Title]                                    Title: [Title]\n"
                f"Date: {dates_clean}                               Date: {dates_clean}\n"
            )

        return sanitize_text(doc)
