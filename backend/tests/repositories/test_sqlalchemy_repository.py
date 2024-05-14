"""
Tests SQLAlchemy repository
"""

import pytest

from sqlalchemy import delete

from src.repository.base_repository import BaseRepository
from src import Coach, Exercise
from src.utils import generate_random_password


@pytest.mark.asyncio
async def test_create_method_positive(db):
    """
    Tests method to create new record through SQLAlchemy repo
    """

    repo = BaseRepository(session=db)
    repo.model = Coach

    coach_data = {
        "username": "+79253332211",
        "password": generate_random_password(8),
        "first_name": "Станислав",
        "fcm_token": "test_token_value",
    }

    coach = await repo.create(**coach_data)

    assert isinstance(coach, Coach)

    assert coach.id is not None
    assert coach.password is not None
    assert coach.username == coach_data["username"]
    assert coach.first_name == coach_data["first_name"]

    await db.execute(delete(Coach).where(Coach.username == coach_data["username"]))
    await db.commit()


@pytest.mark.asyncio
async def test_create_method_raise_attribute_error(db):
    """
    Tests raising error because of invalid attributes
    """

    repo = BaseRepository(session=db)
    repo.model = Coach

    coach_data = {
        "username": "+79253332211",
        "password": generate_random_password(8),
        "first_name": "Станислав",
        "fake_field": "some_value"
    }
    with pytest.raises(AttributeError):
        await repo.create(**coach_data)


@pytest.mark.asyncio
async def test_get_method(create_customer, db):
    """
    Tests the successful receiving of the object
    """

    repo = BaseRepository(session=db)
    repo.model = Coach

    customer = create_customer
    result = await repo.get(pk=str(customer.coach.id))

    assert isinstance(result, Coach)


@pytest.mark.asyncio
async def test_get_all_method(db):
    """
    Tests the successful receiving all objects from table
    """

    repo = BaseRepository(session=db)
    repo.model = Exercise

    result = await repo.get_all()

    assert all(list(map(lambda x: isinstance(x, Exercise), result)))


@pytest.mark.asyncio
async def test_filter_method(create_customer, db):
    """
    Tests the filtering correctness
    """

    repo = BaseRepository(session=db)
    repo.model = Exercise

    result = await repo.filter(filters={"name": "Жим штанги лежа"}, foreign_keys=[], sub_queries=[])

    for exercise in result:
        assert exercise.name == "Жим штанги лежа"
