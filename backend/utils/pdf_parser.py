import fitz  # PyMuPDF
import re

def clean_text(text: str) -> str:
    """
    Normalize whitespace and remove extra newlines.
    """
    text = text.replace("\u00a0", " ")  # Non-breaking spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes and clean it.
    Returns a string.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pages.append(page.get_text("text"))
    text = "\n".join(pages)
    return clean_text(text)
