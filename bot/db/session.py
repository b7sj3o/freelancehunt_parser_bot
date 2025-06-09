from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine)