from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import Annotated, Literal, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='Sraj@1332', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected")
        break
    except Exception as error:
        print("Database connection failed")
        print("error: ", error)
        time.sleep(2)

    
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="id of the patient")]
    name: Annotated[str, Field(..., description="name of the patient", max_length=40, min_length=2)] 
    city: Annotated[str, Field(..., description="city of the patient")]
    age: Annotated[int, Field(..., description="age of the patient", ge=0, le=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="gender of the patient")]
    height: Annotated[float, Field(gt=0, description="height of the patient in (m)")] 
    weight: Annotated[float, Field(gt=0, description="height of the patient in (kg)")] 

    @computed_field 
    @property
    def bmi (self) -> float:
        bmi = self.weight/(self.height**2)
        bmi = round(bmi, 2)

        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 30:
            return "normal"
        else:
            return "obese"

def load_data():
    cursor.execute('SELECT * FROM "Patient Management"')
    data = cursor.fetchall()
    return data


@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = 'id of the patient in the db', example = "P001",)):

    cursor.execute('SELECT * FROM "Patient Management" WHERE id = %s', (patient_id))
    patient = cursor.fetchone()

    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    return patient

@app.post("/create")
def create_patient(patient : Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status=400, detail="patient already exists")
    else:
        pass







