import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load the API key from .env
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def load_vector_store():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )
    return vectorstore


def retrieve_chunks(question, k=3):
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(question, k=k)
    return results


def generate_answer(question, chunks):
    # Build context text from the retrieved chunks, with page numbers
    context_parts = []
    for doc in chunks:
        page = doc.metadata.get("page_label", "?")
        context_parts.append(f"[Page {page}]: {doc.page_content}")
    context = "\n\n".join(context_parts)

    prompt = f"""You are a helpful assistant answering questions about a college's academic regulations document.

Use ONLY the following excerpts to answer the question. If the answer isn't in the excerpts, say "I don't have enough information to answer that."

Excerpts:
{context}

Question: {question}

Answer clearly and mention which page(s) you used."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def ask(question):
    chunks = retrieve_chunks(question)
    answer = generate_answer(question, chunks)
    print(f"\nQuestion: {question}")
    print(f"\nAnswer:\n{answer}")


if __name__ == "__main__":
    ask("What is the minimum attendance required to sit for exams?")
def ask(question):
    print("Retrieving chunks...")
    chunks = retrieve_chunks(question)
    print("Got chunks, calling LLM...")
    answer = generate_answer(question, chunks)
    print("Got answer!")
    print(f"\nQuestion: {question}")
    print(f"\nAnswer:\n{answer}")