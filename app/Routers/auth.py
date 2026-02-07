from fastapi import APIRouter, Depends, status, HTTPException, Response
# from sqlalchemy.orm import Session
# from ..database import get_db
from .. import models, schemas
from .. Authentication import Oauth, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pynamodb.exceptions import DoesNotExist

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    print(user_credentials.username)
    try:
        user = models.Users.get(user_credentials.username, range_key=None)
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")
        access_token = Oauth.create_acess_token(data={"email" : user.email, "clearance_level" : user.clearance_level})
        return {"access_token" : access_token, "token_type" : user.clearance_level}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")