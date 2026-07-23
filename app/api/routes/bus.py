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

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.bus import Bus
from app.models.user import User
from app.schemas.bus import (
    BusCreate,
    BusResponse,
    BusUpdate,
)
from app.services import bus_service


router = APIRouter(
    prefix="/buses",
    tags=["Buses"],
)


@router.post(
    "/",
    response_model=BusResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bus(
    bus_data: BusCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Bus:
    """
    Create a bus.

    Access:
        ADMIN only.
    """
    return bus_service.create_bus(
        db=db,
        bus_data=bus_data,
    )


@router.get(
    "/",
    response_model=list[BusResponse],
)
def get_buses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Sequence[Bus]:
    """
    Return all buses using pagination.

    Access:
        ADMIN only.
    """
    return bus_service.get_buses(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{bus_id}",
    response_model=BusResponse,
)
def get_bus(
    bus_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Bus:
    """
    Return one bus.

    Access:
        ADMIN only.
    """
    return bus_service.get_bus(
        db=db,
        bus_id=bus_id,
    )


@router.patch(
    "/{bus_id}",
    response_model=BusResponse,
)
def update_bus(
    bus_data: BusUpdate,
    bus_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Bus:
    """
    Partially update a bus.

    Access:
        ADMIN only.
    """
    return bus_service.update_bus(
        db=db,
        bus_id=bus_id,
        bus_data=bus_data,
    )


@router.delete(
    "/{bus_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_bus(
    bus_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Response:
    """
    Delete a bus.

    Access:
        ADMIN only.
    """
    bus_service.delete_bus(
        db=db,
        bus_id=bus_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )