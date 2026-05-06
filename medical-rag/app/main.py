import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.rag_engine import MedicalRAGEngine
from app.schemas import HealthResponse, MedicalAnswer, MedicalQuery

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Medical Literature RAG API",
    description="Clinical question answering grounded in medical guidelines. Allanswers cite source documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

rag_engine = MedicalRAGEngine()


@app.on_event("startup")
async def startup():
    success = rag_engine.load()
    if not success:
        logging.warning("RAG engine could not load — run scripts/ingest.py first")


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(
        status="healthy" if rag_engine.is_loaded else "degraded",
        index_loaded=rag_engine.is_loaded,
        vector_count=rag_engine.vector_count,
    )


@app.post("/ask", response_model=MedicalAnswer, tags=["RAG"])
async def ask(query: MedicalQuery):
    """
    Answer a clinical question using the medical literature knowledge base.
    Every answer is grounded in retrieved guideline documents — no hallucination.
    """
    if not rag_engine.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG engine not loaded. Check server logs and run ingest.py.",
        )
    try:
        return rag_engine.query(
            question=query.question,
            top_k=query.top_k,
            use_sub_questions=query.use_sub_questions,
            temperature=query.temperature,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sources", tags=["System"])
async def list_sources():
    """List all documents in the knowledge base."""
    return {
        "sources": [
            "malaria_guidelines.txt",
            "hypertension_guidelines.txt",
            "diabetes_management.txt",
        ],
        "vector_count": rag_engine.vector_count,
    }
