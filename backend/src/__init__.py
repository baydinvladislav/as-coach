from .database import Base, engine
from .coach.models import Coach
from .customer.models import Customer, TrainingPlan
from .gym.models import (
    Diet, DietOnTrainingPlan, Training,
    Exercise, ExercisesOnTraining, MuscleGroup
)
