# Embedding model loader and embed function
from typing import List

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[list]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()
