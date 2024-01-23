from sqlalchemy import select

from src import Coach
from src.repository.base import BaseRepository


class CoachRepository(BaseRepository):
    """
    Access to Coach storage
    """
    model = Coach

    async def provide_by_username(self, username: str) -> Coach | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        coach = result.fetchone()
        return coach
