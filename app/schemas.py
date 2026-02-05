from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ownerCreate(BaseModel):
    name: str
    phone_number: Optional[int] = None
    email: EmailStr

class ownerResponse(ownerCreate):
    pass

class details_schema(BaseModel):
    quantity: int

class details_schema_response(BaseModel):
    quantity: int
    last_updated: datetime

class itemCreate(BaseModel):
    name: str
    code: Optional[str] = None
    owner: ownerCreate
    details: details_schema

class itemResponse(BaseModel):
    name: str
    code: str
    owner: ownerResponse
    details: details_schema_response

class itemUpdate(BaseModel):
    quantity : Optional[int] = 0

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str