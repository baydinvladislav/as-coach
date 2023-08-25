"""
Class for interacting with storage through SQLAlchemy interlayer
"""

from sqlalchemy import select, update

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
        # TODO: await
        if not validate_uuid(pk):
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

    async def filter(self, attribute_name, attribute_value):
        """
        Forms selection by passed params

        Args:
            :params: unknown pairs of attributes and values for selection
        """
        attribute = getattr(self.model, attribute_name)
        if not attribute_name:
            raise

        result = await self.session.execute(
            select(self.model).where(attribute == attribute_value)
        )

        instances = result.scalars().all()
        return instances

    async def update(self, pk, **params):
        instance = await self.get(pk=pk)

        if not instance:
            return

        query = (
            update(self.model).where(
                self.model.id == str(instance.id)
            ).values(
                **params
            )
        )

        await self.session.execute(query)
        await self.session.commit()
        await self.session.refresh(instance)
