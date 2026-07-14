from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_admin, get_current_user
from app.schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverResponse,
)
from app.services.driver_service import (
    create_driver,
    get_drivers,
    get_driver_response,
    update_driver,
    delete_driver,
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.post("/", response_model=DriverResponse)
def create(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return create_driver(db, driver)


@router.get("/", response_model=list[DriverResponse])
def read_all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_drivers(db)


@router.get("/{driver_id}", response_model=DriverResponse)
def read(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_driver_response(db, driver_id)


@router.put("/{driver_id}", response_model=DriverResponse)
def update(
    driver_id: int,
    driver: DriverUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return update_driver(db, driver_id, driver)


@router.delete("/{driver_id}")
def delete(
    driver_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return delete_driver(db, driver_id)
