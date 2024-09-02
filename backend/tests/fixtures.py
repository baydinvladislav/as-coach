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
                        "portion_size": None,
                        "type": "gram",
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
                        "portion_size": None,
                        "type": "gram",
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
                        "portion_size": None,
                        "vendor_name": "Простаквашино",
                        "type": "gram",
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
                        "portion_size": None,
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
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
                "total_calories": 1374,
                "total_proteins": 104,
                "total_fats": 1,
                "total_carbs": 190,
                "products": [
                    {
                        "id": "0fa67bf1-2c2f-4901-9327-a28abcf3beea",
                        "name": "Филе Голени",
                        "portion_size": None,
                        "barcode": "413436788",
                        "vendor_name": "Пава Пава",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 430,
                        "calories": 516,
                        "proteins": 86,
                        "fats": 17.2,
                        "carbs": 0,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Рис Жасмин",
                        "barcode": "623458789",
                        "portion_size": None,
                        "vendor_name": "Мистраль",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 250,
                        "calories": 858,
                        "proteins": 18,
                        "fats": 1,
                        "carbs": 190,
                    },
                ],
            },
            dinner={
                "total_calories": 432,
                "total_proteins": 41,
                "total_fats": 13,
                "total_carbs": 39,
                "products": [
                    {
                        "id": "0fa67bf1-2c2f-4901-9327-a28abcf3beea",
                        "name": "Творог 5%",
                        "barcode": "413466888",
                        "vendor_name": "Ozon",
                        "portion_size": 250,
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 250,
                        "calories": 302,
                        "proteins": 40,
                        "fats": 12.5,
                        "carbs": 7.5,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Изюм Светлый",
                        "barcode": "463458789",
                        "portion_size": None,
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 45,
                        "calories": 130,
                        "proteins": 1,
                        "fats": 0,
                        "carbs": 31,
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
                        "id": "0fa67bf1-2c2f-4901-9327-a28abcf3beea",
                        "name": "Протеиновое Мороженое",
                        "barcode": "413426888",
                        "vendor_name": "Bombar",
                        "portion_size": 250,
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 250,
                        "calories": 302,
                        "proteins": 40,
                        "fats": 12.5,
                        "carbs": 7.5,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Изюм Светлый",
                        "barcode": "463458789",
                        "portion_size": None,
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 45,
                        "calories": 130,
                        "proteins": 1,
                        "fats": 0,
                        "carbs": 31,
                    },
                ],
            },
        ),
        DietDays(
            date=create_training_plans[0].start_date + timedelta(days=4),
            diet=diets_list[0],
            breakfast={
                "total_calories": 952,
                "total_proteins": 20.62,
                "total_fats": 41.64,
                "total_carbs": 122.44,
                "products": [
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Изюм Светлый",
                        "barcode": "463458789",
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 70,
                        "calories": 203,
                        "proteins": 1.75,
                        "fats": 0.35,
                        "carbs": 49,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Миндаль",
                        "barcode": "4634428789",
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 70,
                        "calories": 452,
                        "proteins": 13.02,
                        "fats": 40.39,
                        "carbs": 11.34,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Хлебцы Карамельные",
                        "barcode": "463458341",
                        "vendor_name": "Dr.Korner",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 90,
                        "calories": 297,
                        "proteins": 5.85,
                        "fats": 0.9,
                        "carbs": 62.1,
                    },
                ],
            },
            lunch={
                "total_calories": 1219,
                "total_proteins": 114.4,
                "total_fats": 19.4,
                "total_carbs": 138.2,
                "products": [
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Булгур",
                        "barcode": "46344283131",
                        "vendor_name": "Мистраль",
                        "type": "gram",
                        "portion_size": None,
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 200,
                        "calories": 703,
                        "proteins": 28.4,
                        "fats": 2.2,
                        "carbs": 138.2,
                    },
                    {
                        "id": "0fa67bf1-2c2f-4901-9327-a28abcf3beea",
                        "name": "Филе Голени",
                        "barcode": "413436788",
                        "portion_size": None,
                        "vendor_name": "Пава Пава",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 430,
                        "calories": 516,
                        "proteins": 86,
                        "fats": 17.2,
                        "carbs": 0,
                    },
                ],
            },
            dinner={
                "total_calories": 572,
                "total_proteins": 42.44,
                "total_fats": 27.28,
                "total_carbs": 41.08,
                "products": [
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Изюм Светлый",
                        "barcode": "463458789",
                        "portion_size": None,
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 40,
                        "calories": 116,
                        "proteins": 1,
                        "fats": 0.2,
                        "carbs": 28,
                    },
                    {
                        "id": "79f26cf0-7373-4d3f-b6e3-d4abb9aa9238",
                        "name": "Миндаль",
                        "barcode": "4634428789",
                        "portion_size": None,
                        "vendor_name": "Перекрёсток",
                        "type": "gram",
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 40,
                        "calories": 116,
                        "proteins": 1,
                        "fats": 7.44,
                        "carbs": 6.48,
                    },
                    {
                        "id": "0fa67bf1-2c2f-4901-9327-a28abcf3beea",
                        "name": "Творог 2%",
                        "barcode": "413466488",
                        "vendor_name": "Простаквашино",
                        "type": "gram",
                        "portion_size": 200,
                        "creator_id": "39d4553f-d047-4c2f-aa68-6a5360f87ea9",
                        "amount": 200,
                        "calories": 198,
                        "proteins": 34,
                        "fats": 4,
                        "carbs": 6.6,
                    },
                ],
            },
            snacks={},
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
