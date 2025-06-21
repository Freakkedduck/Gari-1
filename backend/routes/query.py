from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.vectorstore.indexer import Indexer
import requests

router = APIRouter()
indexer = Indexer()

class QueryRequest(BaseModel):
    question: str
    doc_id: str = None
    top_k: int = 5

@router.post("/query/")
async def query_docs(req: QueryRequest):
    # Search vector DB for top-k relevant chunks
    hits = indexer.search(req.question, top_k=req.top_k)
    # Prepare context for LLM
    context = "\n".join([
        f"[DocID: {h['metadata'].get('doc_id')}, Page: {h['metadata'].get('page')}, Paragraph: {h['metadata'].get('paragraph')}] {h['metadata'].get('text', '')}"
        for h in hits
    ])
    # Call Ollama LLM locally
    prompt = f"Context:\n{context}\n\nQuestion: {req.question}\nAnswer:"
    ollama_payload = {
        "model": "granite3.3:2b",  # Change to your preferred model name
        "prompt": prompt,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
    if response.ok:
        answer = response.json().get("response", "")
    else:
        answer = "[LLM Error]"
    # Prepare citations
    citations = [
        {
            "doc_id": h['metadata'].get('doc_id'),
            "page": h['metadata'].get('page'),
            "paragraph": h['metadata'].get('paragraph')
        }
        for h in hits
    ]
    return {"answer": answer, "citations": citations}
