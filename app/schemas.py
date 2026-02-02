from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ownerCreate(BaseModel):
    name: str
    phone_number: Optional[int] = None
    email: EmailStr

class details_schema(BaseModel):
    quantity: int
    created_at: datetime

class itemCreate(BaseModel):
    name: str
    code: str
    owner: str
    details: details_schema

class itemResponse(itemCreate):
    pass

