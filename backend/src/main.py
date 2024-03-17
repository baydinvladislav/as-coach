"""
Application entrypoint.
"""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.config import STATIC_DIR
from src.presentation.authentication import auth_router
from src.presentation.customer import customer_router
from src.presentation.library import gym_router


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
        customer_router,
        gym_router
    )

    for router in app_routers:
        as_coach.include_router(router, prefix="/api")

    return as_coach


app = get_application()


@app.get("/health")
async def health_endpoint():
    return "version: AsCoach v.1.0"
