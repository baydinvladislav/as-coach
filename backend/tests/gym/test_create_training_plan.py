import pytest

from httpx import AsyncClient

from src.main import app
from src.customer.models import TrainingPlan
from src.auth.utils import create_access_token


@pytest.mark.anyio
async def test_create_training_plan_successfully(create_customer, override_get_db):
    """
    Successfully training plan creation
    """
    training_plan_data = {
        "start_date": "2023-04-10",
        "end_date": "2023-04-16",
        "diets": [
            {
                "proteins": 200,
                "fats": 100,
                "carbs": 400
            }
        ],
        "trainings": [
            {
                "name": "Плечи, грудь",
                "exercises": [
                    {
                        "id": "string",
                        "sets": [20, 15, 10, 15, 20]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 12, 12]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    }
                ]
            },
            {
                "name": "Спина, задняя дельта, бицепс",
                "exercises": [
                    {
                        "id": "string",
                        "sets": [15, 8, 8, 8, 8]
                    },
                    {
                        "id": "string",
                        "sets": [15, 8, 8, 8, 8]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [20, 15, 10, 15, 20]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15, 15]
                    },
                ]
            },
            {
                "name": "Грудь средняя и передняя дельты, трицепс",
                "exercises": [
                    {
                        "id": "string",
                        "sets": [10, 10, 10, 10]
                    },
                    {
                        "id": "string",
                        "sets": [12, 12, 12, 12]
                    },
                    {
                        "id": "string",
                        "sets": [12, 12, 12, 12]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [10, 10, 10, 10]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    }
                ]
            },
            {
                "name": "Ноги",
                "exercises": [
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [10, 10, 10, 10]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [10, 10, 10, 10]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    },
                    {
                        "id": "string",
                        "sets": [12, 12, 12, 12]
                    },
                    {
                        "id": "string",
                        "sets": [20, 20, 20, 20]
                    },
                    {
                        "id": "string",
                        "sets": [15, 15, 15, 15]
                    }
                ]
            }
        ]
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        auth_token = create_access_token(create_customer.user.username)
        response = await ac.post(
            f"/api/customers/{create_customer.id}/week_plans/",
            json=training_plan_data,
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

    assert response.status_code == 201

    if response.status_code == 201:
        training_plan = override_get_db.query(TrainingPlan).filter(
            TrainingPlan.id == response.json()["id"]
        ).first()
        override_get_db.delete(training_plan)
        override_get_db.commit()
