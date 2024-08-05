from sqlalchemy import select, update, delete, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from src import Coach
from src.presentation.schemas.register import CoachRegistrationData
from src.schemas.coach_dto import CoachDtoSchema


class CoachRepository:
    async def create_coach(self, uow: AsyncSession, data: CoachRegistrationData) -> CoachDtoSchema | None:
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

        return CoachDtoSchema.from_orm(coach)

    async def update_coach(self, uow: AsyncSession, **kwargs) -> CoachDtoSchema | None:
        statement = (
            update(Coach)
            .where(Coach.id == kwargs["id"])
            .values(**kwargs)
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        coach = result.fetchone()

        if coach is None:
            return None

        return CoachDtoSchema.from_orm(coach)

    async def delete_coach(self, uow: AsyncSession, pk: str) -> str | None:
        stmt = delete(Coach).where(Coach.id == pk)
        result = await uow.execute(stmt)
        await uow.commit()

        if result.rowcount == 0:
            return None

        return pk

    async def provide_by_username(self, uow: AsyncSession, username: str) -> CoachDtoSchema | None:
        query = select(Coach).where(Coach.username == username)
        result = await uow.execute(query)
        coach = result.scalars().first()

        if coach is None:
            return None

        return CoachDtoSchema.from_orm(coach)
