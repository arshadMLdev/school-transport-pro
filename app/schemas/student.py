from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    """Common student fields shared by create and response schemas."""

    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )
    admission_number: str = Field(
        min_length=1,
        max_length=50,
    )
    grade: str = Field(
        min_length=1,
        max_length=20,
    )
    section: str | None = Field(
        default=None,
        max_length=10,
    )
    gender: str | None = Field(
        default=None,
        max_length=10,
    )
    date_of_birth: date | None = None
    address: str | None = Field(
        default=None,
        max_length=255,
    )
    parent_id: int = Field(gt=0)

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(
        cls,
        value: date | None,
    ) -> date | None:
        if value is not None and value > date.today():
            raise ValueError(
                "Date of birth cannot be in the future"
            )

        return value


class StudentCreate(StudentBase):
    """Request schema for creating a student."""

    pass


class StudentUpdate(BaseModel):
    """
    Request schema for partially updating a student.

    All fields are optional because PATCH should update only the
    fields supplied in the request.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    admission_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    grade: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    section: str | None = Field(
        default=None,
        max_length=10,
    )
    gender: str | None = Field(
        default=None,
        max_length=10,
    )
    date_of_birth: date | None = None
    address: str | None = Field(
        default=None,
        max_length=255,
    )
    parent_id: int | None = Field(
        default=None,
        gt=0,
    )

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(
        cls,
        value: date | None,
    ) -> date | None:
        if value is not None and value > date.today():
            raise ValueError(
                "Date of birth cannot be in the future"
            )

        return value


class StudentResponse(StudentBase):
    """Response schema returned by Student API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
