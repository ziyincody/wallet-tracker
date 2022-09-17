from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import NumberAttribute


class TransactionAddressIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'transaction-address-index'
        read_capacity_units = 10
        write_capacity_units = 10
        projection = AllProjection()

    address = UnicodeAttribute(hash_key=True)

class Transaction(Model):
    class Meta:
        table_name = 'Transaction'
        region = 'us-east-1'
        host = "http://localhost:8000"
        write_capacity_units = 10
        read_capacity_units = 10
        aws_access_key_id = 'DUMMYIDEXAMPLE'
        aws_secret_access_key = 'DUMMYEXAMPLEKEY'

    tx_id = UnicodeAttribute(hash_key=True)
    tx_created_at_ms = NumberAttribute()
    tx_details = UnicodeAttribute()
    address = UnicodeAttribute()
    address_index = TransactionAddressIndex()
