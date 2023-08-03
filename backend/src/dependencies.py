"""
Common dependencies for application
"""

from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src.database import SessionLocal


async def get_db() -> AsyncSession:
    """
    Creates new database session.
    """
    async with SessionLocal() as database:
        try:
            yield database
        finally:
            await database.close()
