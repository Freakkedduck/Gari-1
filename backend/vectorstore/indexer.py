# Indexer: chunk, embed, and store in ChromaDB
from .embedder import Embedder
from .chroma_client import ChromaClient
from typing import Dict, Any

class Indexer:
    def __init__(self):
        self.embedder = Embedder()
        self.chroma = ChromaClient()

    def chunk_text(self, doc: Dict[str, Any]) -> list:
        # Example: chunk by paragraph
        chunks = []
        doc_id = doc.get("doc_id", "unknown")
        for page in doc.get("pages", []):
            page_num = page.get("page_num", 0)
            for i, para in enumerate(page.get("paragraphs", [])):
                chunks.append({
                    "text": para,
                    "metadata": {"doc_id": doc_id, "page": page_num, "paragraph": i}
                })
        return chunks

    def index(self, doc: Dict[str, Any]):
        chunks = self.chunk_text(doc)
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        ids = [f"{m['doc_id']}_{m['page']}_{m['paragraph']}" for m in metadatas]
        embeddings = self.embedder.embed(texts)
        self.chroma.add_documents(embeddings, metadatas, ids)
