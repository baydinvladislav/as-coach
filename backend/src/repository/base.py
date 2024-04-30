from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.repository.abstract import AbstractRepository
from src.utils import validate_uuid


class BaseRepository(AbstractRepository):
    """
    The base repository implements the abstract repository interface.

    Almost all of its subclasses will use its methods for CUD operations.
    but will implement their own methods that perform queries, avoiding the use of filter(),
    however I'll leave the method in because it serves as a convenient way to filter for testing and debugging.
    """

    model = None

    def __init__(self, session):
        self.session = session

    async def create(self, **params):
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
        if not await validate_uuid(pk):
            raise TypeError("Argument is not valid UUID")

        instance = await self.session.get(self.model, pk)
        return instance

    async def get_all(self):
        query = select(self.model)
        instances = await self.session.execute(query)
        return instances.scalars().all()

    async def update(self, pk, **params):
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

    async def delete(self, row_id: str) -> str | None:
        instance = await self.get(row_id)

        if not instance:
            return None

        deleted_pk = str(instance.id)
        await self.session.delete(instance)
        await self.session.commit()
        return deleted_pk

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
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
                        selectinload(getattr(self.model, foreign_key)).subqueryload(sub_query)
                    )
            else:
                f_keys.append(selectinload(getattr(self.model, foreign_key)))

        result = await self.session.execute(
            select(self.model).where(*pairs).options(*f_keys)
        )

        instances = result.scalars().all()
        return instances
