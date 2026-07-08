from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import (
    User,
    Parent,
    Driver,
    Student,
    Route,
    RouteStop,
    Bus,
    Trip,
    Attendance,
    LocationTracking,
    Notification,
    EmergencyAlert,
)