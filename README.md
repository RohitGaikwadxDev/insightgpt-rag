# 📚 InsightRAG

### AI-Powered Document Intelligence Assistant

InsightRAG is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural-language questions about their content.

Instead of relying only on the language model's internal knowledge, InsightRAG retrieves relevant information from the uploaded documents and uses that context to generate grounded answers.

---

## ✨ Features

- 📄 PDF document upload
- 🔍 Automatic document ingestion
- ✂️ Intelligent text chunking
- 🧠 Hugging Face embeddings
- 🗄️ ChromaDB vector storage
- 🔎 Semantic similarity search
- 💬 Conversational question answering
- 🔄 Follow-up question understanding
- 📚 Source and page references
- 🚫 Reduced hallucination through context-grounded prompting
- ⚡ Local LLM inference
- 🧪 Automated RAG pipeline tests
- 🖥️ Streamlit user interface

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │   PDF Upload    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PDF Loader    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Text Cleaning  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Text Chunking   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Embeddings    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ChromaDB     │
                    └─────────────────┘
                             │
                             │
                    ┌────────▼────────┐
                    │ User Question   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Query Rewriting │
                    │ for Follow-ups  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Semantic Search │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Context + Query │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Qwen LLM      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Answer + Source │
                    └─────────────────┘