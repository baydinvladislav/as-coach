import os
from datetime import date, timedelta
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.customer.models import Customer, TrainingPlan
from src.auth.utils import get_hashed_password
from src.dependencies import get_db
from src.main import app
from src.auth.models import User
from src.gym.models import Exercise, MuscleGroup
from src.customer.utils import generate_random_password

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_USER_USERNAME = os.getenv("TEST_USER_USERNAME")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


@pytest.fixture()
def create_muscle_groups(override_get_db):
    muscle_groups = override_get_db.query(MuscleGroup).all()
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


@pytest.fixture()
def create_exercises(create_muscle_groups, override_get_db):
    exercises = override_get_db.query(Exercise).all()
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


@pytest.fixture()
def create_customer(create_user, override_get_db):
    """
    Creates test customer
    """
    test_user = override_get_db.query(User).filter(
        User.username == create_user.username
    ).first()

    if not test_user.customers:
        test_customer = Customer(
            username='+79991119922',
            first_name='Арнольд',
            last_name='Шварцнеггер',
            password=generate_random_password(8),
            user_id=str(create_user.id)
        )

        override_get_db.add(test_customer)
        override_get_db.commit()
        return test_customer
    else:
        return test_user.customers[0]


@pytest.fixture()
def create_user(override_get_db):
    """
    Creates test user
    """
    test_user = override_get_db.query(User).filter(
        User.username == TEST_USER_USERNAME
    ).first()

    if not test_user:
        test_user = User(
            username=TEST_USER_USERNAME,
            first_name='Владислав',
            password=get_hashed_password(TEST_USER_PASSWORD)
        )

        override_get_db.add(test_user)
        override_get_db.commit()

    return test_user


@pytest.fixture()
def override_get_db():
    """
    Creates session to testing db
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """
    In the beginning on each test creates database schema,
    also changes production db to testing db
    """
    from src.database import Base

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
