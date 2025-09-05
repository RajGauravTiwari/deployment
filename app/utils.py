from PyPDF2 import PdfReader
import docx2txt
import tempfile

async def extract_text_from_bytes(file_stream, filename):
    ext = filename.lower().split('.')[-1]

    if ext == 'pdf':
        reader = PdfReader(file_stream)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == 'docx':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_stream.read())
            tmp.flush()
            return docx2txt.process(tmp.name)
    else:
        return "Unsupported file format."
