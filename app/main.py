from fastapi import Depends, FastAPI, HTTPException, status
from .routers import patient, user
# importing files 
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(patient.router)
 




