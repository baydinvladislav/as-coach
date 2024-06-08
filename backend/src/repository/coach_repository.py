from sqlalchemy import select, literal_column
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from src import Coach


class CoachRepository:
    async def create_coach(self, uow: Session, data: CustomerRegistrationData) -> CustomerOut | None:
        statement = (
            insert(Coach)
            .values(
                coach_id=data.coach_id,
                telegram_username=data.telegram_username,
                first_name=data.first_name,
                last_name=data.last_name,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = uow.execute(statement).fetchone()
        if result is None:
            return None

        return Coach.from_orm(result)

    async def update_coach(self, uow: Session, data: CustomerRegistrationData) -> CustomerOut | None:
        ...

    async def delete_coach(self, uow: Session, data: CustomerRegistrationData) -> CustomerOut | None:
        ...

    async def provide_by_username(self, uow: Session, username: str) -> Coach | None:
        query = select(Coach).where(Coach.username == username)
        result = await uow.execute(query)
        coach = result.fetchone()
        return coach
