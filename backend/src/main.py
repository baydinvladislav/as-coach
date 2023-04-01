"""
Application entrypoint.
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import auth_router
from src.customer.router import customer_router

APP_ROUTERS = (
    auth_router, customer_router
)


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

    for router in APP_ROUTERS:
        as_coach.include_router(router, prefix="/api")

    return as_coach


app = get_application()


@app.get("/")
async def root():
    """
    Test endpoint.
    """
    return "Hello!"
