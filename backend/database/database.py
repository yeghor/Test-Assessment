from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)
from sqlalchemy import text
from dotenv import load_dotenv
from os import getenv
from .models import Base
import asyncio

from config import settings

load_dotenv()

engine: AsyncEngine = None

async def create_engine() -> AsyncEngine:
    """Set mode - "prod" to main database | "test" to test database"""

    global engine
    if engine:
        return engine

    for i in range(settings.pg_retries):
        try:
            engine = create_async_engine(url=settings.pg_dsn, echo=settings.pg_echo)
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            return engine
        except Exception:
            print(f"{i+1}-th Connection failed or not ready yet")
            await asyncio.sleep(settings.pg_retry_delay)
    raise ConnectionError("Failed to connect to PostgresSQL")


def create_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine,
    )


# async def drop_all(engine: AsyncEngine, Base: Base) -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


async def initialize_models(engine: AsyncEngine, Base: Base) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_engine() -> AsyncEngine:
    return await create_engine()


def get_sessionlocal(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(engine=engine)
