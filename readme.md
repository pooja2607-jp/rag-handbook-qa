📚 Academic Regulations Q&A — RAG-based Document Assistant
A Retrieval-Augmented Generation (RAG) system that lets you ask natural-language questions about a college's B.Tech Academic Regulations document and get accurate, cited answers — instead of manually searching through a 11-page PDF.
Live demo: https://rag-handbook-app-kfhvrgkgvdjysejoo5bztc.streamlit.app/
---
🧠 Problem
Searching a dense academic regulations PDF for a specific rule (attendance %, credit requirements, grading policy) is slow and error-prone with plain Ctrl+F search — different sections use different wording for related rules, so keyword search often misses what you're looking for.
💡 Solution
This project builds a RAG pipeline that:
Breaks the document into small, searchable chunks
Converts each chunk into a vector embedding (semantic meaning, not just keywords)
Retrieves the most relevant chunks for any question using semantic similarity search
Passes those chunks to an LLM to generate a grounded, cited answer
The result: ask "what's the minimum attendance to sit for exams?" and get "75%, per Page 3, Section 7.1" — even though the question and the document use slightly different phrasing.
---
⚙️ How it works (architecture)
```
PDF Document
     │
     ▼
[Chunking]  → splits into ~500-character chunks (RecursiveCharacterTextSplitter)
     │
     ▼
[Embedding] → sentence-transformers/all-MiniLM-L6-v2 (local, free)
     │
     ▼
[Vector Store] → ChromaDB (persisted locally)
     │
     ▼
User Question → embedded → similarity search → top-3 relevant chunks
     │
     ▼
[LLM Generation] → Llama 3.1 8B (via Groq API) → grounded answer + source citation
     │
     ▼
Streamlit Web UI
```
🛠️ Tech Stack
Component	Tool
PDF parsing	`pypdf` / `PyPDFLoader`
Chunking	LangChain `RecursiveCharacterTextSplitter`
Embeddings	`sentence-transformers` (`all-MiniLM-L6-v2`) — local, free, no API key
Vector database	ChromaDB (persisted to disk)
LLM	Llama 3.1 8B Instant via Groq API (free tier)
Frontend	Streamlit
Language	Python
---
📊 Evaluation
Rather than assuming the system works, I built a hand-labeled evaluation set of 20 question-answer pairs covering attendance rules, grading, credit/promotion requirements, and examination malpractice penalties — then measured the pipeline's accuracy automatically.
Result: 16/20 correct (80%)
Failure analysis
Digging into the 4 misses revealed two distinct issues, not random failure:
3 false negatives in the evaluation script itself — the generated answers were actually correct (e.g., "expelled" instead of the exact keyword "Expulsion"), but my keyword-matching check was too strict to catch paraphrased-but-correct answers.
1 genuine retrieval failure — a question about the maximum years to complete the degree retrieved a related-but-different clause (the 10-year seat-forfeiture rule) instead of the correct 8-year completion rule, since both rules use similar language in nearby sections.
This taught me that (a) simple keyword-based evaluation has real limits and a semantic/LLM-based grading approach would be more accurate, and (b) documents with multiple similar-sounding rules can cause retrieval to conflate related clauses — a good candidate for future improvement via better chunking or re-ranking.
Full results: `evaluation_results.txt` · `evaluation_results.json`
---
🚀 Running it locally
```bash
# 1. Clone the repo
git clone https://github.com/pooja2607-jp/rag-handbook-qa.git
cd rag-handbook-qa

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
# Create a .env file in the project root with:
# GROQ_API_KEY=your_key_here

# 5. Build the vector database (one-time, run after adding/changing the PDF in data/)
python src/embed.py

# 6. Run the evaluation (optional)
python src/evaluate.py

# 7. Launch the app
streamlit run app.py
```
---
🔮 What I'd improve next
Add hybrid search (keyword + semantic) to reduce retrieval confusion between similar clauses
Replace strict keyword-match evaluation with an LLM-based grader for more accurate scoring
Support multiple documents (compare regulations across colleges/years)
Add a re-ranking step after retrieval to improve precision on ambiguous questions
---
📁 Project Structure
```
rag-handbook-qa/
├── data/                      # source PDF documents
├── src/
│   ├── ingest.py              # PDF loading + chunking
│   ├── embed.py                # embedding generation + vector store setup
│   ├── query.py                 # retrieval + LLM answer generation
│   └── evaluate.py             # automated evaluation against 20 test questions
├── app.py                      # Streamlit web interface
├── evaluation_results.json/txt # evaluation output
└── requirements.txt
```
