from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import json
from dotenv import load_dotenv  # ✅ NEW
import os                      # ✅ NEW

load_dotenv()  # ✅ NEW — loads variables from .env file

def initialize_rag():
    # Load course content
    with open("course_content.json") as f:
        course_data = json.load(f)
    course_docs = [
        {"text": f"# {section['section']}\n\n{''.join(section['content'])}", "metadata": {"url": section["url"]}}
        for section in course_data
    ]
    
    # Load discourse posts
    with open("discourse_content.json") as f:
        discourse_data = json.load(f)
    discourse_docs = [
        {"text": ''.join(post['content']), "metadata": {"url": post["url"]}}
        for post in discourse_data
    ]
    
    documents = course_docs + discourse_docs

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents(
        texts=[doc["text"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents]
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore = FAISS.from_documents(docs, embeddings)

    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # ✅ NEW — from .env

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-small",
        huggingfacehub_api_token=HUGGINGFACE_API_KEY   # ✅ uses key from .env
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
