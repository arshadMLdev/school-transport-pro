from pydantic import BaseModel
from datetime import date


class StudentBase(BaseModel):
    parent_id: int
    full_name: str
    grade: str
    section: str
    gender: str
    date_of_birth: date
    address: str
    admission_number: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
