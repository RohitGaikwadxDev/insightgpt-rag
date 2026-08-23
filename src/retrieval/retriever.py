from retrieval.vector_store import load_vector_store


def retrieve_context(
    question: str,
    k: int = 3
) -> tuple[str, list[dict]]:
    """
    Retrieve the most relevant document chunks
    for a user question.
    """

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    context_parts = []
    sources = []
    seen_sources = set()

    for document, score in results:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page",
            "Unknown page"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {document.page_content}"
        )

        source_key = (
            source,
            page
        )

        if source_key not in seen_sources:

            sources.append(
                {
                    "source": source,
                    "page": page,
                    "score": score
                }
            )

            seen_sources.add(
                source_key
            )

    context = "\n\n".join(
        context_parts
    )

    return context, sources