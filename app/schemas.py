from pydantic import BaseModel, ConfigDict, Field, computed_field, EmailStr
from typing import Annotated, Literal


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

class Patientresponse(BaseModel):
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


class UserIn(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=30)]
    email_id: EmailStr
    hashed_password: Annotated[str, Field(min_length=6)]

class UserOut(BaseModel):
    username: str
    email_id: EmailStr

    model_config = ConfigDict(from_attributes=True)
