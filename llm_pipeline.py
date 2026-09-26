from docx import Document
from PIL import Image
import json
import re

from google import genai
from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"


# ---------------- DOCX → TEXT ----------------
def docx_to_text(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs).strip()


# ---------------- PNG → TEXT (VISION OCR) ----------------
def png_to_text(file):
    image = Image.open(file)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            "Extract ALL readable text EXACTLY as written. "
            "Do NOT correct spelling. Do NOT summarize.",
            image
        ]
    )

    return response.text.strip() if response and response.text else ""


# ---------------- METADATA EXTRACTION ----------------
def extract_metadata(text):
    prompt = f"""
You are a legal agreement metadata extraction system.

======================
GENERAL RULES
======================
1. Extract values ONLY if explicitly present in the document.
2. Do NOT infer, normalize, expand, or correct values.
3. Do NOT correct spelling.
4. Do NOT add honorifics (Mr, Mrs, Ms, Shri, Smt).
5. Preserve initials, dots, and spacing exactly.
6. All outputs MUST be returned as STRINGS.
7. If a value is missing, return null.

======================
FIELD RULES
======================

Agreement Value:
- Extract ONLY the MONTHLY RENT.
- Ignore deposits or advances.
- Remove currency symbols and commas.
- Example: "Rs. 12,000" → "12000"

Agreement Start Date:
- Extract lease start date.
- Convert to DD.MM.YYYY.

Agreement End Date:
- Extract lease end date.
- Convert to DD.MM.YYYY.
- If duration is given, compute end date accurately.

Renewal Notice (Days):
- Extract notice period.
- Convert months to days:
  1 month → 30 days
  2 months → 60 days

Party One:
- Extract LESSOR / OWNER name.
- Remove honorifics.
- Preserve initials, dots, spacing exactly.

Party Two:
- Extract LESSEE / TENANT name.
- Remove honorifics.
- Preserve initials, dots, spacing exactly.

======================
OUTPUT FORMAT (STRICT)
======================
Return ONLY valid JSON:

{{
  "agreement_value": null,
  "agreement_start_date": null,
  "agreement_end_date": null,
  "renewal_notice_days": null,
  "party_one": null,
  "party_two": null
}}

======================
DOCUMENT TEXT
======================
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response or not response.text:
        return empty_result()

    content = response.text.strip()

    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return empty_result()


def empty_result():
    return {
        "agreement_value": None,
        "agreement_start_date": None,
        "agreement_end_date": None,
        "renewal_notice_days": None,
        "party_one": None,
        "party_two": None
    }


# ---------------- UNIFIED PIPELINE ----------------
def process_file(file):
    filename = file.name.lower()

    if filename.endswith(".docx"):
        text = docx_to_text(file)
    elif filename.endswith(".png"):
        text = png_to_text(file)
    else:
        raise ValueError("Unsupported file format")

    if not text.strip():
        return empty_result()

    return extract_metadata(text)
