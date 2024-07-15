from uuid import UUID

from sqlalchemy import select, or_, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from src import Exercise, MuscleGroup
from src.schemas.muscle_group_dto import MuscleGroupDto
from src.schemas.exercise_dto import ExerciseDtoSchema


class ExerciseRepository:
    async def get_exercise_by_id(self, uow: AsyncSession, exercise_id: UUID) -> ExerciseDtoSchema | None:
        query = (
            select(Exercise)
            .join(Exercise.muscle_group)
            .where(Exercise.id == exercise_id)
        )

        result = await uow.execute(query)
        exercise = result.scalar_one_or_none()

        if exercise is None:
            return None

        exercise_dto = ExerciseDtoSchema(
            id=exercise.id,
            name=exercise.name,
            coach_id=exercise.coach_id,
            muscle_group_id=exercise.muscle_group_id,
            muscle_group_name=exercise.muscle_group.name,
        )

        return exercise_dto

    async def create_exercise(
        self, uow: AsyncSession, name: str, coach_id: UUID, muscle_group_id: UUID
    ) -> ExerciseDtoSchema | None:
        statement = (
            insert(Exercise)
            .values(
                name=name,
                coach_id=coach_id,
                muscle_group_id=muscle_group_id,
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        exercise_id = result.scalar_one_or_none()

        if exercise_id is None:
            return None

        exercise = await self.get_exercise_by_id(uow, exercise_id)
        return exercise

    async def get_coach_exercises(self, uow: AsyncSession, coach_id: str) -> list[ExerciseDtoSchema]:
        query = (
            select(
                Exercise.id,
                Exercise.name,
                Exercise.coach_id,
                MuscleGroup.name.label('muscle_group_name'),
            )
            .join(MuscleGroup, Exercise.muscle_group_id == MuscleGroup.id)
            .where(
                or_(
                    Exercise.coach_id.is_(None),
                    Exercise.coach_id == UUID(coach_id),
                )
            )
        )
        result = await uow.execute(query)
        exercises = result.fetchall()
        return [ExerciseDtoSchema.from_orm(exercise) for exercise in exercises]


class MuscleGroupRepository:
    async def get_specified_muscle_group(self, uow: AsyncSession, muscle_group_id: str) -> MuscleGroupDto | None:
        query = (
            select(MuscleGroup).where(MuscleGroup.id == UUID(muscle_group_id))
        )
        result = await uow.execute(query)
        muscle_group = result.scalar_one_or_none()

        if muscle_group is None:
            return None

        return MuscleGroupDto.from_orm(muscle_group)

    async def get_all_muscle_groups(self, uow: AsyncSession) -> list[MuscleGroupDto]:
        query = select(MuscleGroup.id, MuscleGroup.name)
        result = await uow.execute(query)
        muscle_groups = result.fetchall()
        return [MuscleGroupDto.from_orm(muscle_group) for muscle_group in muscle_groups]
