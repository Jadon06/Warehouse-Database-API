from fastapi import FastAPI
from .Routers import warehouse, users, auth
from .models import items, Users
from datetime import datetime

app = FastAPI()

def init_dynamodb():
    if not items.exists():
        items.create_table(wait=True)

    items(
        name="InitItem",
        code="000",
        user={
            "name": "system",
            "email": "system@example.com"
        },
        details={"quantity": 0,
                 "last_updated": datetime.now()}
    ).save()

    if not Users.exists():
        Users.create_table(wait=True)

    Users(
        name="InitName",
        phone_number=000000000,
        email="initemail@gmail.com",
        password="password",
        clearance_level="GUEST"
    ).save()

init_dynamodb()

app.include_router(warehouse.router)
app.include_router(users.router)
app.include_router(auth.router)