# 🤖 RockyBot – AI RAG Chatbot

RockyBot is an AI-powered chatbot that allows users to ask questions from **news articles, PDFs, and Word documents** using Retrieval-Augmented Generation (RAG).

---

## 🚀 Live Demo

👉 https://rockybot-ai-rag-chatbot-main.streamlit.app/

---

## 🧠 Features

* 🔗 Extract information from URLs
* 📄 Upload and query PDF & Word files
* 💬 ChatGPT-style conversational UI
* ⚡ Fast responses using Groq LLM
* 📚 Context-aware answers using RAG
* 🧹 Clear chat functionality

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM:** Groq (LLaMA 3)
* **Embeddings:** HuggingFace (MiniLM)
* **Vector Database:** FAISS
* **Framework:** LangChain

---

## 📂 Project Structure

```
rockybot-rag-chatbot/
│
├── app.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

## ⚙️ Installation (Local Setup)

```bash
git clone https://github.com/your-username/rockybot-rag-chatbot.git
cd rockybot-rag-chatbot
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy your repository
4. Add secret in settings:

```
GROQ_API_KEY=your_api_key_here
```

---

## 🎯 Use Cases

* News research & summarization
* Document Q&A
* Study assistant
* Knowledge extraction

---

## 📸 Screenshots

<img width="1891" height="831" alt="image" src="https://github.com/user-attachments/assets/557f0cae-d1c3-443a-89ef-251a57f4893d" />


---

## 👨‍💻 Author

**Anand Gupta**
AI/ML Engineer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
