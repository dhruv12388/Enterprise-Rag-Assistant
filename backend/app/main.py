from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import engine, Base
import app.models  # Registers models for metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create PostgreSQL tables on startup asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

    # Clean up engine on shutdown
    await engine.dispose()


app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["default"])
def root():
    return {"message": "Enterprise RAG Server is Running"}