"""add exercises to library

Revision ID: 39597fa7b57c
Revises: 7ca6bc8f8e69
Create Date: 2023-08-09 12:40:07.032498

"""

from alembic import op
from sqlalchemy.orm import Session

from src.domain.models import MuscleGroup, Exercise

# revision identifiers, used by Alembic.
revision = '39597fa7b57c'
down_revision = '7ca6bc8f8e69'
branch_labels = None
depends_on = None


def insert_muscle_groups(session):
    """
    Inserts default muscle group for default exercises
    """

    muscle_groups = (
        MuscleGroup(name="Грудь"),
        MuscleGroup(name="Бицепс"),
        MuscleGroup(name="Спина"),
        MuscleGroup(name="Трицепс"),
        MuscleGroup(name="Ноги"),
        MuscleGroup(name="Плечи"),
        MuscleGroup(name="Пресс")
    )

    session.bulk_save_objects(muscle_groups)
    session.flush()


def insert_exercises(session):
    """
    Inserts default exercises that can fetch any coach in gym library
    """

    chest = session.query(MuscleGroup).filter(MuscleGroup.name == "Грудь").first()
    biceps = session.query(MuscleGroup).filter(MuscleGroup.name == "Бицепс").first()
    back = session.query(MuscleGroup).filter(MuscleGroup.name == "Спина").first()
    triceps = session.query(MuscleGroup).filter(MuscleGroup.name == "Трицепс").first()
    press = session.query(MuscleGroup).filter(MuscleGroup.name == "Ноги").first()
    shoulders = session.query(MuscleGroup).filter(MuscleGroup.name == "Плечи").first()
    legs = session.query(MuscleGroup).filter(MuscleGroup.name == "Пресс").first()

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
        ),
        Exercise(
            name='Жим штанги сидя',
            muscle_group_id=str(shoulders.id)
        ),
        Exercise(
            name='Махи с гантелями в стороны',
            muscle_group_id=str(shoulders.id)
        ),
        Exercise(
            name='Скручивания',
            muscle_group_id=str(press.id)
        ),
    )

    session.bulk_save_objects(exercises)


def upgrade() -> None:
    session = Session(bind=op.get_bind())

    insert_muscle_groups(session)
    insert_exercises(session)

    session.commit()


def downgrade() -> None:
    session = Session(bind=op.get_bind())

    session.query(Exercise).delete()
    session.query(MuscleGroup).delete()

    session.commit()
    session.close()
