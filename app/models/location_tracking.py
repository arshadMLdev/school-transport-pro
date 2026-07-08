from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class LocationTracking(Base):
    __tablename__ = "location_tracking"

    id = Column(Integer, primary_key=True, index=True)

    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)

    latitude = Column(Float, nullable=False)

    longitude = Column(Float, nullable=False)

    speed = Column(Float, nullable=True)

    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip")
