from sqlalchemy import select, delete, literal_column
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from src import Coach
from src.schemas.authentication_schema import CoachRegistrationData


class CoachRepository:
    async def create_coach(self, uow: Session, data: CoachRegistrationData):
        statement = (
            insert(Coach)
            .values(
                username=data.username,
                fcm_token=data.fcm_token,
                first_name=data.first_name,
                password=data.password,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        coach = result.fetchone()

        if coach is None:
            return None

        return Coach.from_orm(coach)

    async def update_coach(self, uow: Session, **kwargs):
        statement = (
            insert(Coach)
            .values(**kwargs)
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        coach = result.fetchone()

        if coach is None:
            return None

        return Coach.from_orm(coach)

    async def delete_coach(self, uow: Session, pk: str):
        delete_stmt = delete(Coach).where(Coach.id == pk)
        result = await uow.execute(delete_stmt)
        uow.commit()

        if result.rowcount == 0:
            return None

        return pk

    async def provide_by_username(self, uow: Session, username: str) -> Coach | None:
        query = select(Coach).where(Coach.username == username)
        result = await uow.execute(query)
        coach = result.fetchone()
        return coach
