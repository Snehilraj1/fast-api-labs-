from typing import Annotated, List, Literal
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, computed_field
from sqlalchemy.orm import Session

# importing files 
from . import models
from .database import engine, get_db
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/view", response_model=List[schemas.Patientresponse])
def view_all(db: Session = Depends(get_db)):
  return db.query(models.Patient).all()


@app.get("/patient/{patient_id}", response_model=schemas.Patientresponse)
def view_patient(patient_id: int, db: Session = Depends(get_db)):
  patient = (
      db.query(models.Patient).filter(models.Patient.id == patient_id).first()
  )
  print(type(patient))
  if not patient:
    raise HTTPException(status_code=404, detail="patient not found")
  return patient


@app.post("/create",  status_code=201)
def create_patient(payload: schemas.PatientBase, db: Session = Depends(get_db)):
  new_patient = models.Patient(
      **payload.model_dump()
  )
#   basically parsing a python dict making the code clearner 
  db.add(new_patient)
  db.commit()
  db.refresh(new_patient)
  return new_patient


@app.delete("/delete/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
  patient = (
      db.query(models.Patient).filter(models.Patient.id == patient_id).first()
  )
  if not patient:
    raise HTTPException(status_code=404, detail="patient not found")
  db.delete(patient)
  db.commit()


@app.put("/update/{patient_id}", )
def update_patient(
    patient_id: int, payload: schemas.PatientBase, db: Session = Depends(get_db)
):
  query = db.query(models.Patient).filter(models.Patient.id == patient_id)
  patient = query.first()
  if not patient:
    raise HTTPException(status_code=404, detail="patient not found")

  data = payload.model_dump()
  data["bmi"] = payload.bmi
  data["verdict"] = payload.verdict

  query.update(data, synchronize_session=False)
  db.commit()
  db.refresh(patient)
  return patient


@app.post("/createuser",  status_code=201, response_model=schemas.UserOut)
def create_patient(payload: schemas.UserIn, db: Session = Depends(get_db)):
  new_user = models.User(
      **payload.model_dump()
  )
#   basically parsing a python dict making the code clearner 
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user



