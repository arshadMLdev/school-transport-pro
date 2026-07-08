from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    admission_number = Column(String(50), unique=True, nullable=False)

    grade = Column(String(20), nullable=False)

    section = Column(String(10))

    gender = Column(String(10))

    date_of_birth = Column(Date)

    address = Column(String(255))

    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)

    parent = relationship("Parent")
