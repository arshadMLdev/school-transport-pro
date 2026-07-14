from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.student import Student
from app.models.parent import Parent
from app.schemas.student import (
    StudentCreate,
    StudentUpdate
)


def get_students(db: Session):

    return db.query(Student).all()



def get_student(db: Session, student_id: int):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student



def create_student(
    db: Session,
    student_data: StudentCreate
):

    parent = (
        db.query(Parent)
        .filter(
            Parent.id == student_data.parent_id
        )
        .first()
    )

    if not parent:
        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )


    existing = (
        db.query(Student)
        .filter(
            Student.admission_number ==
            student_data.admission_number
        )
        .first()
    )


    if existing:
        raise HTTPException(
            status_code=400,
            detail="Admission number already exists"
        )


    student = Student(
        **student_data.model_dump()
    )


    db.add(student)
    db.commit()
    db.refresh(student)

    return student



def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):

    student = get_student(
        db,
        student_id
    )


    data = student_data.model_dump(
        exclude_unset=True
    )


    if "parent_id" in data:

        parent = (
            db.query(Parent)
            .filter(
                Parent.id == data["parent_id"]
            )
            .first()
        )

        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent not found"
            )


    for key,value in data.items():
        setattr(
            student,
            key,
            value
        )


    db.commit()
    db.refresh(student)

    return student



def delete_student(
    db: Session,
    student_id:int
):

    student = get_student(
        db,
        student_id
    )


    db.delete(student)
    db.commit()

    return student



def get_parent_students(
    db:Session,
    parent_id:int
):

    return (
        db.query(Student)
        .filter(
            Student.parent_id == parent_id
        )
        .all()
    )
