"""
Application entrypoint.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.src.auth.router import auth_router


def get_application() -> FastAPI:
    """
    Initialises the application
    """
    as_coach = FastAPI(title="As Coach")

    as_coach.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    as_coach.include_router(auth_router, prefix="/api")

    return as_coach


app = get_application()


@app.get("/")
async def root():
    """
    Test endpoint.
    """
    return "Hello!"
