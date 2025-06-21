from fastapi import APIRouter, UploadFile, File, Query
from backend.services.extract_text import extract_text_from_file
from backend.services.extract_rich import extract_rich_from_pdf
from backend.models.document import DocumentMeta
import os, uuid

router = APIRouter()
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/", response_model=DocumentMeta)
async def upload_file(
    file: UploadFile = File(...),
    mode: str = Query(default="basic", enum=["basic", "rich"])
):
    doc_id = str(uuid.uuid4())
    filepath = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Determine file extension
    ext = os.path.splitext(filepath)[-1].lower()

    # Extraction logic
    if mode == "basic":
        extracted = extract_text_from_file(filepath, doc_id)
    elif mode == "rich":
        if ext == ".pdf":
            extracted = extract_rich_from_pdf(filepath, doc_id)
        else:
            return {
                "doc_id": doc_id,
                "filename": file.filename,
                "pages": 0,
                "sample": ["Rich mode supported only for PDFs"]
            }

    return DocumentMeta(
        doc_id=doc_id,
        filename=file.filename,
        pages=len(extracted),
        sample=(extracted[0]["paragraphs"][:2] if extracted and "paragraphs" in extracted[0] else [])
    )
