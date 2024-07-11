## Nutrition domain (microservice)
To get nutrition data for rendering the nutrition screen, which is the main screen on the customer side, 
the frontend should request the `/customers/${customer_id}/nutrition` endpoint.

### Table of Contents
- [API](#api)
- [Data Storage Structure](#data-storage-structure)

### API
* ```GET nutrition/diets/${customer_id}/${date}```:
    * info: to get diet for day by date
    * example: nutrition/diets/daa19459-d64c-4372-9e3b-d4de63be7d08/2024-07-11
    * response: backend/extras/get_nutrition_diets_for_customer_by_date.json

* ```POST nutrition/diets/${diet_id}/breakfast || lunch || dinner || snacks/{product_id}```:
    * info: to put product into diet for one of the meal
    * example: nutrition/diets/40f15a2d-bcb3-4a20-9b37-8e89a1d4c8fd/breakfast/477fccb8-0e2b-4ab7-94e6-702618bb6b15
    * request:
    * response:

* ```GET nutrition/products/${product_word}```:
    * info: to get products with their info by some relative product word
    * example_1: nutrition/products/молоко
    * example_2: nutrition/products/молоко-простоквашино
    * example_2: nutrition/products/простоквашино-молоко-2%
    * response:

* ```POST nutrition/products```:
    * info: to put product to AsCoach database
    * example: nutrition/products
    * request:
    * response:

* ```GET nutrition/products/${product_id}```:
    * info: to get product data by product id
    * example: nutrition/products/d7182bb0-9a03-4e48-86ca-8b20d4a9bcba
    * request:
    * response:


### Data Storage Structure
tbd: which datastorage I should use? how do I can store the data?
