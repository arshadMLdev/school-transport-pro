from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict



class StudentCreate(BaseModel):
    """
    Schema used when creating a new student.
    """

    full_name: str

    admission_number: str

    grade: str

    section: Optional[str] = None

    gender: Optional[str] = None

    date_of_birth: Optional[date] = None

    address: Optional[str] = None

    parent_id: int



class StudentUpdate(BaseModel):
    """
    Schema used for updating student information.

    All fields are optional because updates are partial.
    Example:
    
    {
        "address": "Mumbai"
    }

    Only address will be updated.
    """

    full_name: Optional[str] = None

    admission_number: Optional[str] = None

    grade: Optional[str] = None

    section: Optional[str] = None

    gender: Optional[str] = None

    date_of_birth: Optional[date] = None

    address: Optional[str] = None

    parent_id: Optional[int] = None



class StudentResponse(BaseModel):
    """
    Schema returned to API clients.
    """

    id: int

    full_name: str

    admission_number: str

    grade: str

    section: Optional[str] = None

    gender: Optional[str] = None

    date_of_birth: Optional[date] = None

    address: Optional[str] = None

    parent_id: int

    created_at: datetime

    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )
