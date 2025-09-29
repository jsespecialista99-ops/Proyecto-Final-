from PyPDF2 import PdfReader
from docx import Document
import io

def extract_text_from_files(uploaded_files):
    docs_text = {}
    for file in uploaded_files:
        if file.name.lower().endswith('.pdf'):
            reader = PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif file.name.lower().endswith('.docx'):
            doc = Document(io.BytesIO(file.read()))
            text = "\n".join([p.text for p in doc.paragraphs])
        else:
            text = ""
        docs_text[file.name] = text
    return docs_text
