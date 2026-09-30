"""
LegalEase Gemini Document Generator
Core AI module utilizing Google Gemini API to generate structured, professional legal documents
with comprehensive legal drafting templates and failover support.
"""

import logging
import os
import re
from typing import Optional
from dotenv import load_dotenv
from ..utils.text_utils import sanitize_text, parse_terms

# Load environment variables
load_dotenv(override=True)

logger = logging.getLogger("legalease.ai_core")


class GeminiDocumentGenerator:
    """
    AI-powered legal document generator using Google Gemini SDK with intelligent fallback.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initializes the generator with Gemini API credentials and model configuration.
        """
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEy") or "").strip()
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
        self._client = None
        self._sdk_type = None

        if not self.api_key or self.api_key == "your_api_key_here":
            logger.warning("GEMINI_API_KEY is not configured or is a placeholder.")

    def _get_client(self):
        """
        Initializes and returns the appropriate Gemini client.
        Supports both modern `google-genai` and `google.generativeai`.
        """
        if not self.api_key or self.api_key == "your_api_key_here":
            return None, "fallback"

        if self._client is not None:
            return self._client, self._sdk_type

        # Try modern google-genai first
        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            self._sdk_type = "google-genai"
            logger.info("Initialized google-genai client.")
            return self._client, self._sdk_type
        except ImportError:
            pass

        # Fallback to google.generativeai
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=self.api_key)
            self._client = legacy_genai.GenerativeModel(self.model_name)
            self._sdk_type = "google-generativeai"
            logger.info("Initialized legacy google.generativeai client.")
            return self._client, self._sdk_type
        except ImportError:
            return None, "fallback"

    def build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        """
        Constructs the structured, compliance-oriented legal prompt for Gemini.
        """
        parsed_terms_list = parse_terms(terms)
        formatted_terms = "\n".join([f"- {t}" for t in parsed_terms_list]) if parsed_terms_list else terms

        prompt = f"""You are an elite corporate legal counsel and legal document drafter.
Draft a complete, comprehensive, and professional legal document based on the following specifications.

DOCUMENT SPECIFICATIONS:
- DOCUMENT TYPE: {document_type}
- EFFECTIVE DATE: {effective_date}
- PARTIES INVOLVED: {parties}
- SPECIFIC TERMS & CONDITIONS SUPPLIED BY USER:
{formatted_terms}

DRAFTING INSTRUCTIONS & CONSTRAINTS:
1. DOCUMENT TITLE: Start with the formal title in uppercase centered format (e.g. # {document_type.upper()}).
2. PREAMBLE & RECITALS:
   - Identify all parties clearly with their legal capacities, addresses (placeholders if not provided), and defined terms (e.g. "Disclosing Party", "Receiving Party", "Company", "Contractor", "Employer", "Employee", "Lessor", "Lessee").
   - Explicitly state the Effective Date: {effective_date}.
   - Include standard "WHEREAS" recital clauses detailing the context and mutual intent of the parties.
3. OPERATIVE PROVISIONS / NUMBERED SECTIONS:
   - Organize into logical, numbered articles/sections (e.g., SECTION 1. SCOPE OF SERVICES / OBLIGATIONS, SECTION 2. COMPENSATION & PAYMENT TERMS, SECTION 3. TERM & TERMINATION, SECTION 4. CONFIDENTIALITY, etc.).
   - Directly incorporate ALL user-supplied terms & conditions into the relevant operative sections.
   - Include standard legal protections appropriate for a {document_type} (e.g. Representations & Warranties, Indemnification, Intellectual Property, Limitation of Liability, Severability, Entire Agreement, Force Majeure, Amendments, Notices, Counterparts).
4. JURISDICTION & GOVERNING LAW:
   - If the user specified a jurisdiction in the terms, enforce it. Otherwise, use a standard neutral governing law clause without inventing an arbitrary local jurisdiction.
5. EXECUTION & SIGNATURE BLOCK:
   - Provide a formal "IN WITNESS WHEREOF" closing clause followed by structured signature blocks for all parties, including lines for:
     * Authorized Signature (e.g., By: ___________________)
     * Printed Name (Name: ___________________)
     * Title / Designation (Title: ___________________)
     * Date (Date: ___________________)
6. DISCLAIMER:
   - End the document with the following mandatory disclaimer section:
     ## DISCLAIMER & LEGAL NOTICE
     This document is an AI-assisted draft created for template and informational purposes only. It does not constitute formal legal advice and does not create an attorney-client relationship. Laws and legal requirements vary by jurisdiction. All parties should have this document reviewed, customized, and approved by a qualified licensed attorney in their respective jurisdiction prior to execution.
7. ABSOLUTE PROHIBITIONS:
   - Do NOT invent fake case citations, fabricated docket numbers, or fictional statutory codes.
   - Do NOT include conversational commentary, preamble notes (e.g., "Certainly, here is the agreement"), or markdown conversational wrapping.
   - Output ONLY the finished legal document text.
"""
        return prompt

    def generate(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        """
        Executes document generation via the Gemini API with failover to structured legal drafting engine.
        """
        if not document_type or not document_type.strip():
            raise ValueError("Document type cannot be empty.")
        if not parties or not parties.strip():
            raise ValueError("Parties cannot be empty.")
        if not terms or not terms.strip():
            raise ValueError("Terms and conditions cannot be empty.")
        if not effective_date or not effective_date.strip():
            raise ValueError("Effective date cannot be empty.")

        client, sdk_type = self._get_client()

        # If API client is active, attempt live generation across supported models
        if client and sdk_type != "fallback":
            prompt = self.build_prompt(
                document_type=document_type.strip(),
                parties=parties.strip(),
                terms=terms.strip(),
                effective_date=effective_date.strip(),
            )

            models_to_try = [self.model_name, "gemini-3.8-flash", "gemini-3.7-flash", "gemini-flash-latest", "gemini-2.5-flash"]
            # Deduplicate preserving order
            unique_models = []
            for m in models_to_try:
                if m and m not in unique_models:
                    unique_models.append(m)

            for model_cand in unique_models:
                try:
                    logger.info(f"Attempting Gemini generation with model: {model_cand}")
                    if sdk_type == "google-genai":
                        response = client.models.generate_content(
                            model=model_cand,
                            contents=prompt,
                        )
                        raw_text = response.text or ""
                        if raw_text.strip():
                            return sanitize_text(raw_text)
                    elif sdk_type == "google-generativeai":
                        response = client.generate_content(prompt)
                        raw_text = response.text or ""
                        if raw_text.strip():
                            return sanitize_text(raw_text)
                except Exception as e:
                    logger.warning(f"Model {model_cand} error: {e}")

        # If live API returns permission errors or no key, generate complete legal draft
        logger.info(f"Using LegalEase AI Core generator for: {document_type}")
        return self._generate_structured_legal_draft(
            document_type=document_type.strip(),
            parties=parties.strip(),
            terms=terms.strip(),
            effective_date=effective_date.strip(),
        )

    def _generate_structured_legal_draft(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        """
        High-precision legal draft engine incorporating all user specifications,
        contractual recitals, operative clauses, covenants, and signature blocks.
        """
        parsed_terms = parse_terms(terms)
        doc_type_clean = document_type.strip()
        doc_type_upper = doc_type_clean.upper()

        # Extract party names
        party_parts = [p.strip() for p in re.split(r",|and|\&", parties) if p.strip()]
        party1 = party_parts[0] if len(party_parts) > 0 else "First Party"
        party2 = party_parts[1] if len(party_parts) > 1 else "Second Party"

        # Terms formatted into operative clauses
        terms_clauses = ""
        for i, term in enumerate(parsed_terms, start=1):
            terms_clauses += f"* **Clause {i} ({term.split(':')[0] if ':' in term else 'Specific Condition'}):** {term}\n"

        if not terms_clauses:
            terms_clauses = f"* {terms}\n"

        draft = f"""# {doc_type_upper}

This {doc_type_clean} (the "Agreement") is entered into and made effective as of **{effective_date}** (the "Effective Date"), by and between:

* **Party 1:** {party1}
* **Party 2:** {party2}

(Each individually referred to as a "Party" and collectively as the "Parties").

---

## RECITALS

WHEREAS, the Parties desire to enter into this {doc_type_clean} to define their respective rights, duties, and covenants in accordance with mutual commercial understanding; and

WHEREAS, the Parties agree to be legally bound by the terms, covenants, representations, and warranties set forth herein;

NOW, THEREFORE, in consideration of the mutual covenants and valuable considerations herein contained, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:

---

## SECTION 1. SCOPE AND PURPOSE
1.1 The primary purpose of this {doc_type_clean} is to establish the formal arrangement between {party1} and {party2} pursuant to the mutual objectives of both Parties.
1.2 Both Parties agree to act in good faith and carry out their respective responsibilities in a timely and professional manner.

## SECTION 2. KEY TERMS AND STIPULATED CONDITIONS
The following covenants and operating conditions have been expressly agreed upon by the Parties:

{terms_clauses}

## SECTION 3. TERM AND TERMINATION
3.1 **Term:** This Agreement shall commence on the Effective Date ({effective_date}) and shall remain in full force and effect until terminated in accordance with the provisions herein or upon completion of all obligations.
3.2 **Termination for Cause:** Either Party may terminate this Agreement immediately upon written notice if the other Party materially breaches any provision of this Agreement and fails to cure such breach within fifteen (15) days of receipt of written notice.
3.3 **Effect of Termination:** Upon termination, all accrued payment obligations and surviving confidentiality terms shall remain binding upon the Parties.

## SECTION 4. CONFIDENTIALITY AND NON-DISCLOSURE
4.1 The Parties agree that all non-public, proprietary, or business information disclosed by one Party to the other in connection with this Agreement shall be treated as strictly confidential.
4.2 Neither Party shall disclose or disseminate Confidential Information to any third party without prior written consent from the disclosing Party, except as required by applicable law or court order.

## SECTION 5. REPRESENTATIONS AND WARRANTIES
5.1 Each Party represents and warrants that it has full legal power, authority, and capacity to enter into this Agreement and perform its obligations hereunder.
5.2 The execution, delivery, and performance of this Agreement does not violate any other contract, court order, or legal restriction binding on either Party.

## SECTION 6. INDEMNIFICATION AND LIMITATION OF LIABILITY
6.1 Each Party shall defend, indemnify, and hold harmless the other Party, its affiliates, officers, and employees from and against any third-party claims, liabilities, damages, and reasonable legal expenses arising out of gross negligence or willful misconduct.
6.2 To the maximum extent permitted by law, neither Party shall be liable for any indirect, incidental, consequential, or punitive damages arising out of this Agreement.

## SECTION 7. GENERAL PROVISIONS
7.1 **Entire Agreement:** This Agreement constitutes the sole and entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, understandings, and agreements.
7.2 **Amendments:** No modification or amendment to this Agreement shall be binding unless executed in writing and signed by authorized representatives of both Parties.
7.3 **Severability:** If any provision of this Agreement is held to be invalid or unenforceable, such holding shall not affect the validity or enforceability of the remaining provisions.
7.4 **Governing Law & Jurisdiction:** This Agreement shall be governed by and construed in accordance with the laws applicable to the governing jurisdiction of the Parties, without regard to conflicts of law principles.

---

## IN WITNESS WHEREOF
The Parties hereto have caused this {doc_type_clean} to be duly executed by their authorized representatives as of the Effective Date written above.

**FOR: {party1}**

By: ____________________________________
Name: __________________________________
Title: _________________________________
Date: __________________________________


**FOR: {party2}**

By: ____________________________________
Name: __________________________________
Title: _________________________________
Date: __________________________________

---

## DISCLAIMER & LEGAL NOTICE
This document is an AI-assisted draft created for template and informational purposes only. It does not constitute formal legal advice and does not create an attorney-client relationship. Laws and legal requirements vary significantly across jurisdictions. All parties should have this document reviewed, customized, and approved by a qualified licensed attorney in their respective jurisdiction prior to execution.
"""
        return sanitize_text(draft)
