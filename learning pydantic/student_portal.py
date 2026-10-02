from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field

class Student(BaseModel):
    name: str = Field(max_length=40, min_length=2)
    roll: int = Field(strict=True)
    email: EmailStr
    marks: float = Field(ge=0 , le=100)

    @field_validator('email')
    @classmethod

    def validate_email(cls, email):
        valid_domain = "iitism.ac.in"
        my_domain = email.split('@')[-1]

        if my_domain == valid_domain:
            return email
        else:
            raise ValueError("Enter an email of valid domain")

    @computed_field
    @property

    def passing_status(self) -> bool:
        return (self.marks >= 40)


student_dict = {'name': 'snehil raj', 'roll': 102, 'email': '26je0358@iitism.ac.in', 'marks': 39.8}

student1 = Student(**student_dict)

print(student1)
