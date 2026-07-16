from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.parent import Parent
from app.models.user import User

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
)



def get_students(db: Session):
    """
    Return all students.
    Admin only access.
    """

    return (
        db.query(Student)
        .all()
    )



def get_student(
    db: Session,
    student_id: int
):
    """
    Get single student by ID.
    """

    student = (
        db.query(Student)
        .filter(
            Student.id == student_id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student



def get_student_for_user(
    db: Session,
    student_id: int,
    user: User
):
    """
    Authorization check.

    ADMIN:
        Can access all students.

    PARENT:
        Can access only own children.
    """

    student = get_student(
        db,
        student_id
    )


    if user.role == "ADMIN":
        return student


    if user.role == "PARENT":

        if student.parent.user_id != user.id:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return student


    raise HTTPException(
        status_code=403,
        detail="Access denied"
    )



def create_student(
    db: Session,
    student_data: StudentCreate
):
    """
    Create new student.
    """

    # Validate parent exists

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


    # Check duplicate admission number

    existing_student = (
        db.query(Student)
        .filter(
            Student.admission_number ==
            student_data.admission_number
        )
        .first()
    )


    if existing_student:

        raise HTTPException(
            status_code=400,
            detail="Admission number already exists"
        )


    student = Student(
        **student_data.model_dump()
    )


    try:

        db.add(student)

        db.commit()

        db.refresh(student)


    except Exception:

        db.rollback()

        raise


    return student



def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate
):
    """
    Partial student update.
    """

    student = get_student(
        db,
        student_id
    )


    data = (
        student_data
        .model_dump(
            exclude_unset=True
        )
    )


    # Check duplicate admission number

    if "admission_number" in data:

        existing_student = (
            db.query(Student)
            .filter(
                Student.admission_number ==
                data["admission_number"],
                Student.id != student_id
            )
            .first()
        )


        if existing_student:

            raise HTTPException(
                status_code=400,
                detail="Admission number already exists"
            )



    # Validate new parent

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


    for key, value in data.items():

        setattr(
            student,
            key,
            value
        )


    try:

        db.commit()

        db.refresh(student)


    except Exception:

        db.rollback()

        raise


    return student



def delete_student(
    db: Session,
    student_id: int
):
    """
    Delete student.
    """

    student = get_student(
        db,
        student_id
    )


    try:

        db.delete(student)

        db.commit()


    except Exception:

        db.rollback()

        raise


    return {
        "message": "Student deleted successfully"
    }



def get_parent_students(
    db: Session,
    parent_id: int
):
    """
    Return students belonging to a parent.
    """

    return (
        db.query(Student)
        .filter(
            Student.parent_id == parent_id
        )
        .all()
    )
