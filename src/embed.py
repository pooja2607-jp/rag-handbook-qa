from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def load_and_chunk(pdf_folder="data"):
    all_chunks = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            loader = PyPDFLoader(filepath)
            pages = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)
    return all_chunks


def build_vector_store():
    print("Step 1: Loading and chunking PDF...")
    chunks = load_and_chunk()
    print(f"Created {len(chunks)} chunks.")

    print("\nStep 2: Loading embedding model (first run downloads it, ~80MB)...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("\nStep 3: Creating embeddings and storing in Chroma...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"   # saves to disk so we don't redo this every time
    )

    print("\nDone! Vector store saved to ./chroma_db")
    return vectorstore


if __name__ == "__main__":
    build_vector_store()