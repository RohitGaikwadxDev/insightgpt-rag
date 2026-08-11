import re

from langchain_core.documents import Document


def clean_text(text: str) -> str:
    """
    Clean raw text extracted from PDF pages.
    """

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r" *\n *", "\n", text)

    corrections = {
        "vdeo": "video",
        "teh": "the",
        " adn ": " and "
    }

    for wrong, correct in corrections.items():
        text = text.replace(
            wrong,
            correct
        )

    return text.strip()


def clean_documents(
    documents: list[Document]
) -> list[Document]:
    """
    Clean every LangChain Document.
    """

    cleaned_documents = []

    for document in documents:

        document.page_content = clean_text(
            document.page_content
        )

        cleaned_documents.append(
            document
        )

    return cleaned_documents