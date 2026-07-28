from fastapi import APIRouter
from app.services.rag_service import query_rag_pipeline
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 4

class QueryResponse(BaseModel):
    answer: str
    sources: list = []

@router.post("/api/v1/documents/query", response_model=QueryResponse)
async def query_documents(payload: QueryRequest):
    result = await query_rag_pipeline(payload.query, payload.top_k)
    if isinstance(result, str):
        return {"answer": result, "sources": []}
    return result
