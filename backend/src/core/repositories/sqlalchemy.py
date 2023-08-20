"""
Class for interacting with storage through SQLAlchemy interlayer
"""

from sqlalchemy import select, and_

from src.core.repositories.abstract import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """
    Implements connection to storage
    """

    def __init__(self, model, session):
        self.model = model
        self.session = session

    async def create(self, **params):
        """
        Creates new instance in storage

        Args:
            :params: unknown pairs of attributes and values for new instance
        """
        invalid_attrs = [attribute for attribute, value in params.items() if attribute not in self.model.__dict__]
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

        instance = await self.session.get(self.model, pk)
        return instance

    async def get_all(self):
        """
        Returns instances from tables
        """

        query = select(self.model)
        instances = await self.session.execute(query)
        return instances

    async def filter(self, **params):
        """
        Forms selection by passed params

        Args:
            :params: unknown pairs of attributes and values for selection
        """

        query = select(self.model)
        filters = []

        for field, value in params.items():
            if hasattr(self.model, field):
                filters.append(getattr(self.model, field) == value)
            # raise error if field doesn't exist

        if filters:
            query = query.where(and_(*filters))

        result = await self.session.execute(query)
        instances = result.fetchall()

        return instances
