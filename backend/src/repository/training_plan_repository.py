from datetime import date
from uuid import UUID

from sqlalchemy import select, desc, literal_column
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from src import TrainingPlan, Training
from src.schemas.diet_dto import DietDtoSchema
from src.schemas.exercise_dto import ExerciseDtoSchema
from src.schemas.training_dto import TrainingDtoSchema
from src.schemas.training_plan_dto import TrainingPlanDtoShortSchema, TrainingPlanDtoSchema


class TrainingPlanRepository:
    async def create_training_plan(
        self,
        uow: AsyncSession,
        customer_id: str,
        start_date: date,
        end_date: date,
        set_rest: int,
        exercise_rest: int,
        notes: str,
    ) -> TrainingPlanDtoSchema | None:
        statement = (
            insert(TrainingPlan)
            .values(
                customer_id=customer_id,
                start_date=start_date,
                end_date=end_date,
                set_rest=set_rest,
                exercise_rest=exercise_rest,
                notes=notes
            )
            .on_conflict_do_nothing()
            .returning(literal_column("*"))
        )

        result = await uow.execute(statement)
        training_plan_id = result.scalar_one_or_none()

        if training_plan_id is None:
            return None

        training_plan = await self.provide_training_plan_by_id(uow, training_plan_id)
        return TrainingPlanDtoSchema.from_orm(training_plan)

    async def provide_training_plan_by_id(self, uow: AsyncSession, pk: UUID) -> TrainingPlanDtoSchema | None:
        query = (
            select(TrainingPlan)
            .where(TrainingPlan.id == pk)
            .options(
                selectinload(TrainingPlan.trainings).selectinload(Training.exercises),
                selectinload(TrainingPlan.diets),
            )
        )
        result = await uow.execute(query)
        training_plan = result.scalars().first()

        if training_plan is None:
            return None

        def map_exercise_to_dto(exercise):
            return ExerciseDtoSchema(id=exercise.id, name=exercise.name)

        def map_training_to_dto(training):
            exercises_dto = [map_exercise_to_dto(exercise) for exercise in training.exercises]
            return TrainingDtoSchema(id=training.id, name=training.name, exercises=exercises_dto)

        def map_diet_to_dto(diet):
            return DietDtoSchema(id=diet.id, proteins=diet.proteins, fats=diet.fats, carbs=diet.carbs)

        trainings_dto = [map_training_to_dto(training) for training in training_plan.trainings]
        diets_dto = [map_diet_to_dto(diet) for diet in training_plan.diets]

        training_plan_dto = TrainingPlanDtoSchema(
            id=training_plan.id,
            start_date=training_plan.start_date,
            end_date=training_plan.end_date,
            customer_id=training_plan.customer_id,
            diets=diets_dto,
            set_rest=training_plan.set_rest,
            exercise_rest=training_plan.exercise_rest,
            notes=training_plan.notes,
            trainings=trainings_dto,
        )

        return training_plan_dto

    async def provide_customer_plans_by_customer_id(
        self,
        uow: AsyncSession,
        customer_id: str
    ) -> list[TrainingPlanDtoShortSchema]:
        query = (
            select(
                TrainingPlan
            )
            .where(TrainingPlan.customer_id == UUID(customer_id))
            .options(
                selectinload(TrainingPlan.trainings),
                selectinload(TrainingPlan.diets),
            )
            .order_by(desc(TrainingPlan.end_date))
        )

        result = await uow.execute(query)
        training_plans = result.scalars().all()
        training_plans_dto = [
            TrainingPlanDtoShortSchema(
                id=str(training_plan.id),
                start_date=training_plan.start_date,
                end_date=training_plan.end_date,
                number_of_trainings=len(training_plan.trainings),
                diets=training_plan.diets,
            )
            for training_plan in training_plans
        ]

        return training_plans_dto
