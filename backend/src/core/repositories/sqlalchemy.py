"""

"""

from sqlalchemy import select, and_

from src.core.repositories.abstract import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """"""

    def __init__(self, model, session):
        self.model = model
        self.session = session

    async def create(self, **params):
        """"""

        new_instance = self.model(**params)
        self.session.add(new_instance)
        await self.session.commit(new_instance)
        # or yield?
        return new_instance

    async def get(self, pk):
        """"""

        instance = await self.session.get(self.model, pk)
        return instance

    async def get_all(self):
        """"""

        query = select(self.model)
        instances = await self.session.execute(query)
        return instances

    async def filter(self, **params):
        """"""

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
