import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

# Import RAG components
from retriever import Retriever
from generator import generate_answer

from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor()

app = FastAPI(title="RAG Troubleshooting API")

# Allow requests from any origin (for testing; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://<your-app>.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG on startup
retriever = Retriever(None)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 2


class QueryResponse(BaseModel):
    query: str
    answer: str


@app.post("/search")
def search(request: QueryRequest) -> QueryResponse:
    """Search KB and return troubleshooting answer."""
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Retrieve and generate
    retrieved = retriever.search(query, top_k=request.top_k)
    answer = generate_answer(query, retrieved)
    
    return QueryResponse(query=query, answer=answer)


@app.get("/health")
def health_check():
    """Kubernetes/cloud health check."""
    return {"status": "healthy"}


# Serve the built chat UI (frontend/ compiled into static/ by Vite).
# Mounted last so API routes above take precedence.
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="ui")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
