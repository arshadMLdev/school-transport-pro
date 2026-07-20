from pydantic import BaseModel, ConfigDict, Field


class RouteStopBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    route_id: int = Field(gt=0)

    stop_name: str = Field(
        min_length=2,
        max_length=100,
    )

    stop_order: int = Field(gt=0)

    latitude: str | None = Field(
        default=None,
        max_length=30,
    )

    longitude: str | None = Field(
        default=None,
        max_length=30,
    )


class RouteStopCreate(RouteStopBase):
    pass


class RouteStopUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    route_id: int | None = Field(
        default=None,
        gt=0,
    )

    stop_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    stop_order: int | None = Field(
        default=None,
        gt=0,
    )

    latitude: str | None = Field(
        default=None,
        max_length=30,
    )

    longitude: str | None = Field(
        default=None,
        max_length=30,
    )


class RouteStopResponse(RouteStopBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
