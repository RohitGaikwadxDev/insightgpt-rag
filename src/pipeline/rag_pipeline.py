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


def check_answer_grounding(
    question: str,
    answer: str,
    context: str
) -> bool:
    """
    Check whether the generated answer is supported
    by the retrieved document context.
    """

    verification_prompt = f"""
You are a strict document-grounding verifier.

Your task is to determine whether the ANSWER is fully
supported by the DOCUMENT CONTEXT.

Rules:

1. Use ONLY the DOCUMENT CONTEXT.
2. Do not use outside knowledge.
3. The answer must be directly supported by the context.
4. If the context does not contain enough information
   to support the answer, return NO.
5. If the answer contains information that is not supported
   by the context, return NO.
6. Do not judge whether the answer is generally true.
7. Return ONLY one word:
YES
or
NO

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
{answer}

VERDICT:
"""

    verdict = generate_answer(
        verification_prompt,
        max_new_tokens=5
    ).strip().upper()

    return verdict.startswith("YES")


def ask_question(
    question: str,
    chat_history: list[dict] | None = None
) -> tuple[str, list[dict]]:
    """
    Complete conversational RAG pipeline.
    """

    if chat_history is None:
        chat_history = []

    # -----------------------------------------
    # BUILD STANDALONE QUESTION
    # -----------------------------------------

    standalone_question = build_standalone_question(
        question,
        chat_history
    )

    # -----------------------------------------
    # RETRIEVE CONTEXT
    # -----------------------------------------

    context, sources = retrieve_context(
        standalone_question
    )

    # -----------------------------------------
    # BUILD RAG PROMPT
    # -----------------------------------------

    prompt = build_rag_prompt(
        context=context,
        question=question,
        chat_history=chat_history
    )

    # -----------------------------------------
    # GENERATE ANSWER
    # -----------------------------------------

    answer = generate_answer(
        prompt
    ).strip()

    # -----------------------------------------
    # HANDLE EXPLICIT "NOT FOUND" ANSWER
    # -----------------------------------------

    fallback_message = (
        "I could not find the answer in the provided document."
    )

    if fallback_message.lower() in answer.lower():

        return fallback_message, []

    # -----------------------------------------
    # CHECK WHETHER ANSWER IS GROUNDED
    # -----------------------------------------

    is_grounded = check_answer_grounding(
        question=question,
        answer=answer,
        context=context
    )

    # -----------------------------------------
    # ANSWER NOT SUPPORTED BY DOCUMENT
    # -----------------------------------------

    if not is_grounded:

        return fallback_message, []

    # -----------------------------------------
    # ANSWER SUPPORTED BY DOCUMENT
    # -----------------------------------------

    return answer, sources