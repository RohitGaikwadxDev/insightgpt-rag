from ingestion.pdf_loader import load_pdf
from ingestion.text_cleaner import clean_documents
from ingestion.text_splitter import split_documents

from retrieval.vector_store import create_vector_store


def index_pdf(pdf_path: str) -> int:
    """
    Complete indexing pipeline.

    PDF
      ↓
    Load
      ↓
    Clean
      ↓
    Split
      ↓
    Store in Chroma

    Returns:
        Number of chunks indexed.
    """

    documents = load_pdf(pdf_path)

    cleaned_documents = clean_documents(documents)

    chunks = split_documents(cleaned_documents)

    create_vector_store(chunks)

    return len(chunks)