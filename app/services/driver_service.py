from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import hash_password
from app.models.user import User
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate


def _driver_to_response(driver: Driver) -> dict:
    """Builds a flat response dict, pulling name/email/mobile from the linked User."""
    return {
        "id": driver.id,
        "full_name": driver.user.full_name,
        "email": driver.user.email,
        "mobile": driver.user.mobile,
        "license_number": driver.license_number,
        "license_expiry": driver.license_expiry,
        "experience_years": driver.experience_years,
        "address": driver.address,
        "emergency_contact": driver.emergency_contact,
        "status": driver.status,
    }


def create_driver(db: Session, driver: DriverCreate):

    # Check email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == driver.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    # Check mobile already exists
    existing_mobile = (
        db.query(User)
        .filter(User.mobile == driver.mobile)
        .first()
    )

    if existing_mobile:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already exists",
        )

    # Create User
    db_user = User(
        full_name=driver.full_name,
        email=driver.email,
        mobile=driver.mobile,
        password_hash=hash_password(driver.password),
        role="DRIVER",
        status="ACTIVE",
    )

    db.add(db_user)
    db.flush()      # Generates db_user.id

    # Create Driver
    db_driver = Driver(
        user_id=db_user.id,
        license_number=driver.license_number,
        license_expiry=driver.license_expiry,
        experience_years=driver.experience_years,
        address=driver.address,
        emergency_contact=driver.emergency_contact,
        status="ACTIVE",
    )

    db.add(db_driver)
    db.commit()

    db.refresh(db_user)
    db.refresh(db_driver)

    return _driver_to_response(db_driver)


def get_drivers(db: Session):
    drivers = db.query(Driver).all()
    return [_driver_to_response(d) for d in drivers]


def get_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver


def update_driver(db: Session, driver_id: int, driver_data: DriverUpdate):
    driver = get_driver(db, driver_id)  # raises 404 if missing, returns ORM object

    update_data = driver_data.model_dump(exclude_unset=True)

    # Fields that belong on User vs Driver
    user_fields = {"full_name", "email", "mobile"}

    for key, value in update_data.items():
        if key in user_fields:
            setattr(driver.user, key, value)
        else:
            setattr(driver, key, value)

    db.commit()
    db.refresh(driver)
    db.refresh(driver.user)

    return _driver_to_response(driver)


def delete_driver(db: Session, driver_id: int):
    driver = get_driver(db, driver_id)  # ORM object, raises 404 if missing

    # Delete the User — cascade="all, delete-orphan" on User.driver removes the Driver row too
    db.delete(driver.user)
    db.commit()

    return {"message": "Driver deleted successfully"}


def get_driver_response(db: Session, driver_id: int):
    """Public helper for routes: returns the flat response dict for a single driver."""
    driver = get_driver(db, driver_id)
    return _driver_to_response(driver)
