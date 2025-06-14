# TDS Virtual TA API

This is the **Virtual Teaching Assistant API** built for the TDS course project at IITM Online BSc program.  
The API answers student queries based on scraped content from the TDS course website and the IITM Discourse forum.

---

## 🔍 Features

- Scrapes data from:
  - TDS Course Pages
  - IITM Discourse Forum Posts
- Uses **RAG (Retrieval Augmented Generation)** with Sentence Transformers and FAISS.
- **FastAPI** REST endpoint for handling questions.
- Deployable via Docker.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/tds-virtual-ta.git
cd tds-virtual-ta
# tds-virtual-ta
