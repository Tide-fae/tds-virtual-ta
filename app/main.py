from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import initialize_rag   

app = FastAPI()
qa_pipeline = initialize_rag()

class QuestionRequest(BaseModel):
    question: str
    image: str = None  # optional

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


