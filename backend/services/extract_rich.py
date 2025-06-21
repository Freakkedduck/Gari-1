import fitz  # PyMuPDF
import os
import json
from typing import List, Dict
from backend.services.ocr_utils import ocr_image, ocr_pdf_full

def extract_rich_from_pdf(filepath: str, doc_id: str) -> List[Dict]:
    extracted_dir = "data/extracted"
    os.makedirs(extracted_dir, exist_ok=True)

    doc = fitz.open(filepath)
    result = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")
        page_blocks = page.get_text("dict")["blocks"]

        paragraphs = []
        tables = []
        images_text = []

        for block in page_blocks:
            if "lines" not in block:
                continue  # likely an image block

            block_text = ""
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]])
                block_text += line_text + " "
            block_text = block_text.strip()

            if block_text.count("\n") > 3 or block_text.count("  ") > 4:
                tables.append(block_text)
            else:
                if len(block_text) > 20:
                    paragraphs.append(block_text)

        # OCR any image regions
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_name = f"doc_{doc_id}_page_{page_num+1}_img_{img_index+1}.{image_ext}"
            image_path = f"data/uploads/{image_name}"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # OCR the image
            try:
                from PIL import Image
                img_obj = Image.open(image_path)
                ocr_result = ocr_image(img_obj)
                if ocr_result.strip():
                    images_text.append(ocr_result.strip())
            except Exception as e:
                print(f"[Image OCR Error] {image_name}: {e}")

        result.append({
            "page": page_num + 1,
            "paragraphs": paragraphs,
            "tables": tables,
            "image_ocr": images_text
        })

    # Fallback OCR if everything fails
    if len(result) == 0:
        print("[Fallback] Using full OCR")
        ocr_texts = ocr_pdf_full(filepath)
        for i, ocr_page in enumerate(ocr_texts, start=1):
            result.append({
                "page": i,
                "paragraphs": [ocr_page],
                "tables": [],
                "image_ocr": []
            })

    # Save output
    save_path = os.path.join(extracted_dir, f"{doc_id}_rich.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result
