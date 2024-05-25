from src.service.coach_service import CoachService
from src.shared.container import init_combat_container

container = init_combat_container()


async def provide_coach_service() -> CoachService:
    return container.coach_service
