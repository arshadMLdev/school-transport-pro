from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class StudentCreate(BaseModel):
    full_name: str
    admission_number: str
    grade: str
    section: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    parent_id: int


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    admission_number: Optional[str] = None
    grade: Optional[str] = None
    section: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    parent_id: Optional[int] = None


class StudentResponse(BaseModel):

    id: int
    full_name: str
    admission_number: str
    grade: str
    section: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[date]
    address: Optional[str]
    parent_id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True
    )
