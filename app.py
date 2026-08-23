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


# -----------------------------------------
# SESSION STATE
# -----------------------------------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# -----------------------------------------
# PAGE HEADER
# -----------------------------------------

st.title("📚 InsightRAG")

st.subheader(
    "AI Powered Document Intelligence Assistant"
)


# -----------------------------------------
# UPLOAD CONFIGURATION
# -----------------------------------------

UPLOAD_FOLDER = os.path.join(
    "data",
    "uploaded_pdfs"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# -----------------------------------------
# PDF UPLOAD
# -----------------------------------------

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

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    with st.spinner(
        "Processing PDF..."
    ):

        result = index_pdf(
            file_path
        )


    if result["status"] == "indexed":

        st.success(
            f"Indexed {result['chunks']} "
            f"chunks from "
            f"{result['file_name']}."
        )

    elif result["status"] == "already_indexed":

        st.info(
            f"{result['file_name']} "
            f"is already indexed."
        )


st.divider()


# -----------------------------------------
# CHAT HEADER
# -----------------------------------------

st.header("💬 Chat")


# -----------------------------------------
# CLEAR CHAT
# -----------------------------------------

if st.button("🗑️ Clear Chat"):

    st.session_state.chat_history = []

    st.rerun()


# -----------------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------------

for message in st.session_state.chat_history:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.write(
                message["content"]
            )


# -----------------------------------------
# QUESTION INPUT
# -----------------------------------------

question = st.chat_input(
    "Please enter your query..."
)


if question:

    # -------------------------------------
    # DISPLAY USER QUESTION
    # -------------------------------------

    with st.chat_message("user"):

        st.write(
            question
        )


    # -------------------------------------
    # GENERATE ANSWER
    # -------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Generating answer..."
        ):

            answer, sources = ask_question(
                question,
                st.session_state.chat_history
            )


        st.write(
            answer
        )


        # ---------------------------------
        # SOURCES
        # ---------------------------------

        if sources:

            st.markdown(
                "**📚 Sources**"
            )

            displayed_sources = set()

            for source in sources:

                source_name = source["source"]

                page_number = source["page"]

                if isinstance(
                    page_number,
                    int
                ):

                    page_number += 1


                source_key = (
                    source_name,
                    page_number
                )


                if source_key in displayed_sources:

                    continue


                displayed_sources.add(
                    source_key
                )


                st.caption(
                    f"📄 {source_name} "
                    f"— Page {page_number}"
                )


    # -------------------------------------
    # SAVE CONVERSATION
    # -------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )


    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )