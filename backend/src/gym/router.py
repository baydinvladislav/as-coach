"""

"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.auth.dependencies import get_current_user
from src.gym.schemas import TrainingPlanIn, TrainingPlanOut

gym_router = APIRouter()


@gym_router.post(
    "/training_plans",
    summary="Create new training plan for customer",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingPlanOut)
async def create_training_plan(
        training_plan_data: TrainingPlanIn,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> dict:
    pass
