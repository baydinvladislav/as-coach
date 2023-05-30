from .database import Base, engine
from .auth.models import Coach
from .customer.models import Customer, TrainingPlan
from .gym.models import (
    Diet, DietOnTrainingPlan, Training,
    Exercise, ExercisesOnTraining, MuscleGroup
)
