from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class details_attr(MapAttribute):
    quantity = NumberAttribute(default=0)
    created_at = UTCDateTimeAttribute()

class Owner(GlobalSecondaryIndex):
    name = UnicodeAttribute(hash_key=True)
    phone_number = NumberAttribute(null=True)
    email = UnicodeAttribute(null=False)

class items(Model):
    class Meta:
        table_name = "warehouse_table"
        region = "us-east-1"
        write_capacity_units = 5
        read_capacity_units = 5
    # NOTE - Can only have one prtition key and one sort key per table
    name = UnicodeAttribute(range_key=True) # 'range_key=True' makes this the sort key 
    code = UnicodeAttribute(hash_key=True) # 'hash_key=True' makes this the partition key
    owner = Owner() # stores a set of strings which must be all unique
    details = details_attr()

class owners(Model):
    class Meta:
        table_name = "owners_table"
        region = "us-east-1"
        write_capacity_units = 5
        read_capacity_units = 5

    name = UnicodeAttribute(hash_key=True)
    phone_number = NumberAttribute(null=True)
    email = UnicodeAttribute(null=False)

if not items.exists():
    items.create_table(wait=True)

if not owners.exists():
    owners.create_table(wait=True)

    