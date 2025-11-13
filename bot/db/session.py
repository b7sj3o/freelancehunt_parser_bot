from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import settings


engine = create_async_engine(settings.DATABASE_URL, future=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db(drop: bool = False):
    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)