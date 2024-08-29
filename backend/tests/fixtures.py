import os
import uuid
from datetime import date, timedelta

import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine

from src.main import app
from src.shared.dependencies import provide_database_unit_of_work
from src import (
    ExercisesOnTraining,
    Training,
    TrainingPlan,
    MuscleGroup,
    Exercise,
    Coach,
    Customer,
    Diet,
    DietDays,
)
from src.utils import generate_random_password, get_hashed_password
from tests.conftest import TestingSessionLocal
from src.shared.config import (
    TEST_COACH_FIRST_NAME,
    TEST_COACH_LAST_NAME,
    TEST_COACH_USERNAME,
    TEST_COACH_PASSWORD,
    TEST_CUSTOMER_FIRST_NAME,
    TEST_CUSTOMER_LAST_NAME,
    TEST_CUSTOMER_USERNAME,
    OTP_LENGTH,
)


@pytest_asyncio.fixture()
async def create_training_exercises(create_trainings, create_exercises, db):
    superset_id = uuid.uuid4()
    training_exercises = []

    for training in create_trainings:
        ordering = 0
        for exercise in create_exercises:
            if exercise.muscle_group.name == training.name:
                training_exercise = ExercisesOnTraining(
                    training_id=str(training.id),
                    exercise_id=str(exercise.id),
                    sets=[10, 10, 10],
                    superset_id=superset_id if training.name == "Грудь" else None,
                    ordering=ordering,
                )
                training_exercises.append(training_exercise)
                ordering += 1

    db.add_all(training_exercises)
    await db.commit()

    result = await db.execute(select(ExercisesOnTraining))
    training_exercises = result.scalars().all()
    return training_exercises


@pytest_asyncio.fixture()
async def create_diets(create_training_plans, db):
    diets_list = [
        Diet(
            total_proteins=200,
            total_fats=100,
            total_carbs=300,
            total_calories=2900,
            training_plan_id=create_training_plans[0].id,
        ),
        Diet(
            total_proteins=200,
            total_fats=100,
            total_carbs=200,
            total_calories=2500,
            training_plan_id=create_training_plans[1].id,
        ),
    ]

    db.add_all(diets_list)

    diet_days_list = [
        DietDays(
            date=create_training_plans[0].start_date + timedelta(days=2),
            diet=diets_list[0],
            breakfast={
                "total_calories": 774,
                "total_proteins": 25.72,
                "total_fats": 25.24,
                "total_carbs": 109.34,
                "products": [
                    {
                        "id": "b2c8d440-d59d-44d1-8b27-70fc08b6b831",
                        "name": "Изюм Светлый",
                        "barcode": "123456788",
                        "vendor_name": "Пятёрочка",
                        "product_type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 40,
                        "calories": 116,
                        "proteins": 1,
                        "fats": 0.2,
                        "carbs": 28,
                    },
                    {
                        "id": "90cbaa5b-b322-4a4b-a5ec-17cd39b9a13a",
                        "name": "Геркулес",
                        "barcode": "123456789",
                        "vendor_name": "Увелка",
                        "product_type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 100,
                        "calories": 370,
                        "proteins": 12,
                        "fats": 6,
                        "carbs": 64,
                    },
                    {
                        "id": "ae1df566-1a9a-4bc8-9fd5-bd47cee7a983",
                        "name": "Молоко 2.5%",
                        "barcode": "123456790",
                        "vendor_name": "Простаквашино",
                        "product_type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 300,
                        "calories": 159,
                        "proteins": 9,
                        "fats": 9,
                        "carbs": 14.1,
                    },
                    {
                        "id": "1ff18cad-faca-432e-a44d-5515abb11be1",
                        "name": "Миндаль",
                        "barcode": "123456791",
                        "vendor_name": "Перекрёсток",
                        "product_type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 20,
                        "calories": 129,
                        "proteins": 3.72,
                        "fats": 11.54,
                        "carbs": 3.24,
                    },
                ],
            },
            lunch={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "919b5f1e-36e0-4e15-a39a-a88481cdc938",
                        "amount": 100,
                    },
                ],
            },
            dinner={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "098af4ff-64fa-4ffb-8ced-6d8696b3ecb9",
                        "amount": 300,
                    },
                ],
            },
            snacks={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "24ef3147-1ec8-4e82-9020-3241c35b22b0",
                        "amount": 200,
                    },
                ],
            },
        ),
        DietDays(
            date=create_training_plans[0].start_date + timedelta(days=4),
            diet=diets_list[0],
            breakfast={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "b2c8d440-d59d-44d1-8b27-70fc08b6b831",
                        "amount": 200,
                    },
                ],
            },
            lunch={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "919b5f1e-36e0-4e15-a39a-a88481cdc938",
                        "amount": 100,
                    },
                ],
            },
            dinner={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "098af4ff-64fa-4ffb-8ced-6d8696b3ecb9",
                        "amount": 300,
                    },
                ],
            },
            snacks={
                "total_calories": 300,
                "total_proteins": 50,
                "total_fats": 30,
                "total_carbs": 80,
                "products": [
                    {
                        "product_id": "24ef3147-1ec8-4e82-9020-3241c35b22b0",
                        "amount": 200,
                    },
                ],
            },
        )
    ]

    db.add_all(diet_days_list)

    await db.commit()

    result = await db.execute(select(Diet))
    diets = result.scalars().all()
    return diets


@pytest_asyncio.fixture()
async def create_trainings(create_training_plans, db):
    training_plan = create_training_plans[0]

    training_names = ["Грудь", "Бицепс", "Спина", "Трицепс", "Ноги"]
    trainings_list = [Training(name=name, training_plan_id=str(training_plan.id)) for name in training_names]

    db.add_all(trainings_list)
    await db.commit()

    result = await db.execute(select(Training))
    trainings = result.scalars().all()
    return trainings


@pytest_asyncio.fixture()
async def create_training_plans(create_coach, create_customer, db):
    training_plans_list = [
        TrainingPlan(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=6),
            customer=create_customer,
        ),
        TrainingPlan(
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=14),
            customer=create_customer,
        )
    ]

    db.add_all(training_plans_list)
    await db.commit()

    result = await db.execute(
        select(
            TrainingPlan
        ).options(
            selectinload(TrainingPlan.customer),
        )
    )
    training_plans = result.scalars().all()
    return training_plans


@pytest_asyncio.fixture()
async def create_muscle_groups(db):
    muscle_group_names = ["Грудь", "Бицепс", "Спина", "Трицепс", "Ноги",]
    muscle_groups = [MuscleGroup(name=name) for name in muscle_group_names]
    db.add_all(muscle_groups)
    await db.commit()

    result = await db.execute(select(MuscleGroup))
    muscle_groups = result.scalars().all()
    return muscle_groups


@pytest_asyncio.fixture()
async def create_exercises(create_muscle_groups, db):

    async def add_exercises_for_muscle_group(muscle_group_name, exercise_names):
        muscle_group = await db.execute(select(MuscleGroup).where(MuscleGroup.name == muscle_group_name))
        muscle_group = muscle_group.scalar()
        return [Exercise(name=exercise_name, muscle_group_id=muscle_group.id) for exercise_name in exercise_names]

    exercises_by_muscle_group = {
        "Грудь": ['Жим штанги лежа', 'Разводка с гантелями', 'Сведения в кроссовере'],
        "Бицепс": ['Подъем штанги на бицепс', 'Сгибания Молот', 'Сгибания на скамье Скотта'],
        "Спина": ['Подтягивания', 'Тяга штанги в наклоне', 'Пулловер с верхнего блока'],
        "Трицепс": ['Жим штанги узким хватом', 'Разгибания с верхнего блока', 'Французский жим'],
        "Ноги": [
            'Приседания со штангой', 'Жим платформы ногами', 'Сгибания ногами сидя',
            'Разгибания ногами лежа', 'Становая тяга на прямых ногах'
        ],
    }

    exercises = []
    for muscle_group, names in exercises_by_muscle_group.items():
        exercises.extend(await add_exercises_for_muscle_group(muscle_group, names))

    db.add_all(exercises)
    await db.commit()

    query = select(Exercise).options(selectinload(Exercise.muscle_group))
    result = await db.execute(query)
    exercises = result.scalars().all()
    return exercises


@pytest_asyncio.fixture()
async def create_customer(create_coach, db) -> Customer:
    test_customer = Customer(
        username=TEST_CUSTOMER_USERNAME,
        first_name=TEST_CUSTOMER_FIRST_NAME,
        last_name=TEST_CUSTOMER_LAST_NAME,
        password=generate_random_password(OTP_LENGTH),
        coach=create_coach
    )

    db.add(test_customer)
    await db.commit()

    query = select(
        Customer
    ).where(
        Customer.id == str(test_customer.id)
    ).options(
        selectinload(Customer.coach),
        selectinload(Customer.training_plans),
    )

    result = await db.execute(query)
    return result.scalar()


@pytest_asyncio.fixture()
async def create_coach(db) -> Coach:
    test_coach = Coach(
        username=TEST_COACH_USERNAME,
        first_name=TEST_COACH_FIRST_NAME,
        last_name=TEST_COACH_LAST_NAME,
        password=await get_hashed_password(TEST_COACH_PASSWORD),
        fcm_token="test token value",
    )
    db.add(test_coach)
    await db.commit()
    return test_coach


@pytest_asyncio.fixture()
async def db_engine():
    engine = create_async_engine(os.environ.get("TEST_DATABASE_URL"))
    yield engine


@pytest_asyncio.fixture(scope="function")
async def db(db_engine):
    connection = await db_engine.connect()
    await connection.begin()

    db = TestingSessionLocal(bind=connection)
    app.dependency_overrides[provide_database_unit_of_work] = lambda: db

    yield db

    await db.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(db):
    app.dependency_overrides[provide_database_unit_of_work] = lambda: db
