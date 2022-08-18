from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, utils, oauth2
from database import get_db


router = APIRouter(
    # prefix="/users",
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # create a token
    return {"access_token": access_token, "token_type": "bearer"}



# @router.get("/{id}", response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#
#     user = db.query(models.User).filter(models.User.id == id).first()
#
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"user with id: {id} does not exist")
#     return user