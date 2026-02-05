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
    try:
        user = models.owners.get(user_credentials.name, range_key=None)
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")
    
    # create a token
    # return the token for login
    access_token = Oauth.create_acess_token(data={"User_id" : user.id, "email" : user.email})
    return {"access_token" : access_token, "token_type" : "Bearer"}