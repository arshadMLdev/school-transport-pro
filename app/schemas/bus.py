from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BusBase(BaseModel):
    """Common bus fields shared by create and response schemas."""

    model_config = ConfigDict(str_strip_whitespace=True)

    bus_number: str = Field(
        min_length=1,
        max_length=50,
    )

    registration_number: str = Field(
        min_length=1,
        max_length=50,
    )

    capacity: int = Field(gt=0)

    driver_id: int | None = Field(
        default=None,
        gt=0,
    )

    route_id: int | None = Field(
        default=None,
        gt=0,
    )


class BusCreate(BusBase):
    """Request schema for creating a bus."""

    pass


class BusUpdate(BaseModel):
    """
    Request schema for partially updating a bus.

    All fields are optional because PATCH updates only the
    fields supplied in the request.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    bus_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    registration_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    capacity: int | None = Field(
        default=None,
        gt=0,
    )

    driver_id: int | None = Field(
        default=None,
        gt=0,
    )

    route_id: int | None = Field(
        default=None,
        gt=0,
    )


class BusResponse(BusBase):
    """Response schema returned by Bus API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime