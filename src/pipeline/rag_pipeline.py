from retrieval.retriever import retrieve_context
from llm.llm import generate_answer
from prompts.rag_prompt import build_rag_prompt


def build_standalone_question(
    question: str,
    chat_history: list[dict]
) -> str:
    """
    Rewrite a follow-up question into a standalone question.
    """

    if not chat_history:
        return question

    history_text = "\n".join(
        f"{message['role'].capitalize()}: "
        f"{message['content']}"
        for message in chat_history[-6:]
    )

    prompt = f"""
Rewrite the user's latest question into a standalone question.

Rules:

1. Preserve the original meaning.
2. Resolve references such as "it", "they", "that", or "this".
3. Do not answer the question.
4. Do not add information not present in the conversation.
5. If already standalone, return it unchanged.
6. Return ONLY the rewritten question.

Conversation:
{history_text}

Latest question:
{question}

Standalone question:
"""

    return generate_answer(
        prompt,
        max_new_tokens=80
    ).strip()


def ask_question(
    question: str,
    chat_history: list[dict] | None = None
) -> tuple[str, list[dict]]:
    """
    Complete conversational RAG pipeline.
    """

    if chat_history is None:
        chat_history = []

    standalone_question = build_standalone_question(
        question,
        chat_history
    )

    context, sources = retrieve_context(
        standalone_question
    )

    prompt = build_rag_prompt(
        context=context,
        question=question,
        chat_history=chat_history
    )

    answer = generate_answer(
        prompt
    )

    return answer, sources