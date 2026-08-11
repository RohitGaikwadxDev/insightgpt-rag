from retrieval.retriever import retrieve_context
from llm.llm import generate_answer
from prompts.rag_prompt import build_rag_prompt


def ask_question(question: str) -> str:
    """
    Complete RAG pipeline.

    Question
        ↓
    Retrieve Context
        ↓
    Build Prompt
        ↓
    Generate Answer
    """

    context = retrieve_context(question)

    prompt = build_rag_prompt(
        context=context,
        question=question
    )

    answer = generate_answer(prompt)

    return answer