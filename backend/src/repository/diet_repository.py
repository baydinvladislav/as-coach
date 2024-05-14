from src import Diet, DietOnTrainingPlan
from src.repository.base_repository import BaseRepository


class DietRepository(BaseRepository):
    model = Diet


class DietOnTrainingPlanRepository(BaseRepository):
    model = DietOnTrainingPlan
