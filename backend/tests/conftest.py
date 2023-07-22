import os
import uuid
from datetime import date, timedelta
import pytest
import pytest_asyncio

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src import engine
from src.customer.models import Customer, TrainingPlan
from src.auth.utils import get_hashed_password
from src.dependencies import get_db
from src.main import app
from src.coach.models import Coach
from src.gym.models import Exercise, MuscleGroup, Training, ExercisesOnTraining
from src.customer.utils import generate_random_password


TEST_COACH_FIRST_NAME = os.getenv("TEST_COACH_FIRST_NAME")
TEST_COACH_LAST_NAME = os.getenv("TEST_COACH_LAST_NAME")
TEST_COACH_USERNAME = os.getenv("TEST_COACH_USERNAME")
TEST_COACH_PASSWORD = os.getenv("TEST_COACH_PASSWORD")

TEST_CUSTOMER_FIRST_NAME = os.getenv("TEST_CUSTOMER_FIRST_NAME")
TEST_CUSTOMER_LAST_NAME = os.getenv("TEST_CUSTOMER_LAST_NAME")
TEST_CUSTOMER_USERNAME = os.getenv("TEST_CUSTOMER_USERNAME")

TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture()
def create_training_exercises(
        create_trainings,
        create_exercises,
        override_get_db
):
    training_exercises = override_get_db.query(ExercisesOnTraining).all()
    if training_exercises:
        return training_exercises

    training_exercises = []
    superset_id = uuid.uuid4()
    for training in create_trainings:
        available_exercises = [
            exercise for exercise in create_exercises
            if exercise.muscle_group.name == training.name
        ]
        for exercise in available_exercises:
            training_exercises.append(
                ExercisesOnTraining(
                    training_id=str(training.id),
                    exercise_id=str(exercise.id),
                    sets=[10, 10, 10],
                    # make chest's exercises in superset manner
                    superset_id=superset_id if training.name == "Грудь" else None
                )
            )

    override_get_db.bulk_save_objects(training_exercises)
    override_get_db.commit()

    return override_get_db.query(ExercisesOnTraining).all()


@pytest.fixture()
def create_trainings(create_training_plans, override_get_db):
    trainings = override_get_db.query(Training).all()
    if trainings:
        return trainings

    training_plan = create_training_plans[0]

    trainings = (
        Training(
            name="Грудь",
            training_plan_id=str(training_plan.id)
        ),
        Training(
            name="Бицепс",
            training_plan_id=str(training_plan.id)
        ),
        Training(
            name="Спина",
            training_plan_id=str(training_plan.id)
        ),
        Training(
            name="Трицепс",
            training_plan_id=str(training_plan.id)
        ),
        Training(
            name="Ноги",
            training_plan_id=str(training_plan.id)
        )
    )

    override_get_db.bulk_save_objects(trainings)
    override_get_db.commit()

    return override_get_db.query(Training).all()


@pytest.fixture()
def create_training_plans(create_user, create_customer, override_get_db):
    training_plans = override_get_db.query(TrainingPlan).all()
    if training_plans:
        return training_plans

    training_plans = [
        TrainingPlan(
            start_date=date.today().strftime('%Y-%m-%d'),
            end_date=(date.today() + timedelta(days=6)).strftime('%Y-%m-%d'),
            customer_id=str(create_customer.id)
        ),
        TrainingPlan(
            start_date=(date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            end_date=(date.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
            customer_id=str(create_customer.id)
        )
    ]

    override_get_db.bulk_save_objects(training_plans)
    override_get_db.commit()

    return override_get_db.query(TrainingPlan).all()


@pytest_asyncio.fixture()
async def create_muscle_groups(override_get_db):
    muscle_groups = await override_get_db.execute(select(MuscleGroup))
    if muscle_groups:
        return muscle_groups

    muscle_groups = (
        MuscleGroup(name="Грудь"),
        MuscleGroup(name="Бицепс"),

        MuscleGroup(name="Спина"),
        MuscleGroup(name="Трицепс"),

        MuscleGroup(name="Ноги")
    )

    override_get_db.bulk_save_objects(muscle_groups)
    override_get_db.commit()

    return override_get_db.query(MuscleGroup).all()


@pytest_asyncio.fixture()
async def create_exercises(create_muscle_groups, override_get_db):
    exercises = await override_get_db.execute(select(Exercise))

    if exercises:
        return exercises

    chest = override_get_db.query(MuscleGroup).filter(MuscleGroup.name == "Грудь").first()
    biceps = override_get_db.query(MuscleGroup).filter(MuscleGroup.name == "Бицепс").first()
    back = override_get_db.query(MuscleGroup).filter(MuscleGroup.name == "Спина").first()
    triceps = override_get_db.query(MuscleGroup).filter(MuscleGroup.name == "Трицепс").first()
    legs = override_get_db.query(MuscleGroup).filter(MuscleGroup.name == "Ноги").first()

    exercises = (
        Exercise(
            name='Жим штанги лежа',
            muscle_group_id=str(chest.id)
        ),
        Exercise(
            name='Разводка с гантелями',
            muscle_group_id=str(chest.id)
        ),
        Exercise(
            name='Сведения в кроссовере',
            muscle_group_id=str(chest.id)
        ),

        Exercise(
            name='Подъем штанги на бицепс',
            muscle_group_id=str(biceps.id)
        ),
        Exercise(
            name='Сгибания Молот',
            muscle_group_id=str(biceps.id)
        ),
        Exercise(
            name='Сгибания на скамье Скотта',
            muscle_group_id=str(biceps.id)
        ),

        Exercise(
            name='Подтягивания',
            muscle_group_id=str(back.id)
        ),
        Exercise(
            name='Тяга штанги в наклоне',
            muscle_group_id=str(back.id)
        ),
        Exercise(
            name='Пулловер с верхнего блока',
            muscle_group_id=str(back.id)
        ),

        Exercise(
            name='Жим штанги узким хватом',
            muscle_group_id=str(triceps.id)
        ),
        Exercise(
            name='Разгибания с верхнего блока',
            muscle_group_id=str(triceps.id)
        ),
        Exercise(
            name='Французский жим',
            muscle_group_id=str(triceps.id)
        ),

        Exercise(
            name='Приседания со штангой',
            muscle_group_id=str(legs.id)
        ),
        Exercise(
            name='Жим платформы ногами',
            muscle_group_id=str(legs.id)
        ),
        Exercise(
            name='Сгибания ногами сидя',
            muscle_group_id=str(legs.id)
        ),
        Exercise(
            name='Разгибания ногами лежа',
            muscle_group_id=str(legs.id),
        ),
        Exercise(
            name='Становая тяга на прямых ногах',
            muscle_group_id=str(legs.id)
        )
    )

    override_get_db.bulk_save_objects(exercises)
    override_get_db.commit()

    return override_get_db.query(Exercise).all()


@pytest_asyncio.fixture()
async def create_customer(create_user, override_get_db):
    """
    Creates test customer
    """

    test_user = await override_get_db.execute(
        select(Coach).order_by(Coach.username).options(selectinload(Coach.customers))
    )

    test_user = test_user.scalars().first()
    if test_user and not test_user.customers:
        test_customer = Customer(
            username=TEST_CUSTOMER_USERNAME,
            first_name=TEST_CUSTOMER_FIRST_NAME,
            last_name=TEST_CUSTOMER_LAST_NAME,
            password=generate_random_password(8),
            coach_id=str(create_user.id)
        )

        override_get_db.add(test_customer)
        await override_get_db.commit()
        return test_customer
    else:
        return test_user.customers[0]


@pytest_asyncio.fixture()
async def create_user(override_get_db):
    """
    Creates test user
    """
    test_user = await override_get_db.execute(
        select(Coach).where(Coach.username == TEST_COACH_USERNAME)
    )

    test_user = test_user.scalar()

    if test_user is None:
        test_user = Coach(
            username=TEST_COACH_USERNAME,
            first_name=TEST_COACH_FIRST_NAME,
            last_name=TEST_COACH_LAST_NAME,
            password=get_hashed_password(TEST_COACH_PASSWORD)
        )

        override_get_db.add(test_user)
        await override_get_db.commit()

    yield test_user


@pytest_asyncio.fixture()
async def override_get_db():
    """
    Creates session to testing db
    """
    async with TestingSessionLocal() as db:
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            await db.close()


@app.on_event("startup")
async def startup_event():
    """
    In the beginning on each test creates database schema,
    also changes production db to testing db
    """
    from src import Base, engine

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
