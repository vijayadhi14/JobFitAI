import fitz  # PyMuPDF
import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text("text"))
    full_text = ''.join(pages_text)
    return clean_text(full_text)
