import os
import streamlit as st
import pickle
import re
import time

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader
from docx import Document

# ---------------- API KEY (DEPLOY ONLY) ----------------
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Add GROQ_API_KEY in Streamlit Secrets")
    st.stop()

# ---------------- PAGE ----------------
st.set_page_config(page_title="RockyBot", page_icon="🤖", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.chat-container {
    max-width: 850px;
    margin: auto;
}
.user-msg {
    background: #343541;
    color: #e5e7eb;
    padding: 10px 14px;
    border-radius: 18px;
    margin: 6px 0;
    display: inline-block;
    max-width: 70%;
    float: right;
}
.bot-msg {
    background: rgba(255,255,255,0.05);
    color: #e5e7eb;
    padding: 10px 14px;
    border-radius: 18px;
    margin: 6px 0;
    display: inline-block;
    max-width: 70%;
    float: left;
    border: 1px solid rgba(255,255,255,0.08);
}
.chat-row::after {
    content: "";
    display: block;
    clear: both;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h2 style='text-align:center;color:#e5e7eb;'>🤖 RockyBot</h2>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("### 🌐 Add Data")

urls = []
for i in range(2):
    u = st.sidebar.text_input(f"🔗 URL {i+1}")
    if u:
        urls.append(u)

uploaded_file = st.sidebar.file_uploader(
    "📄 Upload (PDF / Word) — Max 50MB",
    type=None
)

# ---------------- PROCESS ----------------
if st.sidebar.button("🚀 Process"):
    docs = []

    if urls:
        loader = WebBaseLoader(urls)
        docs.extend(loader.load())

    if uploaded_file:
        if uploaded_file.size > 50 * 1024 * 1024:
            st.sidebar.error("❌ File too large")
            st.stop()

        filename = uploaded_file.name.lower()

        if not (filename.endswith(".pdf") or filename.endswith(".docx")):
            st.sidebar.error("❌ Only PDF or Word allowed")
            st.stop()

        text = ""

        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""

        else:
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"

        splitter = RecursiveCharacterTextSplitter(chunk_size=800)
        docs.extend(splitter.create_documents([text]))

    splitter = RecursiveCharacterTextSplitter(chunk_size=800)
    docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(docs, embeddings)

    with open("faiss.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

    st.sidebar.success("✅ Ready!")

# ---------------- CLEAR CHAT ----------------
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat = []

# ---------------- SESSION ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- LLM ----------------
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.6)

def clean(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return "\n".join(dict.fromkeys(text.split("\n")))

# ---------------- INPUT ----------------
query = st.chat_input("💬 Ask anything...")

# ---------------- QUERY ----------------
if query:
    st.session_state.chat.append(("user", query))

    if not os.path.exists("faiss.pkl"):
        answer = "⚠️ Please process data first."
    else:
        with open("faiss.pkl", "rb") as f:
            vectorstore = pickle.load(f)

        docs = vectorstore.as_retriever().invoke(query)[:2]
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
        Answer briefly and clearly (max 3-4 lines).

        Context:
        {context}

        Question: {query}
        """

        response = llm.invoke(prompt)
        answer = clean(response.content)

    st.session_state.chat.append(("bot", answer))

# ---------------- DISPLAY ----------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f"<div class='chat-row'><div class='user-msg'>{msg}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-row'><div class='bot-msg'>🤖 {msg}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
