from src.pdf_loader import load_pdf
from src.text_splitter import split_documents

pdf_path = "data/uploaded_pdfs/Python_Interview_Questions.pdf"

documents = load_pdf(pdf_path)

print(f"Total Documents Loaded: {len(documents)}")
print(type(documents))
print(type(documents[0]))
print(documents[3].page_content)

chunks = split_documents(documents)

print(f"Total Chunks: {len(chunks)}")
print(type(chunks))
print(type(chunks[0]))
print(chunks[0].page_content)
print(chunks[0].metadata)
