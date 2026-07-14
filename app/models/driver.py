from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    license_number = Column(String(100), unique=True, nullable=False)
    
    experience_years = Column(Integer, nullable=True)
    
    emergency_contact = Column(String(20), nullable=True)

    license_expiry = Column(Date, nullable=True)

    address = Column(String(255), nullable=True)

    status = Column(String(20), default="ACTIVE")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="driver"
    )
