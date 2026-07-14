from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Parent(Base):

    __tablename__ = "parents"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )


    address = Column(
        String(255)
    )


    emergency_contact = Column(
        String(20)
    )


    relationship_to_student = Column(
        String(50)
    )


    # User relationship
    user = relationship(
        "User",
        back_populates="parent"
    )


    # Student relationship
    students = relationship(
        "Student",
        back_populates="parent"
    )
