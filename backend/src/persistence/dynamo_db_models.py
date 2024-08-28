from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model


class Product(Model):
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    barcode = UnicodeAttribute()
    product_type = UnicodeAttribute()
    proteins = NumberAttribute()
    fats = NumberAttribute()
    carbs = NumberAttribute()
    calories = NumberAttribute()
    vendor_name = UnicodeAttribute()
    user_id = UnicodeAttribute()

    # TODO: table indexes
    # name_index = NameIndex()
    # vendor_name_index = VendorNameIndex()

    class Meta:
        table_name = "products"
        region = "us-east-1"
