"""
Application entrypoint.
"""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from backend.src.config import STATIC_DIR
from backend.src.auth.router import auth_router
from backend.src.coach.router import coach_router
from backend.src.customer.router import customer_router
from backend.src.gym.router import gym_router


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

    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    as_coach.mount(
        "/static",
        StaticFiles(directory=STATIC_DIR),
        name="static"
    )

    app_routers = (
        auth_router,
        coach_router,
        customer_router,
        gym_router
    )

    for router in app_routers:
        as_coach.include_router(router, prefix="/api")

    return as_coach


app = get_application()


@app.get("/")
async def root():
    """
    Test endpoint.
    """
    return "Hello!"
