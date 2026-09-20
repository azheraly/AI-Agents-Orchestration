# Pydantic

from pydantic import BaseModel, ValidationError, Field, EmailStr, field_validator
from typing import Annotated, List, Dict, Optional


class Patient(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            ..., description="The email of the patient", example="john.doe@example.com"
        ),
    ]
    name: Annotated[
        str,
        Field(..., description="The name of the patient", min_length=1, max_length=100),
    ]
    age: Annotated[int, Field(..., description="The age of the patient", gt=0, lt=150)]
    details: Annotated[
        Dict[str, str], Field(..., description="Additional details about the patient")
    ]
    is_married: Annotated[
        bool, Field(default=False, description="Indicates if the patient is married")
    ]
    allergies: Annotated[
        Optional[List[str]], Field(None, description="List of patient allergies")
    ]

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        valid_email = ["gmail.com", "yahoo.com", "hotmail.com"]
        value = v.split("@")[-1]
        if value not in valid_email:
            raise ValueError("Invalid email domain")
        return v


def create_patient(patient: Patient):
    print(
        f"Patient Name: {patient.name}, Age: {patient.age} , Details: {patient.details}, Is Married: {patient.is_married}, Allergies: {patient.allergies}"
    )


data = {
    "name": "John Doe",
    "age": 30,
    "details": {"blood_type": "O+", "height": "5'9", "weight": "160 lbs"},
    "is_married": True,
    # "allergies":["Peanuts", "Shellfish"]
}


try:
    invalid_data = {
        "email": "jane.doe@example.com",
        "name": "Jane Doe",
        "age": "5",  # Invalid age type
        "details": {"blood_type": "A-", "height": "5'5", "weight": "130 lbs"},
        "is_married": False,
        # "allergies":["Pollen"]
    }
    invalid_patient = Patient(**invalid_data)
    create_patient(invalid_patient)
except ValidationError as e:
    print(f"Validation error creating patient: {e}")
except ValidationError as e:
    print(f"Error creating patient: {e.errors()}")
