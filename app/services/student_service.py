from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.parent import Parent
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate
from app.models.route import Route

ADMISSION_NUMBER_CONSTRAINTS = {
    "students_admission_number_key",
    "uq_students_admission_number",
}


def _get_constraint_name(exc: IntegrityError) -> str | None:
    """
    Extract the PostgreSQL constraint name from an IntegrityError.

    This lets the service return a specific error instead of treating
    every database integrity failure as a duplicate admission number.
    """
    original_error = exc.orig
    diagnostic = getattr(original_error, "diag", None)

    if diagnostic is None:
        return None

    return getattr(diagnostic, "constraint_name", None)


def _get_parent_or_404(
    db: Session,
    parent_id: int,
) -> Parent:
    """
    Return a parent by Parent.id or raise a 404 error.
    """
    parent = db.scalar(
        select(Parent).where(Parent.id == parent_id)
    )

    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent not found",
        )

    return parent


def _get_parent_by_user_id_or_404(
    db: Session,
    user_id: int,
) -> Parent:
    """
    Return the Parent profile linked to an authenticated User.id.
    """
    parent = db.scalar(
        select(Parent).where(Parent.user_id == user_id)
    )

    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent profile not found",
        )

    return parent


def _get_student_or_404(
    db: Session,
    student_id: int,
) -> Student:
    """
    Return a student or raise a 404 error.
    """
    student = db.scalar(
        select(Student).where(Student.id == student_id)
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student


def _get_role_value(user: User) -> str:
    """
    Return the user's role as an uppercase string.

    Supports roles stored as plain strings or Python Enum values.
    """
    role = user.role

    if hasattr(role, "value"):
        return str(role.value).upper()

    return str(role).upper()


def _ensure_admission_number_is_unique(
    db: Session,
    admission_number: str,
    exclude_student_id: int | None = None,
) -> None:
    """
    Ensure that an admission number is not already in use.

    exclude_student_id prevents an existing student from conflicting
    with their own admission number during an update.
    """
    statement = select(Student.id).where(
        Student.admission_number == admission_number
    )

    if exclude_student_id is not None:
        statement = statement.where(
            Student.id != exclude_student_id
        )

    existing_student_id = db.scalar(statement)

    if existing_student_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admission number already exists",
        )


def create_student(
    db: Session,
    student_data: StudentCreate,
) -> Student:
    """
    Create a new student.

    Validations:
    - The parent must exist.
    - The admission number must be unique.
    """
    _get_parent_or_404(
        db=db,
        parent_id=student_data.parent_id,
    )

    _ensure_admission_number_is_unique(
        db=db,
        admission_number=student_data.admission_number,
    )

    if student_data.route_id is not None:
        route = db.scalar(
            select(Route).where(
                Route.id == student_data.route_id
            )
        )

        if route is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found",
            )

    student = Student(
        **student_data.model_dump()
    )

    db.add(student)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError as exc:
        db.rollback()

        constraint_name = _get_constraint_name(exc)

        if constraint_name in ADMISSION_NUMBER_CONSTRAINTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admission number already exists",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student data conflicts with an existing record",
        ) from exc

    return student


def get_student(
    db: Session,
    student_id: int,
) -> Student:
    """
    Return one student by ID.

    This function does not perform role or ownership checks. Use
    get_student_for_user() in routes accessible to parents.
    """
    return _get_student_or_404(
        db=db,
        student_id=student_id,
    )


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Student]:
    """
    Return a paginated list of all students.

    Intended for administrators.
    """
    statement = (
        select(Student)
        .order_by(Student.id)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def get_students_for_parent_user(
    db: Session,
    user_id: int,
) -> Sequence[Student]:
    """
    Return only students belonging to the authenticated parent user.

    user_id refers to users.id. It is first translated to the linked
    parents.id before querying students.parent_id.
    """
    parent = _get_parent_by_user_id_or_404(
        db=db,
        user_id=user_id,
    )

    statement = (
        select(Student)
        .where(Student.parent_id == parent.id)
        .order_by(Student.full_name)
    )

    return db.scalars(statement).all()


def get_student_for_user(
    db: Session,
    student_id: int,
    current_user: User,
) -> Student:
    """
    Return a student according to role and ownership.

    ADMIN:
        Can access any student.

    PARENT:
        Can access only their own child.

    DRIVER:
        Cannot access student profile endpoints.
    """
    role = _get_role_value(current_user)

    if role == "ADMIN":
        return _get_student_or_404(
            db=db,
            student_id=student_id,
        )

    if role == "PARENT":
        parent = _get_parent_by_user_id_or_404(
            db=db,
            user_id=current_user.id,
        )

        student = db.scalar(
            select(Student).where(
                Student.id == student_id,
                Student.parent_id == parent.id,
            )
        )

        if student is None:
            # Do not reveal whether another parent's student exists.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        return student

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to access student records",
    )


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate,
) -> Student:
    """
    Partially update a student.

    Only fields explicitly included in the PATCH request are changed.
    """
    student = _get_student_or_404(
        db=db,
        student_id=student_id,
    )

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    if "route_id" in update_data:
        route_id = update_data["route_id"]

        if route_id is not None:
            route = db.scalar(
                select(Route).where(
                    Route.id == route_id
                )
            )

            if route is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Route not found",
                )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    required_fields = {
        "full_name",
        "admission_number",
        "grade",
        "parent_id",
    }

    null_required_fields = sorted(
        field_name
        for field_name in required_fields
        if field_name in update_data
        and update_data[field_name] is None
    )

    if null_required_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "These fields cannot be null: "
                + ", ".join(null_required_fields)
            ),
        )

    new_parent_id = update_data.get("parent_id")

    if (
        new_parent_id is not None
        and new_parent_id != student.parent_id
    ):
        _get_parent_or_404(
            db=db,
            parent_id=new_parent_id,
        )

    new_admission_number = update_data.get(
        "admission_number"
    )

    if (
        new_admission_number is not None
        and new_admission_number
        != student.admission_number
    ):
        _ensure_admission_number_is_unique(
            db=db,
            admission_number=new_admission_number,
            exclude_student_id=student.id,
        )

    for field_name, field_value in update_data.items():
        setattr(student, field_name, field_value)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError as exc:
        db.rollback()

        constraint_name = _get_constraint_name(exc)

        if constraint_name in ADMISSION_NUMBER_CONSTRAINTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admission number already exists",
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student data conflicts with an existing record",
        ) from exc

    return student


def delete_student(
    db: Session,
    student_id: int,
) -> None:
    """
    Delete a student.

    Deletion is blocked when related database records, such as
    attendance records, still reference the student.
    """
    student = _get_student_or_404(
        db=db,
        student_id=student_id,
    )

    db.delete(student)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Student cannot be deleted because related "
                "records exist"
            ),
        ) from exc
