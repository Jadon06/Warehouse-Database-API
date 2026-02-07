from passlib.context import CryptContext
import pynamodb.pagination
from .. import schemas
import hashlib
import pytz
from datetime import datetime

# Hashing algortihm for User password security
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(pw: str):
    return pwd_context.hash(pw)

def verify(plain_pw: str, database_pw: str):
    return pwd_context.verify(plain_pw, database_pw)

def response_to_dict(query: pynamodb.pagination.ResultIterator):
    results = []
    for item in query:
        to_dict = item.to_simple_dict()
        results.append(to_dict)
    return results

def item_code(item: schemas.itemCreate):
    composite_key = f"{item.owner}-{item.name}".encode("utf-8")
    return hashlib.sha256(composite_key).hexdigest()

def time():
    now_utc = datetime.now(pytz.utc)
    return now_utc