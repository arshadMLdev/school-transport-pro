from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RouteStop(Base):
    __tablename__ = "route_stops"

    id = Column(Integer, primary_key=True, index=True)

    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    stop_name = Column(String(100), nullable=False)

    stop_order = Column(Integer, nullable=False)

    latitude = Column(String(30))

    longitude = Column(String(30))

    route = relationship("Route", back_populates="stops")
