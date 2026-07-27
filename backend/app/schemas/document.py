from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="The question or search prompt from the user.")
    top_k: int = Field(default=4, description="Number of context chunks to retrieve from Qdrant.")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="The synthesized answer from the LLM based on retrieved context.")
    sources: list[str] = Field(default=[], description="List of source text chunks used to answer the query.")