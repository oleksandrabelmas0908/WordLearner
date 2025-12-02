from core.settings import settings
from core.db.models import Base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from collections.abc import AsyncGenerator


async def get_engine():
    engine = create_async_engine(settings.database_url, echo=True)
    return engine



async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = await get_engine()
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_tables() -> None:
    engine = await get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)