"""
Database settings module
"""

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine  # type: ignore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from dotenv import load_dotenv

from .config import DATABASE_URL, TEST_ENV


if bool(TEST_ENV):
    load_dotenv()
    TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
    engine = AsyncEngine(create_async_engine(
        str(TEST_DATABASE_URL), future=True, echo=False, poolclass=NullPool
    ))
else:
    engine = AsyncEngine(create_async_engine(
        DATABASE_URL, future=True, echo=False, poolclass=NullPool
    ))

SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
