
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # field function is also used to add description to these things like name etc
    name: str = Field(max_length=50, min_length=1, title="name of the patient", description="Name the patie" \
    "int in less than 50 letters")
    age: int 
    height: float 
    weight: float = Field(strict=True) # or the annotated one, strict to prevent type changing if the data is str it will not be converted to float
    allergies: Optional[List[str]] = None #make it optional and give a default value if no allergies then none 
    married: Optional[bool] = None 
    contact_info: Dict[str, str]

    # we have to validate the emails before accepting them 
    email: EmailStr
    linkedin: AnyUrl

    # for custom things use field and for inbuilt templates use emailstr anyurl etc there are a lot 

    # lets aslo validate email/
    @field_validator('email') #field validator has two modes before (before type conveersion), after (after type conversion)
    @classmethod
    def email_validator(cls, value):

        valid_domain = ['iitism.ac.in', 'hdfc.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domain:
            raise ValueError("Email not a valid domain")

        return value

    @field_validator("age")
    @classmethod

    def validate_age(cls, value):
        if (0<value<100):
            return value
        else:
            raise ValueError("Age must be under 0 and 100")

    # to validate using two vars or more we will use model validator as field is for one we are working on the whol pydantic model not a single field
    @model_validator(mode='after')
    def emergencyContactValidator(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_info:
            raise ValueError("People more than 60 must have a emergency contact no.")


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = ((self.height)**2)/self.weight
        bmi = 1/bmi

        return round(bmi, 2)

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.weight)
    print(patient.bmi)
    print("inserted")

patient_info = {'name': "snehil", 'age': 65, 'weight': 6.7,'height' : 9.8, 'allergies': ['water', 'dogs'], 'contact_info': {'emergency': "8694865958"}, 'married': True, 'email': "snehilraj@iitism.ac.in", 'linkedin': 'http://linkein.com/64654'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)