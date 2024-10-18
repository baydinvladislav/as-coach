from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

from src.shared.config import DYNAMO_DB_PRODUCTS_TABLE_NAME, DYNAMO_DB_PRODUCTS_TABLE_REGION


class Product(Model):
    barcode = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    type = UnicodeAttribute()
    proteins = NumberAttribute()
    fats = NumberAttribute()
    carbs = NumberAttribute()
    calories = NumberAttribute()
    vendor_name = UnicodeAttribute()
    user_id = UnicodeAttribute()

    class Meta:
        table_name = DYNAMO_DB_PRODUCTS_TABLE_NAME
        region = DYNAMO_DB_PRODUCTS_TABLE_REGION
