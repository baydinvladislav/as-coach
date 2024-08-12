from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.coach_service import CoachService
from src.service.library_service import LibraryService
from src.shared.dependencies import provide_user_service, provide_library_service, provide_database_unit_of_work
from src.presentation.schemas.training_plan_schema import ExerciseCreateIn, ExerciseCreateOut, ExerciseForCoachOut

gym_router = APIRouter()


@gym_router.post(
    "/exercises",
    summary="Create new exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=ExerciseCreateOut)
async def create_exercise(
    exercise_data: ExerciseCreateIn,
    user_service: CoachService = Depends(provide_user_service),
    library_service: LibraryService = Depends(provide_library_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> ExerciseCreateOut:
    """
    Creates new exercise for coach

    Args:
        exercise_data: data to create new exercise
        user_service: returns current application user
        library_service: service to organize data in gym library
        uow: database unit of work

    Returns:
        dictionary with just created exercise id, name, muscle_group's name as keys
    """
    user = user_service.user
    exercise = await library_service.create_exercise(
        uow=uow,
        exercise_name=exercise_data.name,
        coach_id=user.id,
        muscle_group_id=exercise_data.muscle_group_id
    )
    return ExerciseCreateOut(
        id=str(exercise.id), muscle_group=exercise.muscle_group_name, name=exercise.name,
    )


@gym_router.get(
    "/exercises",
    summary="Returns all exercises",
    status_code=status.HTTP_200_OK)
async def get_exercises(
    user_service: CoachService = Depends(provide_user_service),
    library_service: LibraryService = Depends(provide_library_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> list:
    """
    Returns all exercises for coach

    Args:
        user_service: returns current application user
        library_service: service to organize data in gym library
        uow: database unit of work

    Returns:
        list of exercises
    """
    user = user_service.user
    exercises = await library_service.get_exercise_list(uow, str(user.id))

    response = [
        ExerciseForCoachOut(
            id=str(exercise.id),
            name=exercise.name,
            muscle_group=exercise.muscle_group_name,
            muscle_group_id=str(exercise.muscle_group_id),
        )
        for exercise in exercises
    ]
    return response


@gym_router.get(
    "/muscle_groups",
    summary="Returns all muscle groups",
    status_code=status.HTTP_200_OK)
async def get_muscle_groups(
    user_service: CoachService = Depends(provide_user_service),
    library_service: LibraryService = Depends(provide_library_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> list:
    """
    Returns all muscle groups for coach

    Args:
        user_service: returns current application user
        library_service: service to organize data in gym library
        uow: database unit of work

    Returns:
        list of muscle groups
    """
    muscle_groups = await library_service.get_muscle_group_list(uow)

    response = []
    for muscle_group in muscle_groups:
        response.append({
            "id": str(muscle_group.id),
            "name": muscle_group.name
        })

    return response
