from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, models
from ..Authentication import Oauth, utils

from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.itemResponse)
def create_item(item: schemas.itemCreate, current_user = Depends(Oauth.get_current_user)):
    if current_user.clearance_level != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Clearance level ADMIN required!")
    items = list(models.items.query(item.name))
    if items:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail="item already exists")
    item.code = utils.item_code(item)
    new_item = models.items(**item.dict())
    new_item.details.last_updated=utils.time()
    
    new_item.save()
    return new_item

@router.get("/{product_name}", response_model=List[schemas.itemResponse]) # returns all items with the product name
def get_item(product_name: str):
    query = models.items.query(product_name)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No item exists with name:{product_name}")
    
    return utils.response_to_dict(query)

@router.put("/{primary_key}/{range_key}", status_code=status.HTTP_202_ACCEPTED) # updates quantity, cannot update primary keys like Global Secondary Keys, Partition Keys or Sort Keys
def update_item(primary_key : str, range_key : str, updates: schemas.itemUpdate):
    item = models.items.get(primary_key, range_key)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No item exists with name:{primary_key}")
    print(item)
    item.update(actions=[
                    models.items.details.last_updated.set(datetime.now()),
                    models.items.details.quantity.set(updates.quantity)])
    item.save()
    return item.to_simple_dict()

@router.delete("/{primary_key}/{range_key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(primary_key: str, range_key: str):
    item = models.items.get(primary_key, range_key)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"item with name:{primary_key} and code:{range_key} does not exist!")
    item.delete()
