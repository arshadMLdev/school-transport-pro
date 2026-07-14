from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Student(Base):

    __tablename__ = "students"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    full_name = Column(
        String(100),
        nullable=False
    )


    admission_number = Column(
        String(50),
        unique=True,
        nullable=False
    )


    grade = Column(
        String(20),
        nullable=False
    )


    section = Column(
        String(10),
        nullable=True
    )


    gender = Column(
        String(10),
        nullable=True
    )


    date_of_birth = Column(
        Date,
        nullable=True
    )


    address = Column(
        String(255),
        nullable=True
    )


    parent_id = Column(
        Integer,
        ForeignKey(
            "parents.id",
            ondelete="RESTRICT"
        ),
        nullable=False
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


    parent = relationship(
        "Parent",
        back_populates="students"
    )
