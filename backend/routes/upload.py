from fastapi import APIRouter, UploadFile, File
from backend.services.text_extractor import extract_text_from_file
from backend.models.document import DocumentMeta
import os, uuid

router = APIRouter()
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(path, "wb") as f:
        f.write(await file.read())

    extracted = extract_text_from_file(path, doc_id)

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "pages": len(extracted) if isinstance(extracted, list) else 0,
        "sample": extracted[0]["paragraphs"][:2] if isinstance(extracted, list) and extracted else [],
    }

