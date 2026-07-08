from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    license_number = Column(String(50), unique=True, nullable=False)

    experience_years = Column(Integer, default=0)

    address = Column(String(255))

    emergency_contact = Column(String(20))

    user = relationship("User")
