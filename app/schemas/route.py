from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RouteBase(BaseModel):
    """Common route fields shared by create and response schemas."""

    model_config = ConfigDict(str_strip_whitespace=True)

    route_name: str = Field(
        min_length=2,
        max_length=100,
    )

    route_number: str = Field(
        min_length=1,
        max_length=50,
    )

    start_point: str = Field(
        min_length=2,
        max_length=255,
    )

    end_point: str = Field(
        min_length=2,
        max_length=255,
    )

    estimated_duration: int | None = Field(
        default=None,
        gt=0,
    )

    status: str = Field(
        default="ACTIVE",
        max_length=20,
    )


    driver_id: int | None = Field(
        default=None,
        gt=0,
    )


class RouteCreate(RouteBase):
    """Request schema for creating a route."""

    pass


class RouteUpdate(BaseModel):
    """Request schema for partially updating a route."""

    model_config = ConfigDict(str_strip_whitespace=True)

    route_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    route_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    start_point: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    end_point: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    estimated_duration: int | None = Field(
        default=None,
        gt=0,
    )

    status: str | None = Field(
        default=None,
        max_length=20,
    )


    driver_id: int | None = Field(
        default=None,
        gt=0,
    )


class RouteResponse(RouteBase):
    """Response schema returned by Route API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
