from retrieval.vector_store import load_vector_store


def retrieve_context(
    question: str,
    k: int = 3
) -> str:
    """
    Retrieve the most relevant context
    for a user question.
    """

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    return context