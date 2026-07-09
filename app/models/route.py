from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)

    route_name = Column(String(100), unique=True, nullable=False)

    source = Column(String(100), nullable=False)

    destination = Column(String(100), nullable=False)

    distance_km = Column(Integer)

    stops = relationship("RouteStop", back_populates="route")
    buses = relationship("Bus", back_populates="route")
