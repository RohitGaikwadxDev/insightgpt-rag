import os
import sys
import streamlit as st


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)


from pipeline.indexing_pipeline import index_pdf
from pipeline.rag_pipeline import ask_question


st.set_page_config(
    page_title="InsightRAG",
    page_icon="📚",
    layout="wide"
)


st.title("📚 InsightRAG")
st.subheader("AI Powered Document Intelligence Assistant")


UPLOAD_FOLDER = os.path.join(
    "data",
    "uploaded_pdfs"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


st.header("Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as file:
        file.write(
            uploaded_file.getbuffer()
        )

    with st.spinner(
        "Indexing PDF..."
    ):

        total_chunks = index_pdf(
            file_path
        )

    st.success(
        f"Indexed {total_chunks} chunks successfully!"
    )


st.divider()


st.header("Ask Questions")

question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):

    if question.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Generating answer..."
        ):

            answer = ask_question(
                question
            )

        st.subheader(
            "Answer"
        )

        st.write(
            answer
        )