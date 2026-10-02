from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json") as f:
        data = json.load(f)

    return data

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

    

