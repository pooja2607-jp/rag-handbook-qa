import streamlit as st
import sys
import os

# Let this file import from the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from query import retrieve_chunks, generate_answer

st.set_page_config(page_title="Academic Regulations Q&A", page_icon="📚")

st.title("📚 Academic Regulations Q&A")
st.write("Ask a question about the B.Tech Academic Regulations document.")

question = st.text_input("Your question:", placeholder="e.g. What is the minimum attendance required?")

if st.button("Ask") and question:
    with st.spinner("Searching document and generating answer..."):
        chunks = retrieve_chunks(question)
        answer = generate_answer(question, chunks)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("See source excerpts used"):
        for i, doc in enumerate(chunks, 1):
            page = doc.metadata.get("page_label", "?")
            st.markdown(f"**Excerpt {i} (Page {page}):**")
            st.write(doc.page_content)
            st.divider()