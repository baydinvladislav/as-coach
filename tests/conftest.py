from dependencies import get_db
from main import app


@app.on_event("startup")
async def startup_event():
    from tests.tests import engine, override_get_db
    from database import Base

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
