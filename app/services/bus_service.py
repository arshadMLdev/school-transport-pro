from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.bus import Bus
from app.models.driver import Driver
from app.schemas.bus import BusCreate, BusUpdate


REGISTRATION_NUMBER_CONSTRAINTS = {
    "buses_registration_number_key",
    "uq_buses_registration_number",
}


def _get_constraint_name(exc: IntegrityError) -> str | None:
    """
    Extract the PostgreSQL constraint name from an IntegrityError.
    """
    original_error = exc.orig
    diagnostic = getattr(original_error, "diag", None)

    if diagnostic is None:
        return None

    return getattr(diagnostic, "constraint_name", None)


def _get_bus_or_404(
    db: Session,
    bus_id: int,
) -> Bus:
    """
    Return a bus or raise a 404 error.
    """
    bus = db.scalar(
        select(Bus).where(Bus.id == bus_id)
    )

    if bus is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found",
        )

    return bus


def _get_driver_or_404(
    db: Session,
    driver_id: int,
) -> Driver:
    """
    Return a driver or raise a 404 error.
    """
    driver = db.scalar(
        select(Driver).where(Driver.id == driver_id)
    )

    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found",
        )

    return driver


def _ensure_registration_number_is_unique(
    db: Session,
    registration_number: str,
    exclude_bus_id: int | None = None,
) -> None:
    """
    Ensure the registration number is unique.
    """
    statement = select(Bus.id).where(
        Bus.registration_number == registration_number
    )

    if exclude_bus_id is not None:
        statement = statement.where(
            Bus.id != exclude_bus_id
        )

    existing_bus = db.scalar(statement)

    if existing_bus is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration number already exists",
        )


def _ensure_driver_has_no_active_bus(
    db: Session,
    driver_id: int,
    exclude_bus_id: int | None = None,
) -> None:
    """
    Ensure the driver is not already assigned to another bus.
    """
    statement = select(Bus.id).where(
        Bus.driver_id == driver_id
    )

    if exclude_bus_id is not None:
        statement = statement.where(
            Bus.id != exclude_bus_id
        )

    existing_bus = db.scalar(statement)

    if existing_bus is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Driver is already assigned to another bus",
        )


def create_bus(
    db: Session,
    bus_data: BusCreate,
) -> Bus:
    """
    Create a new bus.

    Validations:
    - Registration number must be unique.
    - Driver must exist if supplied.
    - Driver cannot already be assigned to another bus.
    """

    _ensure_registration_number_is_unique(
        db=db,
        registration_number=bus_data.registration_number,
    )

    if bus_data.driver_id is not None:
        _get_driver_or_404(
            db=db,
            driver_id=bus_data.driver_id,
        )

        _ensure_driver_has_no_active_bus(
            db=db,
            driver_id=bus_data.driver_id,
        )

    bus = Bus(
        **bus_data.model_dump()
    )

    db.add(bus)

    try:
        db.commit()
        db.refresh(bus)

    except IntegrityError as exc:
        db.rollback()

        constraint_name = _get_constraint_name(exc)

        if constraint_name in REGISTRATION_NUMBER_CONSTRAINTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Registration number already exists",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus data conflicts with an existing record",
        ) from exc

    return bus
def get_bus(
    db: Session,
    bus_id: int,
) -> Bus:
    """
    Return one bus by ID.
    """
    return _get_bus_or_404(
        db=db,
        bus_id=bus_id,
    )


def get_buses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Bus]:
    """
    Return a paginated list of buses.
    """
    statement = (
        select(Bus)
        .order_by(Bus.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_bus(
    db: Session,
    bus_id: int,
    bus_data: BusUpdate,
) -> Bus:
    """
    Partially update a bus.
    """
    bus = _get_bus_or_404(
        db=db,
        bus_id=bus_id,
    )

    update_data = bus_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    required_fields = {
        "bus_number",
        "registration_number",
        "capacity",
    }

    null_required_fields = sorted(
        field_name
        for field_name in required_fields
        if field_name in update_data
        and update_data[field_name] is None
    )

    if null_required_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "These fields cannot be null: "
                + ", ".join(null_required_fields)
            ),
        )

    new_registration_number = update_data.get(
        "registration_number"
    )

    if (
        new_registration_number is not None
        and new_registration_number
        != bus.registration_number
    ):
        _ensure_registration_number_is_unique(
            db=db,
            registration_number=new_registration_number,
            exclude_bus_id=bus.id,
        )

    if "driver_id" in update_data:

        new_driver_id = update_data["driver_id"]

        if new_driver_id is not None:

            if new_driver_id != bus.driver_id:

                _get_driver_or_404(
                    db=db,
                    driver_id=new_driver_id,
                )

                _ensure_driver_has_no_active_bus(
                    db=db,
                    driver_id=new_driver_id,
                    exclude_bus_id=bus.id,
                )

    for field_name, field_value in update_data.items():
        setattr(
            bus,
            field_name,
            field_value,
        )

    try:
        db.commit()
        db.refresh(bus)

    except IntegrityError as exc:
        db.rollback()

        constraint_name = _get_constraint_name(exc)

        if constraint_name in REGISTRATION_NUMBER_CONSTRAINTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Registration number already exists",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bus data conflicts with an existing record",
        ) from exc

    return bus


def delete_bus(
    db: Session,
    bus_id: int,
) -> None:
    """
    Delete a bus.
    """
    bus = _get_bus_or_404(
        db=db,
        bus_id=bus_id,
    )

    db.delete(bus)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Bus cannot be deleted because related "
                "records exist"
            ),
        ) from exc