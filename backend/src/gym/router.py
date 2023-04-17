"""
Gym routing
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.auth.dependencies import get_current_user
from src.gym.models import Exercise
from src.gym.schemas import ExerciseCreateIn, ExerciseCreateOut

gym_router = APIRouter()


@gym_router.post(
    "/exercises",
    summary="Create new exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=ExerciseCreateOut)
async def create_exercise(
        exercise_data: ExerciseCreateIn,
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> dict:
    """
    Creates new exercise for user

    Args:
        exercise_data: data to create new exercise
        database: dependency injection for access to database
        current_user: returns current application user

    Returns:
        dictionary with just created exercise id, name, user_id as keys
    """
    exercise = Exercise(
        name=exercise_data.name,
        muscle_group_id=exercise_data.muscle_group_id,
        user_id=str(current_user.id)
    )

    database.add(exercise)
    database.commit()

    return {
        "id": str(exercise.id),
        "muscle_group": exercise.muscle_group.name,
        "name": exercise.name
    }


@gym_router.get(
    "/exercises",
    summary="Returns all exercises",
    status_code=status.HTTP_200_OK)
async def get_exercises(
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_user)) -> list:
    """
    Returns all exercises for user

    Args:
        database: dependency injection for access to database
        current_user: returns current application user

    Returns:
        list of exercises
    """
    exercises = database.query(Exercise).filter(
        or_(Exercise.user_id.is_(None), Exercise.user_id == str(current_user.id))
    ).all()

    response = []
    for exercise in exercises:
        response.append({
            "id": str(exercise.id),
            "muscle_group": exercise.muscle_group.name,
            "name": exercise.name
        })

    return response
