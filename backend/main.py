from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.upload import router as upload_router
from backend.vectorstore.chroma_client import ChromaClient
from backend.vectorstore.embedder import Embedder
from backend.vectorstore.indexer import Indexer

app = FastAPI(title="DocBot API ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")

# Initialize vectorstore components for compatibility
chroma_client = ChromaClient()
embedder = Embedder()
indexer = Indexer()
