"""
Application entrypoint.
"""

from fastapi import FastAPI

from src.auth.router import auth_router

app = FastAPI(title="As Coach")
app.include_router(auth_router)


@app.get("/")
def root():
    """
    Test endpoint.
    """
    return "Hello!"
