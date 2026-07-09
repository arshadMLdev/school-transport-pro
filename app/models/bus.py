from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)

    bus_number = Column(String(30), unique=True, nullable=False)

    registration_number = Column(String(30), unique=True, nullable=False)

    capacity = Column(Integer, nullable=False)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)

    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    driver = relationship("Driver")

    route = relationship("Route", back_populates="buses")
