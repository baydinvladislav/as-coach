"""
Common dependencies for application
"""

from src.database import SessionLocal


async def get_db():
    """
    Creates new database session.
    """
    async with SessionLocal() as database:
        try:
            yield database
        finally:
            await database.close()
