"""
Class for interacting with storage through SQLAlchemy interlayer
"""

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.core.repositories.abstract import AbstractRepository
from src.utils import validate_uuid


class SQLAlchemyRepository(AbstractRepository):
    """
    Implements connection to storage
    """
    model = None

    def __init__(self, session):
        self.session = session

    async def create(self, **params):
        """
        Creates new instance in storage

        Args:
            :params: unknown pairs of attributes and values for new instance
        """
        invalid_attrs = [
            attribute for attribute, value in params.items()
            if attribute not in self.model.__dict__
        ]
        if invalid_attrs:
            raise AttributeError(
                f"Passed invalid column to create new object of {self.model}\n"
                f"Columns do not exist: " + ", ".join(invalid_attrs)
            )

        new_instance = self.model(**params)
        self.session.add(new_instance)
        await self.session.commit()

        return new_instance

    async def get(self, pk):
        """
        Returns instance by their primary key
        """
        if not await validate_uuid(pk):
            raise TypeError("Argument is not valid UUID")

        instance = await self.session.get(self.model, pk)
        return instance

    async def get_all(self):
        """
        Returns all instances from tables
        """
        query = select(self.model)
        instances = await self.session.execute(query)
        return instances.scalars().all()

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        """
        Forms selection by passed params

        Args:
            filters: dictionary with attributes and values
            foreign_keys: list of foreign keys fields
            sub_queries: list of fields for sub queries
        """
        if foreign_keys is None:
            foreign_keys = []

        if sub_queries is None:
            sub_queries = []

        pairs = []
        for attr, val in filters.items():
            if not hasattr(self.model, attr):
                raise AttributeError(
                    f"{self.model} model doesn't have field {attr}. "
                    f"Updating canceled"
                )

            attribute = getattr(self.model, attr)
            pairs.append(attribute == val)

        f_keys = []
        for foreign_key in foreign_keys:
            if sub_queries:
                for sub_query in sub_queries:
                    f_keys.append(
                        selectinload(
                            getattr(self.model, foreign_key)
                        ).subqueryload(sub_query)
                    )
            else:
                f_keys.append(selectinload(getattr(self.model, foreign_key)))

        result = await self.session.execute(
            select(self.model).where(*pairs).options(*f_keys)
        )

        instances = result.scalars().all()
        return instances

    async def update(self, pk, **params):
        """
        Updates instance into storage

        Args:
             pk: primary key of the instance being updated
             params: parameters for instance updating
        """
        instance = await self.get(pk=pk)

        if not instance:
            return

        query = (
            update(self.model).where(
                self.model.id == str(instance.id)
            ).values(
                **params,
                modified=datetime.now()
            )
        )

        await self.session.execute(query)
        await self.session.commit()
        await self.session.refresh(instance)
