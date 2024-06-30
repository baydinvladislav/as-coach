## Nutrition domain
To get nutrition data for rendering the nutrition screen, which is the main screen on the customer side, 
the frontend should request the `/customers/${customer_id}/nutrition` endpoint.

### Table of Contents
- [Response Structure](#response-structure)
- [Data Storage Structure](#data-storage-structure)

### Response Structure
```json
{
    "actual_nutrition": {
        "daily_total": {
            "proteins": {
                "consumed": integer,
                "total": integer,
                "calories": integer
            },
            "fats": {
                "consumed": integer,
                "total": integer,
                "calories": integer
            },
            "carbs": {
                "consumed": integer,
                "total": integer,
                "calories": integer
            }
        },
        "breakfast": {
            "total": {
                "proteins": integer,
                "fats": integer,
                "carbs": integer,
                "calories": integer
            },
            "products": [
                {
                    "id": internal_id,
                    "name": string,
                    "amount": integer,
                    "type": enum(liquid/solid),
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                }
            ]
        },
        "lunch": {
            "total": {
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                },
            "products": [
                {
                    "id": internal_id,
                    "name": string,
                    "amount": integer,
                    "type": enum(liquid/solid),
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                }
            ]
        },
        "dinner": {
            "total": {
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                },
            "products": [
                {
                    "id": internal_id,
                    "name": string,
                    "amount": integer,
                    "type": enum(liquid/solid),
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                }
            ]
        },
        "snacks": {
            "total": {
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                },
            "products": [
                {
                    "id": internal_id,
                    "name": string,
                    "amount": integer,
                    "type": enum(liquid/solid),
                    "proteins": integer,
                    "fats": integer,
                    "carbs": integer,
                    "calories": integer
                }
            ]
        }
    }
}
```

### Data Storage Structure
