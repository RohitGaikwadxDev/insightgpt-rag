from pathlib import Path

from langchain_chroma import Chroma

from retrieval.embeddings import EMBEDDING_MODEL


CHROMA_DB_PATH = Path("chroma_db")


def create_vector_store(documents):
    """
    Create a Chroma vector database from documents.
    """

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=EMBEDDING_MODEL,
        persist_directory=str(CHROMA_DB_PATH)
    )

    return vector_store


def load_vector_store():
    """
    Load an existing Chroma vector database.
    """

    vector_store = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=EMBEDDING_MODEL
    )

    return vector_store