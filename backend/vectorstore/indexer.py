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

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.embedder.embed([query])
        results = self.chroma.query(query_embeddings=query_embedding, n_results=top_k)
        # ChromaDB returns a dict with 'ids', 'distances', 'metadatas'
        hits = []
        for i in range(len(results['ids'][0])):
            hit = {
                'id': results['ids'][0][i],
                'distance': results['distances'][0][i],
                'metadata': results['metadatas'][0][i]
            }
            hits.append(hit)
        return hits
