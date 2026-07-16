from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Bus(Base):
    __tablename__ = "buses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    bus_number = Column(
        String(50),
        unique=True,
        nullable=False
    )
    registration_number = Column(
        String(100),
        unique=True,
        nullable=False
    )
    capacity = Column(
        Integer,
        nullable=False
    )
    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )
    route_id = Column(
        Integer,
        ForeignKey("routes.id"),
        nullable=True
    )
    status = Column(
        String(20),
        default="ACTIVE"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    driver = relationship(
        "Driver",
        back_populates="buses"
    )
    route = relationship(
        "Route",
        back_populates="buses"
    )
