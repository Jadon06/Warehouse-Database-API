from fastapi import APIRouter, status, HTTPException
from .. import schemas, models, helper_methods
import hashlib
import pytz
from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

def item_code(item: schemas.itemCreate):
    composite_key = f"{item.owner}-{item.name}".encode("utf-8")
    return hashlib.sha256(composite_key).hexdigest()

def time():
    now_utc = datetime.now(pytz.utc)
    return now_utc

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.itemResponse)
def create_item(item: schemas.itemCreate):
    items = list(models.items.query(item.name))
    if items:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="item already exists")
    item.code = item_code(item)
    new_item = models.items(**item.dict())
    new_item.details.last_updated=time()
    
    new_item.save()
    return new_item

@router.get("/{product_name}", response_model=List[schemas.itemResponse])
def get_item(product_name: str):
    query = models.items.query(product_name)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No item exists with name:{product_name}")
    
    return helper_methods.response_to_dict(query)

@router.put("/{product_name}", status_code=status.HTTP_202_ACCEPTED)
def update_item(product_name : str, updates: schemas.itemCreate):
    item = models.items.get(product_name)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No item exists with name:{product_name}")
    
    updated_item = item.update(actions=[models.items.name.set(updates.name),
                         models.items.code.set(updates.code),
                         models.items.owner.set(updates.owner),
                         models.items.details.last_updated.set(datetime.now())])
    updated_item.save()
    return{"status" : "updated!"}