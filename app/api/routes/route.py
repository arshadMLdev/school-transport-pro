from collections.abc import Sequence

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_admin,
    get_current_user,
)
from app.db.session import get_db
from app.models.route import Route
from app.models.user import User
from app.schemas.route import (
    RouteCreate,
    RouteResponse,
    RouteUpdate,
)
from app.services import route_service


router = APIRouter(
    prefix="/routes",
    tags=["Routes"],
)


@router.post(
    "/",
    response_model=RouteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_route(
    route_data: RouteCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Route:
    """
    Create a route.
    Access:
        ADMIN only.
    """
    return route_service.create_route(
        db=db,
        route_data=route_data,
    )


@router.get(
    "/",
    response_model=list[RouteResponse],
)
def get_routes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Sequence[Route]:
    """
    Return all routes.
    Access:
        ADMIN only.
    """
    return route_service.get_routes(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{route_id}",
    response_model=RouteResponse,
)
def get_route(
    route_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Route:
    """
    Return one route.
    Access:
        Authenticated users.
    """
    return route_service.get_route(
        db=db,
        route_id=route_id,
    )


@router.put(
    "/{route_id}",
    response_model=RouteResponse,
)
def update_route(
    route_data: RouteUpdate,
    route_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Route:
    """
    Update a route.
    Access:
        ADMIN only.
    """
    return route_service.update_route(
        db=db,
        route_id=route_id,
        route_data=route_data,
    )


@router.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_route(
    route_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Response:
    """
    Delete a route.
    Access:
        ADMIN only.
    """
    route_service.delete_route(
        db=db,
        route_id=route_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
