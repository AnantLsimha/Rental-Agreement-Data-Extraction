# 📄 Rental Agreement Data Extraction System (LLM-Based)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google GenAI](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-4285F4.svg)](https://ai.google.dev/)

An AI-driven document information extraction system designed to extract structured metadata from legal agreement documents regardless of template layout or file format.

The system supports both digital documents (`.docx`) and scanned images (`.png`), performing zero-shot extraction using **Google Gemini Vision LLMs** without any rule-based Regex heuristics.

---

## 🌟 Key Features

- **Template-Agnostic Extraction**: Parses un-structured legal agreements without custom rules or template configuration.
- **Multimodal Document Processing**:
  - **DOCX**: Direct text parsing via `python-docx`.
  - **PNG**: OCR + spatial text understanding via Gemini 2.5 Flash Vision.
- **REST API Endpoint**: FastAPI server exposing `POST /extract` for enterprise integration.
- **Streamlit Web Dashboard**: User-friendly single-document extraction UI with instant CSV exports.
- **Automated Evaluation Benchmark**: Quantitative evaluation module testing per-field exact-match recall against ground-truth datasets.

---

## 🎯 Target Metadata Fields

| Field Name | Description & Extraction Rules | Benchmark Recall |
| :--- | :--- | :---: |
| **Agreement Value** | Monthly rent only (excludes security deposits & advances) | **1.00 (100%)** |
| **Agreement Start Date** | Lease start date standardized to `DD.MM.YYYY` | **1.00 (100%)** |
| **Agreement End Date** | Lease end date standardized to `DD.MM.YYYY` | **0.50 (50%)** |
| **Renewal Notice (Days)** | Notice period normalized to days (e.g. 2 months → 60 days) | **0.75 (75%)** |
| **Party One** | Lessor / Owner name (strips honorifics, preserves initials) | **0.75 (75%)** |
| **Party Two** | Lessee / Tenant name (strips honorifics, preserves initials) | **0.50 (50%)** |

> **Overall Average Recall**: **0.75 (75%)** under strict exact-match string evaluation.

---

## 🏗 System Architecture

```
Rental Agreement Data Extraction System/
├── api.py                   # FastAPI application (REST endpoint: POST /extract)
├── app.py                   # Streamlit Web GUI for single-file processing
├── evaluate.py              # Quantitative evaluation dashboard & benchmark
├── llm_pipeline.py          # Unified pipeline (DOCX reader, Gemini Vision OCR & prompt logic)
├── config.py                # Environment configuration loader
├── requirements.txt         # Project dependencies
├── .env.example             # API Key configuration template
├── data/
│   ├── train/               # 10 training sample agreement files (.docx, .png)
│   ├── test/                # 4 testing sample agreement files (.docx, .png)
│   ├── train.csv            # Ground truth metadata for training set
│   └── test.csv             # Ground truth metadata for testing set
└── output and accuracy/
    ├── outputs/             # System execution visual artifacts
    └── recall/              # Per-field evaluation benchmark screenshots
```

---

## ⚙️ Setup & Installation

### 1. Clone Repository & Create Virtual Environment

```bash
git clone https://github.com/AnantLsimha/Rental-Agreement-Data-Extraction.git
cd Rental-Agreement-Data-Extraction

python -m venv venv
# Activate on Windows:
.\venv\Scripts\Activate.ps1
# Activate on Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the root directory based on `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 Running the System

### Option A: Streamlit Interactive UI (Single Document Testing)

Launch the web application to upload single `.docx` or `.png` agreements and download structured CSV results:

```bash
streamlit run app.py
```

### Option B: FastAPI REST Endpoint

Start the Uvicorn server:

```bash
uvicorn api:app --reload
```

**API Endpoint**: `POST http://localhost:8000/extract`  
**Form Data**: `file` (Document file: `.docx` or `.png`)

**Sample JSON Response**:
```json
{
  "file_name": "sample_agreement.docx",
  "extracted_metadata": {
    "agreement_value": "12000",
    "agreement_start_date": "01.04.2008",
    "agreement_end_date": "31.03.2009",
    "renewal_notice_days": "60",
    "party_one": "Hanumaiah",
    "party_two": "Vishal Bhardwaj"
  }
}
```

### Option C: Run Quantitative Evaluation Suite

Rerun exact-match evaluation benchmarks against the test dataset:

```bash
streamlit run evaluate.py
```

---

## 📊 Evaluation Metrics & Visual Artifacts

### Evaluation Benchmark Output
![Evaluation Results](<output%20and%20accuracy/recall/Screenshot%20%28100%29.png>)

### Extracted Metadata Visual Preview
![Metadata Extraction Preview](<output%20and%20accuracy/outputs/Screenshot%20%28105%29.png>)

---

## 📜 Summary & Highlights

- **Zero Rule-Based Heuristics**: Entirely prompt-engineered for flexible adaptability to new contract templates.
- **Multimodal Flexibility**: Handles digital text documents and scanned image contracts seamlessly.
- **Reproducible Evaluation**: Transparent evaluation script measuring exact-match recall across test contracts.