from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)

    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    trip_date = Column(DateTime(timezone=True), server_default=func.now())

    trip_status = Column(String(20), default="NOT_STARTED")

    start_time = Column(DateTime(timezone=True), nullable=True)

    end_time = Column(DateTime(timezone=True), nullable=True)

    bus = relationship("Bus")

    driver = relationship("Driver")

    route = relationship("Route")
