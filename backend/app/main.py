from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Enterprise RAG Assistant API")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Enterprise RAG Assistant Backend is running successfully!"}