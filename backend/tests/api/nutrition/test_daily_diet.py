from datetime import timedelta

import pytest
from unittest.mock import patch

from src.schemas.product_dto import ProductDtoSchema
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_diets):
    customer_username = create_diets[0].training_plans.customer.username
    specific_day = create_diets[0].training_plans.start_date + timedelta(days=2)

    response = await make_test_http_request(
        url=f"api/nutrition/diets/{specific_day}",
        method="get",
        username=customer_username,
    )

    assert response.status_code == 200

    response = response.json()
    assert "date" in response
    assert "actual_nutrition" in response

    meals = response["actual_nutrition"]
    assert "daily_total" in meals
    assert "breakfast" in meals
    assert "lunch" in meals
    assert "dinner" in meals
    assert "snacks" in meals


@pytest.mark.asyncio
@patch("src.repository.product_repository.ProductRepository.get_products_by_barcodes")
async def test_add_product_to_diet(mock_insert_product, create_diets):
    updating_daily_diet = create_diets[0].diet_days[0]
    prev_consumed_calories = updating_daily_diet.breakfast["total_calories"]
    prev_consumed_proteins = updating_daily_diet.breakfast["total_proteins"]
    prev_consumed_fats = updating_daily_diet.breakfast["total_fats"]
    prev_consumed_carbs = updating_daily_diet.breakfast["total_carbs"]

    daily_diet_id = str(create_diets[0].diet_days[0].id)
    customer_username = create_diets[0].training_plans.customer.username

    updating_meal = "breakfast"
    product_data = {
        "daily_diet_id": daily_diet_id,
        "meal_type": updating_meal,
        "product_data": [
            {"barcode": "123456789", "amount": 300},
            {"barcode": "987654321", "amount": 100},
        ],
    }

    full_product_info_1 = ProductDtoSchema(
        name="Первый новый продукт",
        barcode="123456789",
        type="milliliter",
        proteins=20,
        fats=10,
        carbs=20,
        calories=250,
        vendor_name="Простаквашино",
        user_id=str(create_diets[0].training_plans.customer.id),
    )
    full_product_info_2 = ProductDtoSchema(
        name="Второй новый продукт",
        barcode="987654321",
        type="gram",
        proteins=5,
        fats=4,
        carbs=70,
        calories=330,
        vendor_name="Простаквашино",
        user_id=str(create_diets[0].training_plans.customer.id),
    )
    mock_insert_product.return_value = [full_product_info_1, full_product_info_2]

    response = await make_test_http_request(
        url=f"api/nutrition/diets",
        method="post",
        json=product_data,
        username=customer_username,
    )

    assert response.status_code == 201
    response_json = response.json()

    product_names = [product["name"] for product in response_json["actual_nutrition"][updating_meal]["products"]]
    assert full_product_info_1.name in product_names
    assert full_product_info_2.name in product_names

    # 3 = 300gr, 1 = 100gr
    added_calories = full_product_info_1.calories * 3 + full_product_info_2.calories * 1
    added_proteins = full_product_info_1.proteins * 3 + full_product_info_2.proteins * 1
    added_fats = full_product_info_1.fats * 3 + full_product_info_2.fats * 1
    added_carbs = full_product_info_1.carbs * 3 + full_product_info_2.carbs * 1

    assert prev_consumed_calories + added_calories == response_json["actual_nutrition"][updating_meal]["total_calories"]
    assert prev_consumed_proteins + added_proteins == response_json["actual_nutrition"][updating_meal]["total_proteins"]
    assert prev_consumed_fats + added_fats == response_json["actual_nutrition"][updating_meal]["total_fats"]
    assert prev_consumed_carbs + added_carbs == response_json["actual_nutrition"][updating_meal]["total_carbs"]
