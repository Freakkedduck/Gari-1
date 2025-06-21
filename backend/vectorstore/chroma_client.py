# ChromaDB client and collection initialization
import chromadb
from chromadb.config import Settings

class ChromaClient:
    def __init__(self, collection_name: str = "doc_chunks"):
        self.client = chromadb.Client(Settings())
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_documents(self, embeddings, metadatas, ids):
        self.collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)

    def query(self, query_embeddings, n_results=5):
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results)

