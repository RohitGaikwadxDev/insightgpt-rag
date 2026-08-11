from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> list[Document]:
    """
    Load a PDF file and return its pages as LangChain Document objects.

    Args:
        pdf_path (str):
            Path to the PDF file.

    Returns:
        list[Document]:
            List of LangChain Document objects.
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_file}"
        )

    loader = PyPDFLoader(str(pdf_file))

    documents = loader.load()

    return documents