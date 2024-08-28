import pytest

from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_product(create_customer):
    response = await make_test_http_request(
            url="api/nutrition/products/406c4cec-a14f-4424-8507-3df2a7954fdd",
            method="get",
            username=create_customer.username,
        )
    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_search_product(create_customer):
#     response = await make_test_http_request(
#         url="api/nutrition/products/lookup?query_text=молоко",
#         method="get",
#         username=create_customer.username,
#     )
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_product(create_customer):
    product_data = {
        "name": "Творог 5%",
        "barcode": 123456789,
        "product_type": "gram",
        "proteins": 20,
        "fats": 5,
        "carbs": 0,
        "vendor_name": "Простаквашино",
    }

    response = await make_test_http_request(
        url="api/nutrition/products",
        method="post",
        username=create_customer.username,
        json=product_data,
    )

    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("id") is not None
    assert response_json.get("name") is not None
