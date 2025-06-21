import os
import pdfplumber
import docx
import json
from typing import List, Dict

def clean_text(text: str) -> str:
    return text.replace('\n', ' ').replace('\r', '').strip()

def split_paragraphs(text: str) -> List[str]:
    # Naive paragraph splitter — can be improved later
    return [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]

def extract_from_pdf(filepath: str) -> List[Dict]:
    output = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            cleaned = clean_text(text)
            output.append({
                "page": i,
                "paragraphs": split_paragraphs(cleaned)
            })
    return output

def extract_from_docx(filepath: str) -> List[Dict]:
    doc = docx.Document(filepath)
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    cleaned = clean_text(full_text)
    return [{
        "page": 1,
        "paragraphs": split_paragraphs(cleaned)
    }]

def extract_from_txt(filepath: str) -> List[Dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    cleaned = clean_text(raw)
    return [{
        "page": 1,
        "paragraphs": split_paragraphs(cleaned)
    }]

def extract_text_from_file(filepath: str, doc_id: str) -> List[Dict]:
    ext = os.path.splitext(filepath)[-1].lower()
    extracted_dir = "data/extracted"
    os.makedirs(extracted_dir, exist_ok=True)

    if ext == ".pdf":
        structured = extract_from_pdf(filepath)
    elif ext == ".docx":
        structured = extract_from_docx(filepath)
    elif ext == ".txt":
        structured = extract_from_txt(filepath)
    else:
        raise ValueError("Unsupported file type for basic extraction.")

    # Save structured output
    save_path = os.path.join(extracted_dir, f"{doc_id}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    return structured
