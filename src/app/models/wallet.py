from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, BooleanAttribute
)

class Wallet(Model):
    class Meta:
        table_name = 'Wallet'
        region = 'us-east-1'
        host = "http://localhost:8000"
        write_capacity_units = 10
        read_capacity_units = 10
        aws_access_key_id = 'DUMMYIDEXAMPLE'
        aws_secret_access_key = 'DUMMYEXAMPLEKEY'

    address = UnicodeAttribute(hash_key=True)
    balance = NumberAttribute()
    last_updated_ms = NumberAttribute()
    is_updating = BooleanAttribute()
