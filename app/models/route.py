from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)

    route_name = Column(String(100), nullable=False)
    route_number = Column(String(50), unique=True, nullable=False)

    start_point = Column(String(255), nullable=False)
    end_point = Column(String(255), nullable=False)

    estimated_duration = Column(Integer)

    status = Column(String(20), default="ACTIVE")

    driver_id = Column(Integer, ForeignKey("drivers.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    buses = relationship(
        "Bus",
        back_populates="route"
    )

    stops = relationship(
        "RouteStop",
        back_populates="route"
    )

    driver = relationship(
        "Driver"
    )
