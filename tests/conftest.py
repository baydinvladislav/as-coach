from src.main import app
from src.dependencies import get_db
from tests.dependencies import override_get_db


@app.on_event("startup")
async def startup_event():
    app.dependency_overrides[get_db] = override_get_db
