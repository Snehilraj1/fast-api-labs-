from pydantic import BaseModel, Field, field_validator

class Address(BaseModel):
    city: str
    state: str
    pin: int

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, pin):
        if len (str(pin)) == 5:
            return pin
        else:
            raise ValueError("The pincode must be of 5 digits")

class Patient(BaseModel):
    name: str 
    gender: str
    age: int 
    address: Address

adress_dict = {'city': "dhanbad", 'state': "jharkhand", 'pin': 78654}

address1 = Address(**adress_dict)

patient_dict = {'name': 'rohan', 'gender': 'male', 'age': 67, 'address' : address1}
patient1 = Patient(**patient_dict)

print(patient1.address.pin)


# now to export the pydantic objects to a python dictionary and a json too
temp = patient1.model_dump()

print(temp)

# for the json 
temp2 = patient1.model_dump_json()

print(type(temp2), "this is temp2")

# to include only 1 or more things 
temp = patient1.model_dump(include=['name', 'age'])

# similarly you can export too 

