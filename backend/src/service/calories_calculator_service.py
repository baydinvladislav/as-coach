class CaloriesCalculatorService:
    @staticmethod
    async def calculate_calories(proteins: int, fats: int, carbs: int) -> int:
        protein_coefficient = 4
        carb_coefficient = 4
        fat_coefficient = 9
        result = (proteins * protein_coefficient) + (carbs * carb_coefficient) + (fats * fat_coefficient)
        return result
