from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.route import Route
from app.models.route_stop import RouteStop
from app.schemas.route_stop import (
    RouteStopCreate,
    RouteStopUpdate,
)

def _get_route_stop_or_404(
    db: Session,
    stop_id: int,
) -> RouteStop:
    """
    Return a route stop or raise 404.
    """

    route_stop = db.scalar(
        select(RouteStop).where(
            RouteStop.id == stop_id
        )
    )

    if route_stop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route stop not found",
        )

    return route_stop


def create_route_stop(
    db: Session,
    stop_data: RouteStopCreate,
) -> RouteStop:
    """
    Create a new route stop.
    """

    route = db.scalar(
        select(Route).where(
            Route.id == stop_data.route_id
        )
    )

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    route_stop = RouteStop(
        **stop_data.model_dump()
    )

    db.add(route_stop)

    try:
        db.commit()
        db.refresh(route_stop)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Route stop could not be created",
        ) from exc

    return route_stop


def get_route_stop(
    db: Session,
    stop_id: int,
) -> RouteStop:
    """
    Return one route stop.
    """

    return _get_route_stop_or_404(
        db=db,
        stop_id=stop_id,
    )


def get_route_stops(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[RouteStop]:
    """
    Return route stops with pagination.
    """

    statement = (
        select(RouteStop)
        .order_by(RouteStop.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_route_stop(
    db: Session,
    stop_id: int,
    stop_data: RouteStopUpdate,
) -> RouteStop:
    """
    Update a route stop.
    """

    route_stop = _get_route_stop_or_404(
        db=db,
        stop_id=stop_id,
    )

    update_data = stop_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    if "route_id" in update_data:
        route = db.scalar(
            select(Route).where(
                Route.id == update_data["route_id"]
            )
        )

        if route is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found",
            )

    for field_name, field_value in update_data.items():
        setattr(route_stop, field_name, field_value)

    db.commit()
    db.refresh(route_stop)

    return route_stop


def delete_route_stop(
    db: Session,
    stop_id: int,
) -> None:
    """
    Delete a route stop.
    """

    route_stop = _get_route_stop_or_404(
        db=db,
        stop_id=stop_id,
    )

    db.delete(route_stop)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Route stop cannot be deleted because "
                "related records exist"
            ),
        ) from exc
