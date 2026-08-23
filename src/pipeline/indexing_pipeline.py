import hashlib
from pathlib import Path

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_splitter import split_documents

from src.retrieval.vector_store import (
    add_documents_to_vector_store,
    load_vector_store
)


DATA_DIR = Path("data/uploaded_pdfs")


def calculate_file_hash(
    file_path: str
) -> str:
    """
    Calculate a SHA-256 hash for a file.
    """

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):

            sha256.update(
                chunk
            )

    return sha256.hexdigest()


def is_document_indexed(
    vector_store,
    document_id: str
) -> bool:
    """
    Check whether a document version
    has already been indexed.
    """

    results = vector_store.get(
        where={
            "document_id": document_id
        },
        limit=1
    )

    return len(
        results["ids"]
    ) > 0


def index_pdf(
    pdf_path: str
) -> dict:
    """
    Index a PDF if its content has not
    already been indexed.
    """

    file_path = Path(pdf_path)

    document_id = calculate_file_hash(
        str(file_path)
    )

    vector_store = load_vector_store()

    if is_document_indexed(
        vector_store,
        document_id
    ):

        return {
            "status": "already_indexed",
            "file_name": file_path.name,
            "document_id": document_id,
            "chunks": 0
        }

    documents = load_pdf(
        str(file_path)
    )

    chunks = split_documents(
        documents
    )

    for chunk in chunks:

        chunk.metadata["source"] = (
            file_path.name
        )

        chunk.metadata["document_id"] = (
            document_id
        )

    add_documents_to_vector_store(
        chunks
    )

    return {
        "status": "indexed",
        "file_name": file_path.name,
        "document_id": document_id,
        "chunks": len(chunks)
    }


def index_all_pdfs():
    """
    Index all PDFs in the upload directory.
    """

    pdf_files = list(
        DATA_DIR.glob("*.pdf")
    )

    if not pdf_files:

        return []

    results = []

    for pdf_file in pdf_files:

        result = index_pdf(
            str(pdf_file)
        )

        results.append(
            result
        )

    return results