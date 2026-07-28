from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the main FastAPI application instance (this resolves the Render 'app not found' error)
app = FastAPI(
    title="Enterprise RAG Backend",
    version="1.0.0"
)

# Enable CORS so your Streamlit frontend can communicate with this backend without restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include your document routing endpoints
from app.services.rag_service import query_rag_pipeline
from pydantic import BaseModel
from fastapi import APIRouter

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

# Register the router to the main app instance under /api/v1 prefix if needed, or directly
app.include_router(router)

@app.get("/")
def root():
    return {"status": "Enterprise RAG Backend is online and fully operational"}
