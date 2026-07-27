from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# 1. Base class for all SQLAlchemy Models
class Base(DeclarativeBase):
    pass


# 2. Create Async Engine
engine: AsyncEngine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,  # Set to True if you want to log raw SQL queries in terminal
    future=True,
    pool_pre_ping=True  # Automatically checks/rebinds broken stale connections
)


# 3. Create Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# 4. FastAPI Dependency for Database Sessions
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a transactional database session for FastAPI endpoints.
    Automatically closes the session after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()