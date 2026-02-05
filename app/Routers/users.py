from fastapi import APIRouter, HTTPException, status
from .. import schemas, models
from pynamodb.exceptions import DoesNotExist

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/")
def create_user(user: schemas.ownerCreate):
    try:
        exists = models.owners.get(user.name, range_key=None)
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!")
    except DoesNotExist:
        new_user = models.owners(**user.dict())
        new_user.save()
        return new_user.to_simple_dict()    