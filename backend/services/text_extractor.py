import pdfplumber
from PIL import Image
import pytesseract
import os
import json
import uuid

def extract_text_from_file(filepath: str, doc_id: str) -> dict:
    ext = os.path.splitext(filepath)[-1].lower()

    if ext == ".pdf":
        structured = extract_from_pdf(filepath)
    elif ext in [".jpg", ".jpeg", ".png"]:
        structured = extract_from_image(filepath)
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        structured = [{"page": 1, "paragraphs": split_paragraphs(raw)}]
    else:
        return {"error": "Unsupported file type."}

    # Save to data/extracted/{doc_id}.json
    save_path = f"data/extracted/{doc_id}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    return structured

def extract_from_pdf(filepath: str):
    result = []
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            cleaned = clean_text(text)
            result.append({
                "page": i,
                "paragraphs": split_paragraphs(cleaned)
            })
    return result

def extract_from_image(filepath: str):
    img = Image.open(filepath)
    text = pytesseract.image_to_string(img)
    return [{
        "page": 1,
        "paragraphs": split_paragraphs(clean_text(text))
    }]

def clean_text(text: str) -> str:
    return text.replace('\n', ' ').replace('\r', '').strip()

def split_paragraphs(text: str) -> list:
    paras = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 30]
    return paras

