import os
import uuid
from datetime import date, timedelta
import pytest_asyncio

from httpx import AsyncClient, Response
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src import (
    engine,
    Coach,
    Customer,
    TrainingPlan,
    Training,
    MuscleGroup,
    Exercise,
    ExercisesOnTraining
)
from src.utils import get_hashed_password, generate_random_password, create_access_token
from src.dependencies import get_db
from src.main import app

TEST_COACH_FIRST_NAME = os.getenv("TEST_COACH_FIRST_NAME")
TEST_COACH_LAST_NAME = os.getenv("TEST_COACH_LAST_NAME")
TEST_COACH_USERNAME = os.getenv("TEST_COACH_USERNAME")
TEST_COACH_PASSWORD = os.getenv("TEST_COACH_PASSWORD")

TEST_CUSTOMER_FIRST_NAME = os.getenv("TEST_CUSTOMER_FIRST_NAME")
TEST_CUSTOMER_LAST_NAME = os.getenv("TEST_CUSTOMER_LAST_NAME")
TEST_CUSTOMER_USERNAME = os.getenv("TEST_CUSTOMER_USERNAME")

TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def make_test_http_request(
        url: str,
        method: str,
        username: str | None = None,
        data: dict | None = None,
        json: dict | None = None,
) -> Response:
    """
    Make tests http request to server,
    has username if test case requires authed user.

    Args:
        url: testing endpoint
        method: http request method
        username: authed user who makes http request
        data: data sent to server
        json: data to signup
    """
    headers = {"content-type": "application/x-www-form-urlencoded"}
    if username:
        auth_token = await create_access_token(username)
        headers["Authorization"] = f"Bearer {auth_token}"

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        match method:
            case "get":
                response = await ac.get(url, headers=headers)
            case "post":
                if data:
                    response = await ac.post(url, headers=headers, data=data)
                else:
                    response = await ac.post(url, headers=headers, json=json)
            case _:
                raise ValueError("Unexpected method")

        return response


@pytest_asyncio.fixture()
async def create_training_exercises(
        create_trainings,
        create_exercises,
        override_get_db
):
    query = select(ExercisesOnTraining)

    training_exercises = await override_get_db.execute(query)
    training_exercises_in_db = training_exercises.scalars().all()
    if training_exercises_in_db:
        return training_exercises_in_db

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

    override_get_db.add_all(training_exercises)
    await override_get_db.commit()

    training_exercises = await override_get_db.execute(query)
    training_exercises_in_db = training_exercises.scalars().all()
    return training_exercises_in_db


@pytest_asyncio.fixture()
async def create_trainings(create_training_plans, override_get_db):
    query = select(Training)

    trainings = await override_get_db.execute(query)
    trainings_in_db = trainings.scalars().all()
    if trainings_in_db:
        return trainings_in_db

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

    override_get_db.add_all(trainings)
    await override_get_db.commit()

    trainings = await override_get_db.execute(query)
    trainings_in_db = trainings.scalars().all()
    return trainings_in_db


@pytest_asyncio.fixture()
async def create_training_plans(create_user, create_customer, override_get_db):
    query = select(TrainingPlan)

    training_plans = await override_get_db.execute(query)
    training_plans_in_db = training_plans.scalars().all()
    if training_plans_in_db:
        return training_plans_in_db

    training_plans = [
        TrainingPlan(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=6),
            customer_id=str(create_customer.id)
        ),
        TrainingPlan(
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=14),
            customer_id=str(create_customer.id)
        )
    ]

    override_get_db.add_all(training_plans)
    await override_get_db.commit()

    training_plans = await override_get_db.execute(query)
    training_plans_in_db = training_plans.scalars().all()
    return training_plans_in_db


@pytest_asyncio.fixture()
async def create_muscle_groups(override_get_db):
    query = select(MuscleGroup)

    muscle_groups = await override_get_db.execute(query)
    muscle_groups_in_db = muscle_groups.scalars().all()
    if muscle_groups_in_db:
        return muscle_groups_in_db

    muscle_groups = (
        MuscleGroup(name="Грудь"),
        MuscleGroup(name="Бицепс"),

        MuscleGroup(name="Спина"),
        MuscleGroup(name="Трицепс"),

        MuscleGroup(name="Ноги")
    )

    override_get_db.add_all(muscle_groups)
    await override_get_db.commit()

    muscle_groups = await override_get_db.execute(query)
    muscle_groups_in_db = muscle_groups.scalars().all()
    return muscle_groups_in_db


@pytest_asyncio.fixture()
async def create_exercises(create_muscle_groups, override_get_db):
    query = select(Exercise)

    exercises = await override_get_db.execute(query)
    exercises_in_db = exercises.scalars().all()
    if exercises_in_db:
        return exercises_in_db

    chest = await override_get_db.execute(select(MuscleGroup).where(MuscleGroup.name == "Грудь"))
    chest = chest.scalar()

    biceps = await override_get_db.execute(select(MuscleGroup).where(MuscleGroup.name == "Бицепс"))
    biceps = biceps.scalar()

    back = await override_get_db.execute(select(MuscleGroup).where(MuscleGroup.name == "Спина"))
    back = back.scalar()

    triceps = await override_get_db.execute(select(MuscleGroup).where(MuscleGroup.name == "Трицепс"))
    triceps = triceps.scalar()

    legs = await override_get_db.execute(select(MuscleGroup).where(MuscleGroup.name == "Ноги"))
    legs = legs.scalar()

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

    override_get_db.add_all(exercises)
    await override_get_db.commit()

    exercises = await override_get_db.execute(query)
    exercises_in_db = exercises.scalars().all()
    return exercises_in_db


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
            coach=create_user
        )

        override_get_db.add(test_customer)
        await override_get_db.commit()

        result = await override_get_db.execute(
            select(Customer).where(Customer.id == str(test_customer.id)).options(
                selectinload(Customer.coach)
            )
        )
        return result.scalar()
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
            password=await get_hashed_password(TEST_COACH_PASSWORD),
            fcm_token="test token value",
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
