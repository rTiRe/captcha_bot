from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from typing_extensions import AsyncGenerator

from config.settings import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.db_url)


def create_session(_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)

@asynccontextmanager
async def get_db():
    async with async_session() as db:
        yield db
