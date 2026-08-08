from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_and_chunk(pdf_folder="data"):
    all_chunks = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            print(f"Loading {filename}...")

            # Step A: extract raw text from the PDF, page by page
            loader = PyPDFLoader(filepath)
            pages = loader.load()

            # Step B: split the text into small chunks (~500 characters, with overlap)
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
            )
            chunks = splitter.split_documents(pages)
            all_chunks.extend(chunks)

    print(f"\nTotal chunks created: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = load_and_chunk()
    print("\n--- Example chunk ---")
    print(chunks[0].page_content)
    print("\n--- Metadata (which file/page it came from) ---")
    print(chunks[0].metadata)