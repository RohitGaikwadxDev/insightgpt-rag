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
# PAGE SCROLLING & TARGETED CONTAINER STYLING
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

        /* Target containers using their custom keys for reliable border thickness */
        .st-key-active_docs_box, .st-key-chat_window_box {
            border: 3px solid rgba(120, 120, 120, 0.7) !important;
            border-radius: 10px !important;
        }

        /* Increase thickness for single lines / dividers (st.divider) */
        hr {
            border-top: 3px solid rgba(120, 120, 120, 0.7) !important;
        }
    </style>
    """,
    unsafe_allow_html=True
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
# SESSION STATE & AUTO-DISCOVERY
# -----------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "deleted_files" not in st.session_state:
    st.session_state.deleted_files = set()

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "uploaded_files_list" not in st.session_state:
    # Auto-discover already uploaded files from disk on app launch
    existing_files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith(".pdf") and filename not in st.session_state.deleted_files:
                existing_files.append({
                    "name": filename,
                    "chunks": "Existing"
                })
    st.session_state.uploaded_files_list = existing_files


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

        # APP HEADER
        st.markdown(
            "<h1 style='text-align: center;'>📚 InsightGPT ™</h1>",
            unsafe_allow_html=True
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

        st.markdown(
            "<h3 style='text-align: center;'>AI Powered Document Intelligence Assistant</h3>",
            unsafe_allow_html=True
        )

    # DOCUMENT UPLOAD & ACTIVE DOCUMENTS SECTION
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
            type=["pdf"],
            key=f"file_uploader_{st.session_state.uploader_key}"
        )

        if uploaded_file is not None:
            file_names = [f["name"] for f in st.session_state.uploaded_files_list]

            # Only process if not already listed AND wasn't explicitly deleted during this session
            if (
                uploaded_file.name not in file_names
                and uploaded_file.name not in st.session_state.deleted_files
            ):
                file_path = os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.name
                )

                with open(file_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

                with st.spinner("Processing PDF..."):
                    result = index_pdf(file_path)

                if result["status"] == "indexed":
                    st.session_state.uploaded_files_list.append({
                        "name": result['file_name'],
                        "chunks": result['chunks']
                    })
                    st.success(
                        f"Indexed {result['chunks']} chunks from {result['file_name']}."
                    )
                    st.session_state.uploader_key += 1
                    st.rerun()

                elif result["status"] == "already_indexed":
                    st.session_state.uploaded_files_list.append({
                        "name": result['file_name'],
                        "chunks": "Existing"
                    })
                    st.info(
                        f"{result['file_name']} is already indexed."
                    )
                    st.session_state.uploader_key += 1
                    st.rerun()

        st.divider()

        # --- SCROLLABLE ACTIVE DOCUMENTS BOX (With Targetable Key) ---
        st.subheader(f"Active Documents ({len(st.session_state.uploaded_files_list)})")
        
        doc_container = st.container(height=280, border=True, key="active_docs_box")
        with doc_container:
            if not st.session_state.uploaded_files_list:
                st.info("No documents uploaded yet.")
            else:
                for idx, doc in enumerate(st.session_state.uploaded_files_list):
                    col_info, col_del = st.columns([3, 1])
                    with col_info:
                        st.write(f"📄 **{doc['name']}**")
                        st.caption(f"Chunks: {doc['chunks']}")
                    with col_del:
                        if st.button("🗑️", key=f"del_{doc['name']}", help="Remove document"):
                            target_path = os.path.join(UPLOAD_FOLDER, doc['name'])
                            if os.path.exists(target_path):
                                os.remove(target_path)
                            
                            # Clean up embeddings from ChromaDB
                            try:
                                import chromadb
                                for db_path in ["./chroma_db", "./data/chroma_db", "chroma_db"]:
                                    if os.path.exists(db_path):
                                        client = chromadb.PersistentClient(path=db_path)
                                        for collection in client.list_collections():
                                            try:
                                                collection.delete(where={"source": doc['name']})
                                            except Exception:
                                                pass
                            except Exception:
                                pass
                            
                            # Track that this file was deleted so the uploader doesn't loop-reload it
                            st.session_state.deleted_files.add(doc['name'])
                            
                            st.session_state.uploaded_files_list.pop(idx)
                            st.rerun()

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

        st.markdown(
            "<div style='text-align: center; color: gray; font-size: 12px;'>Python • Qwen • LangChain • ChromaDB • Streamlit</div>",
            unsafe_allow_html=True
        )


# =========================================================
# RIGHT SIDE (Chat Window)
# =========================================================

with right_side:
    with st.container(key="right_section"):        
        # -----------------------------------------
        # CHAT HEADER
        # -----------------------------------------

        st.header("💬 Chat")

        # -----------------------------------------
        # CHAT BOX (With Targetable Key)
        # -----------------------------------------

        chat_box = st.container(
            height=650,
            border=True,
            key="chat_window_box"
        )

        with chat_box:

            if not st.session_state.chat_history:

                # Only show the instruction text if no documents are uploaded yet
                if not st.session_state.uploaded_files_list:
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