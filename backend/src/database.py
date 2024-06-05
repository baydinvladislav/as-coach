"""
Database settings module
"""

import os
from dataclasses import dataclass

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from src.shared.config import DATABASE_URL, TEST_ENV


@dataclass
class DatabaseSessionFactory:
    def __init__(self, database_url: str, test_database_url: str = None, test_env: str = "active"):
        self.database_url = test_database_url if test_env == "active" else database_url

    def __post_init__(self) -> None:
        self.sessionmaker = sessionmaker(self._create_engine(), expire_on_commit=False, class_=AsyncSession)

    async def __call__(self) -> Session:
        return await self.create_session()

    async def create_session(self) -> Session:
        return self.sessionmaker()

    async def get_sessionmaker(self):
        return self.sessionmaker

    async def _create_engine(self):
        return create_async_engine(self.database_url, future=True, echo=False, poolclass=NullPool)


class UnitOfWorkFactory(DatabaseSessionFactory):
    async def execute(self, statement, *args, **kwargs):
        with self() as uow:
            return uow.execute(statement, *args, **kwargs)


SessionLocal = DatabaseSessionFactory(
    database_url=DATABASE_URL,
    test_database_url=os.environ.get("TEST_DATABASE_URL"),
    test_env=TEST_ENV,
).get_sessionmaker()

Base = declarative_base()
