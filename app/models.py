from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class details_attr(MapAttribute):
    quantity = NumberAttribute(default=0)
    last_updated = UTCDateTimeAttribute()

class user_attr(MapAttribute):
    name = UnicodeAttribute(hash_key=True)
    phone_number = NumberAttribute(null=True)
    email = UnicodeAttribute(null=False)

class User(GlobalSecondaryIndex):
    class Meta:
        index_name='owner'
        projection=AllProjection()
        host = "http://dynamodb-local:8000"

        write_capacity_units = 5
        read_capacity_units = 5

    name = UnicodeAttribute(hash_key=True)
    phone_number = NumberAttribute(null=True)
    email = UnicodeAttribute(null=False)
    clearance_level = UnicodeAttribute(default='GUEST')

class items(Model):
    class Meta:
        table_name = "warehouse_table"
        region = "us-east-1"
        host = "http://dynamodb-local:8000"

        write_capacity_units = 5
        read_capacity_units = 5
    # NOTE - Can only have one prtition key and one sort key per table
    
    name = UnicodeAttribute(hash_key=True)  # 'hash_key=True' makes this the partition key
    code = UnicodeAttribute(range_key=True) # 'range_key=True' makes this the sort key
    user = user_attr()
    user_index = User() # stores a set of strings which must be all unique
    details = details_attr()

class Users(Model):
    class Meta:
        table_name = "owners_table"
        region = "us-east-1"
        host = "http://dynamodb-local:8000"

        write_capacity_units = 5
        read_capacity_units = 5

    email = UnicodeAttribute(hash_key=True)
    phone_number = NumberAttribute(null=True)
    name = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    clearance_level = UnicodeAttribute(default="GUEST")

    