from io import BytesIO
from pathlib import Path

from docx import Document
from PyPDF2 import PdfReader


def extract_text(file_content: bytes, filename: str) -> str:
    """Extract text from a PDF, DOCX, or TXT resume."""
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(BytesIO(file_content))
        pages = [page.extract_text() or "" for page in reader.pages]
        extracted_text = "\n".join(pages)

    elif extension == ".docx":
        document = Document(BytesIO(file_content))
        parts = [paragraph.text for paragraph in document.paragraphs]

        for table in document.tables:
            for row in table.rows:
                parts.append(" ".join(cell.text for cell in row.cells))

        extracted_text = "\n".join(parts)

    elif extension == ".txt":
        extracted_text = file_content.decode("utf-8", errors="ignore")

    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")

    extracted_text = extracted_text.strip()
    if not extracted_text:
        raise ValueError(
            "No readable text found. Scanned/image-only PDFs are not supported."
        )

    return extracted_text
