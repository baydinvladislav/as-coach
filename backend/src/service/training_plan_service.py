import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.exercise_dto import ScheduledExerciseDto
from src.service.training_service import TrainingService
from src.service.diet_service import DietService
from src.repository.training_plan_repository import TrainingPlanRepository
from src.schemas.training_plan_dto import (
    TrainingDtoSchema,
    TrainingPlanDtoSchema,
    TrainingPlanDtoShortSchema,
    TrainingPlanDetailDtoSchema,
)
from src.presentation.schemas.training_plan_schema import TrainingPlanIn

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrainingPlanCreationException(Exception):
    ...


class TrainingPlanService:
    def __init__(
        self,
        training_plan_repository: TrainingPlanRepository,
        training_service: TrainingService,
        diet_service: DietService
    ) -> None:
        self.training_plan_repository = training_plan_repository
        self.training_service = training_service
        self.diet_service = diet_service

    async def create_training_plan(
        self,
        uow: AsyncSession,
        customer_id: str,
        data: TrainingPlanIn
    ) -> TrainingPlanDtoSchema:
        try:
            training_plan = await self.training_plan_repository.create_training_plan(
                uow=uow,
                customer_id=customer_id,
                start_date=datetime.strptime(data.start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(data.end_date, "%Y-%m-%d").date(),
                set_rest=data.set_rest,
                exercise_rest=data.exercise_rest,
                notes=data.notes,
            )
            await self.diet_service.create_diets(
                uow=uow,
                training_plan_id=training_plan.id,
                diets=data.diets,
            )
            await self.training_service.create_trainings(
                uow=uow,
                training_plan_id=training_plan.id,
                trainings=data.trainings,
            )
        except Exception as exc:
            logger.warning("error.occurred.during.execution.training.plan.transaction", str(exc))
            await uow.rollback()
            raise TrainingPlanCreationException from exc
        else:
            await uow.commit()
            training_plan_in_db = await self.training_plan_repository.provide_training_plan_by_id(
                uow=uow, id_=training_plan.id,
            )
            return training_plan_in_db

    async def get_training_plan_by_id(self, uow: AsyncSession, id_: UUID) -> TrainingPlanDetailDtoSchema | None:
        training_plan = await self.training_plan_repository.provide_training_plan_by_id(uow, id_=id_)

        training_ids = [str(training.id) for training in training_plan.trainings]
        exercise_ids = [str(exercise.id) for training in training_plan.trainings for exercise in training.exercises]

        scheduled_trainings = await self.training_service.provide_scheduled_trainings(
            uow=uow,
            training_ids=training_ids,
            exercise_ids=exercise_ids,
        )

        if training_plan is None:
            logger.info(f"training.plan.not.found: id={id_}")
            return None

        trainings = []
        for training in training_plan.trainings:
            training_dto = TrainingDtoSchema(
                id=str(training.id),
                name=training.name,
                number_of_exercises=len(training_plan.trainings),
                exercises=[],
            )

            for exercise in training.exercises:
                scheduled_exercise = scheduled_trainings[str(exercise.id)]
                superset_id = str(scheduled_exercise.superset_id) if scheduled_exercise.superset_id else None

                exercise_dto = ScheduledExerciseDto(
                    id=str(exercise.id),
                    name=exercise.name,
                    sets=scheduled_exercise.sets,
                    exercise_id=exercise.id,
                    training_id=training.id,
                    superset_id=superset_id,
                    ordering=scheduled_exercise.ordering,
                )

                training_dto.exercises.append(exercise_dto)

            trainings.append(training_dto)

        training_plan_dto = TrainingPlanDetailDtoSchema(
            id=str(training_plan.id),
            start_date=training_plan.start_date.strftime("%Y-%m-%d"),
            end_date=training_plan.end_date.strftime("%Y-%m-%d"),
            proteins="/".join([str(diet.proteins) for diet in training_plan.diets]),
            fats="/".join([str(diet.fats) for diet in training_plan.diets]),
            carbs="/".join([str(diet.carbs) for diet in training_plan.diets]),
            calories="/".join([str(diet.calories) for diet in training_plan.diets]),
            trainings=trainings,
            set_rest=training_plan.set_rest,
            exercise_rest=training_plan.exercise_rest,
            notes=training_plan.notes,
        )

        return training_plan_dto

    async def get_customer_training_plans(
        self, uow: AsyncSession, customer_id: str
    ) -> list[TrainingPlanDtoShortSchema]:
        training_plans = await self.training_plan_repository.provide_customer_plans_by_customer_id(
            uow=uow, customer_id=customer_id,
        )
        return training_plans
