from typing import Annotated, List, Literal
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, computed_field
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class PatientBase(BaseModel):
  name: Annotated[
      str,
      Field(
          ..., description="name of the patient", max_length=40, min_length=2
      ),
  ]
  city: Annotated[str, Field(..., description="city of the patient")]
  age: Annotated[
      int, Field(..., description="age of the patient", ge=0, le=120)
  ]
  gender: Annotated[
      Literal["male", "female", "others"],
      Field(..., description="gender of the patient"),
  ]
  height: Annotated[
      float, Field(gt=0, description="height of the patient in (m)")
  ]
  weight: Annotated[
      float, Field(gt=0, description="weight of the patient in (kg)")
  ]

  @computed_field
  @property
  def bmi(self) -> float:
    return round(self.weight / (self.height**2), 2)

  @computed_field
  @property
  def verdict(self) -> str:
    if self.bmi < 18.5:
      return "underweight"
    elif self.bmi < 30.0:
      return "normal"
    return "obese"


class PatientOut(PatientBase):
  id: int
  model_config = ConfigDict(from_attributes=True)


@app.get("/view", response_model=List[PatientOut])
def view_all(db: Session = Depends(get_db)):
  return db.query(models.Patient).all()


@app.get("/patient/{patient_id}", response_model=PatientOut)
def view_patient(patient_id: int, db: Session = Depends(get_db)):
  patient = (
      db.query(models.Patient).filter(models.Patient.id == patient_id).first()
  )
  if not patient:
    raise HTTPException(status_code=404, detail="patient not found")
  return patient


@app.post("/create", response_model=PatientOut, status_code=201)
def create_patient(payload: PatientBase, db: Session = Depends(get_db)):
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


@app.put("/update/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: int, payload: PatientBase, db: Session = Depends(get_db)
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


