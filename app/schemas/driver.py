from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class DriverCreate(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str
    password: str

    license_number: str
    license_expiry: Optional[date] = None
    experience_years: Optional[int] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None


class DriverUpdate(BaseModel):
    # User fields (optional — updated on the linked User record)
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None

    # Driver fields
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    experience_years: Optional[int] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    status: Optional[str] = None


class DriverResponse(BaseModel):
    id: int

    full_name: str
    email: EmailStr
    mobile: str

    license_number: str
    license_expiry: Optional[date]
    experience_years: Optional[int]
    address: Optional[str]
    emergency_contact: Optional[str]

    status: str

    class Config:
        from_attributes = True
