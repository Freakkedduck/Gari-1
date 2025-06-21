import streamlit as st
import requests

st.title("DocBot: Document Q&A")

st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://localhost:8000/api/upload/", files=files)
    if response.ok:
        st.success(f"Uploaded: {uploaded_file.name}")
        doc_id = response.json().get("doc_id")
        st.session_state["doc_id"] = doc_id
    else:
        st.error("Upload failed.")

st.header("Ask a Question")
question = st.text_input("Enter your question:")

doc_id = st.session_state.get("doc_id")
if st.button("Submit Query") and question and doc_id:
    payload = {"question": question, "doc_id": doc_id}
    resp = requests.post("http://localhost:8000/api/query/", json=payload)
    if resp.ok:
        data = resp.json()
        st.subheader("Answer:")
        st.write(data.get("answer"))
        st.subheader("Citations:")
        for c in data.get("citations", []):
            st.write(f"DocID: {c['doc_id']}, Page: {c['page']}, Paragraph: {c['paragraph']}")
    else:
        st.error("Query failed.")
