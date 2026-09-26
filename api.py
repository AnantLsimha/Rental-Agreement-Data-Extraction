from fastapi import FastAPI, UploadFile, File
import tempfile
from llm_pipeline import process_file

app = FastAPI(title="Agreement Metadata Extraction API")

@app.post("/extract")
async def extract_metadata(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        f.name = file.filename
        metadata = process_file(f)

    return {
        "file_name": file.filename,
        "extracted_metadata": metadata
    }
