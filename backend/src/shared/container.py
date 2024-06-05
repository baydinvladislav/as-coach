from dataclasses import dataclass

from src.repository.coach_repository import CoachRepository
from src.repository.customer_repository import CustomerRepository
from src.repository.diet_repository import DietRepository, DietOnTrainingPlanRepository
from src.repository.library_repository import MuscleGroupRepository, ExerciseRepository
from src.repository.training_repository import TrainingRepository, ExercisesOnTrainingRepository
from src.service.coach_service import CoachService, CoachSelectorService, CoachProfileService
from src.service.customer_service import CustomerService, CustomerSelectorService, CustomerProfileService
from src.service.diet_service import DietService
from src.service.library_service import LibraryService
from src.service.notification_service import NotificationService
from src.service.training_plan_service import TrainingPlanService
from src.service.training_service import TrainingService
from src.service.user_service import UserService
from src.shared.settings import AppSettings


@dataclass
class Container:
    coach_service: CoachService
    customer_service: CustomerService
    library_service: LibraryService
    training_plan_service: TrainingPlanService
    user_service: UserService


def init_combat_container() -> Container:
    app_settings = AppSettings()

    notification_service = NotificationService()

    coach_repository = CoachRepository()
    coach_service = CoachService(
        selector_service=CoachSelectorService(coach_repository),
        profile_service=CoachProfileService(coach_repository),
    )

    customer_repository = CustomerRepository()
    customer_service = CustomerService(
        selector_service=CustomerSelectorService(customer_repository),
        profile_service=CustomerProfileService(customer_repository),
        notification_service=notification_service,
    )

    diet_service = DietService({
        "diet_repo": DietRepository(),
        "diets_on_training_repo": DietOnTrainingPlanRepository(),
    })

    library_service = LibraryService({
        "exercise": ExerciseRepository(),
        "muscle_group": MuscleGroupRepository(),
    })

    # training_service = TrainingService({
    #     "training_repo": TrainingRepository(),
    #     "exercises_on_training_repo": ExercisesOnTrainingRepository()
    # })

    training_service = TrainingService(
        training_repository=TrainingRepository(),
        exercises_on_training_repository=ExercisesOnTrainingRepository(),
    )

    training_plan_service = TrainingPlanService(
        training_service=training_service,
        diet_service=diet_service,
    )

    return Container(
        coach_service=coach_service,
        customer_service=customer_service,
        library_service=library_service,
        training_plan_service=training_plan_service,
    )
