from pydantic import BaseModel
from typing import List

class DocumentMeta(BaseModel):
    doc_id: str
    filename: str
    sample: List[str]
    pages: int

