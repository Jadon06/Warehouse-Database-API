from fastapi import FastAPI
from .Routers import warehouse
from .models import items, owners
from datetime import datetime

app = FastAPI()

def init_dynamodb():
    if not items.exists():
        items.create_table(wait=True)

    items(
        name="InitItem",
        code="000",
        owner={
            "name": "system",
            "email": "system@example.com"
        },
        details={"quantity": 0,
                 "last_updated": datetime.now()}
    ).save()

    if not owners.exists():
        owners.create_table(wait=True)

init_dynamodb()

app.include_router(warehouse.router)
