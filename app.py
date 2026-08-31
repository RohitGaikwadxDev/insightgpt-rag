import os
import sys

import streamlit as st


# -----------------------------------------
# IMPORT PROJECT MODULES
# -----------------------------------------

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

from pipeline.indexing_pipeline import index_pdf
from pipeline.rag_pipeline import ask_question


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="InsightGPT",
    page_icon="📚",
    layout="wide"
)


# -----------------------------------------
# PAGE SCROLLING
# -----------------------------------------

st.markdown(
    """
    <style>
        html, body {
            overflow: hidden !important;
        }

        [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
        }

        [data-testid="stMain"] {
            overflow: hidden !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# SESSION STATE
# -----------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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

st.markdown(
    """
    <style>
        .st-key-left_section {
            transform: translateY(-80px);
        }

        .st-key-right_section {
            transform: translateY(-80px);
        }
        
        [data-testid="stChatInput"] {
            transform: translateY(-80px);
        }
        
        .st-key-clear_chat_button {
            transform: translateY(-80px);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TWO SIDES
# =========================================================

left_side, right_side = st.columns(
    [1, 3],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with left_side:
    with st.container(key="left_section"):


        # -----------------------------------------
        # APP HEADER
        # -----------------------------------------

        st.title(
            "📚 InsightGPT ™",
            text_alignment="center"
        )

        st.markdown(
            """
            <style>
                h3 {
                    font-size: 20px !important;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "AI Powered Document Intelligence Assistant",
            text_alignment="center"
        )


    # -----------------------------------------
    # DOCUMENT UPLOAD
    # -----------------------------------------
 
    with st.container(key="upload_section"):

        st.markdown(
            """
            <style>
                .st-key-upload_section {
                    transform: translateY(-100px);
                }

                .st-key-upload_section h2 {
                    font-size: 20px !important;
                }

                .st-key-upload_section [data-testid="stFileUploader"] {
                    min-height: 400px;
                }
                .st-key-left_footer {
                    transform: translateY(-90px);
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.divider()

        st.header("📄 Upload PDF")

        uploaded_file = st.file_uploader(
            "Choose a PDF",
            type=["pdf"]
        )
        st.divider()

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

        st.success(
            "Document uploaded successfully ✓"
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
    

    # -----------------------------------------
    # LEFT FOOTER
    # -----------------------------------------


    with st.container(key="left_footer"):

        st.markdown(
            """
            <div style="text-align: center;">
                Developed with ❤️ by Rohit Gaikwad
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Python • Qwen • LangChain • ChromaDB • Streamlit",
            text_alignment="center"
        )


# =========================================================
# RIGHT SIDE
# =========================================================

with right_side:
    with st.container(key="right_section"):        
        # -----------------------------------------
        # CHAT HEADER
        # -----------------------------------------

        st.header("💬 Chat")

        # -----------------------------------------
        # CHAT BOX
        # -----------------------------------------
        #
        # ONLY THIS AREA SCROLLS
        #

        chat_box = st.container(
            height=650,
            border=True
        )

        with chat_box:

            if not st.session_state.chat_history:

                st.info(
                    "Upload a PDF and ask a question to get started."
                )

            else:

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

                            if message.get("sources"):

                                with st.container(border=True):

                                    st.markdown("**📚 Sources**")

                                    for source in message["sources"]:

                                        st.caption(
                                            f"📄 {source['source']} "
                                            f"— Page {source['page'] + 1}"
                                        )

    # -----------------------------------------
    # INPUT
    # -----------------------------------------

    
    question = st.chat_input(
        "Please enter your query..."
    )

    # -----------------------------------------
    # CLEAR CHAT
    # -----------------------------------------
    with st.container(key="clear_chat_button"):
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    


    # =========================================================
    # PROCESS QUESTION
    # =========================================================

    if question:

        # -----------------------------------------
        # PREVIOUS CHAT HISTORY
        # -----------------------------------------

        previous_history = (
            st.session_state.chat_history.copy()
        )

        # -----------------------------------------
        # GENERATE ANSWER
        # -----------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            answer, sources = ask_question(
                question,
                previous_history
            )

        # -----------------------------------------
        # SAVE USER MESSAGE
        # -----------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # -----------------------------------------
        # SAVE ASSISTANT MESSAGE
        # -----------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

        # -----------------------------------------
        # RERUN
        # -----------------------------------------

        st.rerun()