# DocBot: Document Q&A Chatbot

Gari-1 is a modular document question-answering system. It allows you to upload documents, semantically search their content, and ask questions with answers cited from the source.

## Features
- Upload PDF, DOCX, or TXT documents
- Extract and chunk text with metadata (DocID, Page, Paragraph)
- Generate embeddings and store in ChromaDB
- Semantic search for relevant document chunks
- Local LLM (Ollama) for question answering
- Streamlit UI for easy interaction
- Answers with citation metadata

## Setup Instructions

### 1. Backend
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Start FastAPI backend:
  ```bash
  uvicorn backend.main:app --reload
  ```

### 2. Frontend (Streamlit)
- Install Streamlit:
  ```bash
  pip install streamlit
  ```
- Run the UI:
  ```bash
  streamlit run frontend/streamlit_app.py
  ```

### 3. Ollama (Local LLM)
- Install Ollama: https://ollama.com/
- Start Ollama and pull a model (e.g., llama2):
  ```bash
  ollama pull llama2
  ollama serve
  ```

### 4. ChromaDB
- ChromaDB is used as the vector store (auto-initialized by the backend).

## Usage
1. Open the Streamlit UI in your browser.
2. Upload a document.
3. Enter your question and submit.
4. View the answer and citation metadata (DocID, Page, Paragraph).

## API Example
- Upload: `POST /api/upload/`
- Query: `POST /api/query/` with JSON `{ "question": "...", "doc_id": "..." }`

## Notes
- Make sure Ollama is running before querying.
- You can change the LLM model in `backend/routes/query.py`.

---
MIT License

