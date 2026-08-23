import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_PATH)
)


from pipeline.rag_pipeline import (
    build_standalone_question
)


def test_standalone_question_without_history():
    """
    A question without conversation history
    should remain unchanged.
    """

    question = "What is my favorite color?"

    result = build_standalone_question(
        question,
        []
    )

    assert result == question


def test_follow_up_question_is_rewritten():
    """
    A follow-up question should be converted
    into a standalone question.
    """

    chat_history = [
        {
            "role": "user",
            "content": "What is my favorite color?"
        },
        {
            "role": "assistant",
            "content": "Your favorite color is red."
        }
    ]

    question = "Why do I like it?"

    result = build_standalone_question(
        question,
        chat_history
    )

    result_lower = result.lower()

    assert isinstance(
        result,
        str
    )

    assert result.strip() != ""

    assert "red" in result_lower

    assert (
        "why" in result_lower
        or "what makes" in result_lower
        or "reason" in result_lower
    )