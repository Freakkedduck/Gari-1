import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from typing import List

# Optional: Set this to your Tesseract executable path if needed (especially on Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(image: Image.Image) -> str:
    """Performs OCR on a PIL image."""
    return pytesseract.image_to_string(image)

def pdf_to_images(pdf_path: str, dpi: int = 300) -> List[Image.Image]:
    """
    Converts a PDF to a list of PIL images (one per page).
    Requires poppler to be installed.
    """
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        return images
    except Exception as e:
        print(f"[ERROR] Failed to convert PDF to images: {e}")
        return []

def ocr_pdf_full(pdf_path: str) -> List[str]:
    """
    Performs OCR on every page of a PDF by rendering it to image.
    Returns a list of page-level OCR text strings.
    """
    images = pdf_to_images(pdf_path)
    ocr_pages = []

    for idx, img in enumerate(images, start=1):
        try:
            text = ocr_image(img)
            ocr_pages.append(text)
        except Exception as e:
            print(f"[OCR ERROR] Page {idx} failed: {e}")
            ocr_pages.append("")

    return ocr_pages
