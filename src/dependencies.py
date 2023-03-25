"""
Common dependencies for application
"""

from src.database import SessionLocal


def get_db():
    """
    Creates new database session.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
