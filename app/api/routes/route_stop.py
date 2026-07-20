from collections.abc import Sequence

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_admin,
    get_db,
)
from app.schemas.route_stop import (
    RouteStopCreate,
    RouteStopResponse,
    RouteStopUpdate,
)
from app.services import route_stop_service


router = APIRouter(
    prefix="/route-stops",
    tags=["Route Stops"],
)


@router.post(
    "/",
    response_model=RouteStopResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_route_stop(
    stop_data: RouteStopCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
) -> RouteStopResponse:
    """
    Create a new route stop.
    """

    return route_stop_service.create_route_stop(
        db=db,
        stop_data=stop_data,
    )


@router.get(
    "/",
    response_model=Sequence[RouteStopResponse],
)
def get_route_stops(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
) -> Sequence[RouteStopResponse]:
    """
    Return all route stops.
    """

    return route_stop_service.get_route_stops(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{stop_id}",
    response_model=RouteStopResponse,
)
def get_route_stop(
    stop_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
) -> RouteStopResponse:
    """
    Return one route stop.
    """

    return route_stop_service.get_route_stop(
        db=db,
        stop_id=stop_id,
    )


@router.put(
    "/{stop_id}",
    response_model=RouteStopResponse,
)
def update_route_stop(
    stop_id: int,
    stop_data: RouteStopUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
) -> RouteStopResponse:
    """
    Update a route stop.
    """

    return route_stop_service.update_route_stop(
        db=db,
        stop_id=stop_id,
        stop_data=stop_data,
    )


@router.delete(
    "/{stop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_route_stop(
    stop_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
) -> Response:
    """
    Delete a route stop.
    """

    route_stop_service.delete_route_stop(
        db=db,
        stop_id=stop_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
