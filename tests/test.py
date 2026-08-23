import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from pipeline.rag_pipeline import ask_question


def test_rag_returns_answer():
    """
    Basic smoke test to verify that the RAG pipeline
    can process a question and return an answer.
    """

    question = "What information is available in the document?"

    answer, sources = ask_question(
        question
    )

    assert isinstance(
        answer,
        str
    )

    assert answer.strip() != ""

    assert isinstance(
        sources,
        list
    )


def test_rag_returns_sources():
    """
    Verify that retrieval returns source metadata.
    """

    question = "What information is available in the document?"

    answer, sources = ask_question(
        question
    )

    assert isinstance(
        sources,
        list
    )

    if sources:

        for source in sources:

            assert "source" in source

            assert "page" in source

            assert "score" in source