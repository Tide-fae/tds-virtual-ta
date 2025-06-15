from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import initialize_rag   #Correct import for rag.py
from app.scraper import scrape_course_content, scrape_discourse_posts  #import scraper functions if needed

app = FastAPI()
qa_pipeline = initialize_rag()

class QuestionRequest(BaseModel):
    question: str
    image: str = None  # Optional

@app.get("/")
def health_check():
    return {"status": "TDS Virtual TA is running"}

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    result = qa_pipeline({"query": request.question})
    return {
        "answer": result["result"],
        "links": [
            {"url": doc.metadata["url"], "text": doc.page_content[:100]}
            for doc in result["source_documents"]
        ]
    }
