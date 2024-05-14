from sqlalchemy import select

from src import Coach
from src.repository.base_repository import BaseRepository


class CoachRepository(BaseRepository):
    model = Coach

    async def provide_by_username(self, username: str) -> Coach | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        coach = result.fetchone()
        return coach
