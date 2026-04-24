from .database import get_engine, get_sessionlocal


async def get_session_depends():
    """
    Automatically closes session.\n\n 
    Does not commit transaction on close
    Use with fastAPI Depends()!
    """
    try:
        engine = await get_engine()
        SessionLocal = get_sessionlocal(engine=engine)
        async with SessionLocal() as conn:
            yield conn
    finally:
        await conn.aclose()  # await engine.dispose()
