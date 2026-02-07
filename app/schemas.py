from pydantic import BaseModel, EmailStr, SecretStr
from datetime import datetime
from typing import Optional, Literal

class ownerCreate(BaseModel):
    name: str
    phone_number: Optional[int] = None
    email: EmailStr
    password: str
    clearance_level: Literal["GUEST", "ADMIN", "EMPLOYEE"]

class ownerResponse(ownerCreate):
    name: str
    phone_number: Optional[int] = None
    email: EmailStr
    password: SecretStr
    clearance_level: Literal["GUEST", "ADMIN", "EMPLOYEE"]

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
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str