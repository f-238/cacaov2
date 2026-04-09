from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.models.base import Base


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    future=True,
    pool_pre_ping=True,
)

sync_engine = create_engine(
    settings.sync_database_url,
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


__all__ = [
    "Base",
    "engine",
    "sync_engine",
    "AsyncSessionLocal",
    "SyncSessionLocal",
    "get_db",
]
