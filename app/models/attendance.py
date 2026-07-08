from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)

    pickup_status = Column(String(20), default="PENDING")

    drop_status = Column(String(20), default="PENDING")

    pickup_time = Column(DateTime(timezone=True), nullable=True)

    drop_time = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student")

    trip = relationship("Trip")
