from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.route import Route
from app.schemas.route import RouteCreate, RouteUpdate


ROUTE_NUMBER_CONSTRAINTS = {
    "routes_route_number_key",
}


def _get_route_or_404(
    db: Session,
    route_id: int,
) -> Route:
    """
    Return a route or raise 404.
    """

    route = db.scalar(
        select(Route).where(Route.id == route_id)
    )

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    return route


def _ensure_route_number_unique(
    db: Session,
    route_number: str,
    exclude_route_id: int | None = None,
) -> None:
    """
    Ensure route number is unique.
    """

    statement = select(Route.id).where(
        Route.route_number == route_number
    )

    if exclude_route_id is not None:
        statement = statement.where(
            Route.id != exclude_route_id
        )

    existing_id = db.scalar(statement)

    if existing_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Route number already exists",
        )


def create_route(
    db: Session,
    route_data: RouteCreate,
) -> Route:
    """
    Create a new route.
    """

    _ensure_route_number_unique(
        db=db,
        route_number=route_data.route_number,
    )

    route = Route(
        **route_data.model_dump()
    )

    db.add(route)

    try:
        db.commit()
        db.refresh(route)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Route data conflicts with existing record",
        ) from exc

    return route


def get_route(
    db: Session,
    route_id: int,
) -> Route:
    """
    Return one route.
    """

    return _get_route_or_404(
        db=db,
        route_id=route_id,
    )


def get_routes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Route]:
    """
    Return routes with pagination.
    """

    statement = (
        select(Route)
        .order_by(Route.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_route(
    db: Session,
    route_id: int,
    route_data: RouteUpdate,
) -> Route:
    """
    Update a route.
    """

    route = _get_route_or_404(
        db=db,
        route_id=route_id,
    )

    update_data = route_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    new_route_number = update_data.get(
        "route_number"
    )

    if (
        new_route_number is not None
        and new_route_number != route.route_number
    ):
        _ensure_route_number_unique(
            db=db,
            route_number=new_route_number,
            exclude_route_id=route.id,
        )

    for field_name, field_value in update_data.items():
        setattr(route, field_name, field_value)

    db.commit()
    db.refresh(route)

    return route


def delete_route(
    db: Session,
    route_id: int,
) -> None:
    """
    Delete a route.
    """

    route = _get_route_or_404(
        db=db,
        route_id=route_id,
    )

    db.delete(route)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Route cannot be deleted because "
                "related records exist"
            ),
        ) from exc
