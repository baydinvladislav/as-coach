from src.database import SessionLocal


def get_db():
    """
    Creates new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
