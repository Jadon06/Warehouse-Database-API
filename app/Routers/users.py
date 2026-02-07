from fastapi import APIRouter, HTTPException, status
from .. import schemas, models
from pynamodb.exceptions import DoesNotExist
from ..Authentication import utils

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/")
def create_user(user: schemas.ownerCreate):
    try:
        exists = models.Users.get(user.email, range_key=None)
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!")
    except DoesNotExist:
        new_user = models.Users(**user.dict())
        new_user.password = utils.hash(new_user.password)
        new_user.save()
        return new_user.to_simple_dict()    