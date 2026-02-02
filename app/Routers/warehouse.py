from fastapi import APIRouter, status, HTTPException
from .. import schemas, models
import hashlib

router = APIRouter(
    prefix="/item",
    tags=["itmes"]
)

def item_code(item: schemas.itemCreate):
    composite_key = f"{item.owner.name}-{item.name}".encode("utf-8")
    return hashlib.sha256(composite_key).hexdigest()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.itemResponse)
def create_item(item: schemas.itemCreate):
    item['code'] = item_code(item)
    new_item = models.items(**item.dict())
    
    exists = None
    for items in models.items.query(item.owner, item.name):
        exists = items

    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="item already exists")
    
    new_item.save()
    return new_item
    