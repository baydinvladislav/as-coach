"""
Library routing
"""

from fastapi import APIRouter, Depends, status

from src.service.authentication.coach import CoachService
from src.service.library import Library
from src.dependencies import provide_user_service, provide_library
from src.schemas.library import ExerciseCreateIn, ExerciseCreateOut

gym_router = APIRouter()


@gym_router.post(
    "/exercises",
    summary="Create new exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=ExerciseCreateOut)
async def create_exercise(
        exercise_data: ExerciseCreateIn,
        user_service: CoachService = Depends(provide_user_service),
        library: Library = Depends(provide_library)
) -> dict:
    """
    Creates new exercise for coach

    Args:
        exercise_data: data to create new exercise
        user_service: returns current application user
        library: service to organize data in gym library

    Returns:
        dictionary with just created exercise id, name, muscle_group's name as keys
    """
    user = user_service.user
    exercise = await library.create_exercise(
        exercise_name=exercise_data.name,
        coach_id=str(user.id),
        muscle_group_id=exercise_data.muscle_group_id
    )

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
        user_service: CoachService = Depends(provide_user_service),
        library: Library = Depends(provide_library)
) -> list:
    """
    Returns all exercises for coach

    Args:
        user_service: returns current application user
        library: service to organize data in gym library

    Returns:
        list of exercises
    """
    user = user_service.user
    exercises = await library.get_exercise_list(str(user.id))

    response = []
    for exercise in exercises:
        response.append({
            "id": str(exercise.id),
            "name": exercise.name,
            "muscle_group": exercise.muscle_group.name,
            "muscle_group_id": str(exercise.muscle_group.id)
        })

    return response


@gym_router.get(
    "/muscle_groups",
    summary="Returns all muscle groups",
    status_code=status.HTTP_200_OK)
async def get_muscle_groups(
        user_service: CoachService = Depends(provide_user_service),
        library: Library = Depends(provide_library)
) -> list:
    """
    Returns all muscle groups for coach

    Args:
        user_service: returns current application user
        library: service to organize data in gym library

    Returns:
        list of muscle groups
    """
    muscle_groups = await library.get_muscle_group_list()

    response = []
    for muscle_group in muscle_groups:
        response.append({
            "id": str(muscle_group.id),
            "name": muscle_group.name
        })

    return response
