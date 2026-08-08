import os
from pypdf import PdfReader

def extract_resume_text(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        return f"Error: PDF file not found at path '{pdf_path}'"

    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF '{pdf_path}': {str(e)}"
