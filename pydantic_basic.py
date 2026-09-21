# Pydantic

from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    EmailStr,
    field_validator,
    model_validator,
    computed_field,
)
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
    height: int = Field(..., description="Height of the patient in centimeters")
    weight: int = Field(..., description="Weight of the patient in kilograms")

    @computed_field(return_type=str, description="BMI of the patient")
    def bmi(self) -> str:
        height_m = self.height / 100  # Convert height to meters
        bmi_value = self.weight / (height_m**2)
        return f"{bmi_value:.2f}"

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        valid_email = ["gmail.com", "yahoo.com", "hotmail.com"]
        value = v.split("@")[-1]
        if value not in valid_email:
            raise ValueError("Invalid email domain")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        return v.upper()

    @model_validator(mode="after")
    def validate_patient(cls, model):
        if model.age > 50 and model.is_married == False:
            raise ValueError("Patients over 50 must be married")
        return model


def create_patient(patient: Patient):
    print(
        f"Patient Name: {patient.name}, Age: {patient.age}, Height: {patient.height}, Weight: {patient.weight}, BMI: {patient.bmi}, Details: {patient.details}, Is Married: {patient.is_married}, Allergies: {patient.allergies}"
    )


data = {
    "name": "John Doe",
    "age": 30,
    "details": {"blood_type": "O+", "height": "5'9", "weight": "160 lbs"},
    "is_married": False,
    # "allergies":["Peanuts", "Shellfish"]
}


try:
    invalid_data = {
        "email": "jane.doe@gmail.com",
        "name": "Jane Doe",
        "age": "8",  # Invalid age type
        "details": {"blood_type": "A-", "height": "5'5", "weight": "130 lbs"},
        "is_married": True,
        "allergies": ["Pollen"],
        "height": 165,
        "weight": 60,
    }
    invalid_patient = Patient(**invalid_data)
    create_patient(invalid_patient)
except ValidationError as e:
    print(f"Validation error creating patient: {e}")
except ValidationError as e:
    print(f"Error creating patient: {e.errors()}")
