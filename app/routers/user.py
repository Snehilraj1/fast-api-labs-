from typing import Annotated, List, Literal
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# importing files 
from .. import models, schemas
from ..database import engine, get_db

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
@router.post("/createuser",  status_code=201, response_model=schemas.UserOut)
def create_user(payload: schemas.UserIn, db: Session = Depends(get_db)):
  user_data = payload.model_dump()
  user_data["hashed_password"] = pwd_context.hash(user_data["hashed_password"])
  new_user = models.User(**user_data)

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@router.get("/users/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username==username).first()

  if not user:
    raise HTTPException(status_code=404, detail="this username doesn't exist")
  return user
