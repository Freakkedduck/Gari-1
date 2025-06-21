from fastapi import FastAPI
from backend.routes.upload import router as upload_router
from backend.services.text_extractor import extract_text_from_file
from backend.services.text_extractor import extract_from_docx
from backend.models.document import DocumentMeta

app = FastAPI(title="DocBot API")

app.include_router(upload_router, prefix="/api")

