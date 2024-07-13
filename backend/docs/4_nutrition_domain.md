## Nutrition domain (microservice)
Rendering the nutrition screen, which is the main screen on the customer side, 
the frontend should request these endpoints to work with nutrition domain.

### Table of Contents
- [API](#api)
- [Data Storage Structure](#data-storage-structure)

### API
* ```GET nutrition/diets/${customer_id}/${date}```:
    * info: to get diet for day by date
    * example: nutrition/diets/daa19459-d64c-4372-9e3b-d4de63be7d08/2024-07-11
    * response: ./extras/get_nutrition_diets_for_customer_by_date.json

* ```POST nutrition/diets/${diet_id}/breakfast||lunch||dinner||snacks/```:
    * info: to put product into diet for one of the meal
    * example: nutrition/diets/40f15a2d-bcb3-4a20-9b37-8e89a1d4c8fd/breakfast/477fccb8-0e2b-4ab7-94e6-702618bb6b15
    * request: {"product_id": "d9428888-122b-11e1-b85c-61cd3cbb3210", "amount": 150}
    * response: ./extras/post_add_product_to_diet_response.json

* ```GET nutrition/products/${product_word}```:
    * info: to get products with their info by some relative product word
    * example_1: nutrition/products/молоко
    * example_2: nutrition/products/молоко-простоквашино
    * example_2: nutrition/products/простоквашино-молоко-2%
    * response: ./extras/get_receive_product.json

* ```POST nutrition/products```:
    * info: to put product to AsCoach database
    * example: nutrition/products
    * request: ./extras/post_create_product.json
    * response: ./extras/get_receive_product.json

* ```GET nutrition/products/${product_id}```:
    * info: to get product data by product id for product detail card
    * example: nutrition/products/d7182bb0-9a03-4e48-86ca-8b20d4a9bcba
    * response: ./extras/get_receive_product.json


### Data Storage Structure
Command Query Responsibility Segregation (CQRS) pattern, separating the write operations (commands) 
from the read operations (queries).

* AWS DynamoDB: Used for storing product data and handling insert/update operations.
* AWS OpenSearch Service: Used for indexing and full-text search of product data.
* AWS Lambda: Used to synchronize data between DynamoDB and OpenSearch.
