from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(Integer, primary_key=True, index=True)

    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)

    alert_type = Column(String(100), nullable=False)

    description = Column(String(500))

    alert_time = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip")

    driver = relationship("Driver")
