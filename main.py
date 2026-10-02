from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="id of the patient")]
    name: Annotated[str, Field(..., description="name of the patient", max_length=40, min_length=2)] 
    city: Annotated[str, Field(..., description="city of the patient")]
    age: Annotated[str, Field(..., description="age of the patient", ge=0, le=120)]
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
    with open("patients.json") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Record Managment API"}

@app.get("/about")
def aboutb():
    return {"message": "Manage your Patient"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description = 'id of the patient in the db', example = "P001",)):
    data  = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")

def sort(sortby: str = Query("height", description="Sort on the basis of height, weight and bmi"), order: str = Query("asc", description="Sort in ascending and descending order.")):

    valid_fields = ['height', 'weight', 'bmi']
    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid key, select a {valid_fields}")

    valid_order = ['asc', 'desc']
    if order not in valid_order:
        raise HTTPException(status_code=400, detail=f"invalid order, select a {valid_order}")

    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key= lambda x : x.get(sortby, 0), reverse=sort_order)

    return sorted_data 

@app.post("/create")
def create_patient(patient : Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status=400, detail="patient already exists")
    else:
        data[patient.id] = patient.model_dump(exclude='id')
        save_data(data)
        return JSONResponse(status_code=201, content={'message' : "patient created successfully"})



