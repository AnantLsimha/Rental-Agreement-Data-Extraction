 Agreement Metadata Extraction (LLM-Based)


1. Overview

This project implements an AI/ML system to extract structured metadata from agreement documents irrespective of their template format.

The system supports:
Scanned documents (.png)
Digital documents (.docx)
Extraction is performed using Large Language Models (LLMs) without any rule-based logic



2. Metadata Fields Extracted

The system extracts the following fields:
Agreement Value
Agreement Start Date
Agreement End Date
Renewal Notice (Days)
Party One
Party Two



3. Document Handling

3.1 DOCX Files
Text is extracted using python-docx.

3.2 PNG Files (Scanned Documents)
Gemini Vision is used to perform OCR and extract raw text.
The extracted text is passed directly to the LLM without preprocessing.



4. Setup Instructions

4.1 Create Virtual Environment
python -m venv venv
Activate:
Windows (PowerShell) -> .\venv\Scripts\Activate.ps1


4.2 Install Dependencies
pip install -r requirements.txt


4.3 Configure API Key
Create a .env file in the project root:
GEMINI_API_KEY=your_api_key_here



5. Running the System
5.1 Streamlit UI (Single File Testing)
COMMAND -> streamlit run app.py
Upload a .docx or .png
View extracted metadata as CSV


5.2 REST API
Start the API server:
uvicorn api:app --reload

API Endpoint:
POST /extract

Form-data parameter:
file: Agreement document (.docx or .png)
Example response:

{
  "file_name": "sample_agreement.docx",
  "extracted_metadata": {
    "agreement_value": 12000,
    "agreement_start_date": "01.04.2008",
    "agreement_end_date": "31.03.2009",
    "renewal_notice_days": 60,
    "party_one": "Hanumaiah",
    "party_two": "Vishal Bhardwaj"
  }
}

5.3 Evaluation Tool
Evaluation is implemented in evaluate.py using Streamlit.

COMMAND -> streamlit run evaluate.py

Evaluation results shown in the outputs and evaluation folder. Can rerun this file using the command to check the recall score for the model



6. Summary
This project demonstrates a robust, template-agnostic agreement metadata extraction system using modern LLMs, with:

->No rule-based logic
->Strong prompt engineering
->Transparent evaluation
->Fully reproducible results