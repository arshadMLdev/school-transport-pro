from collections.abc import Sequence
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session
from app.api.deps import (
    get_current_admin,
    get_current_parent,
    get_current_user,
)
from app.db.session import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from app.services import student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Student:
    """
    Create a student.
    Access:
        ADMIN only.
    """
    return student_service.create_student(
        db=db,
        student_data=student_data,
    )


@router.get(
    "/",
    response_model=list[StudentResponse],
)
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Sequence[Student]:
    """
    Return all students using pagination.
    Access:
        ADMIN only.
    """
    return student_service.get_students(
        db=db,
        skip=skip,
        limit=limit,
    )


# Keep this route above /{student_id}.
@router.get(
    "/my-children",
    response_model=list[StudentResponse],
)
def get_my_children(
    db: Session = Depends(get_db),
    current_parent: User = Depends(get_current_parent),
) -> Sequence[Student]:
    """
    Return children belonging to the authenticated parent.
    Access:
        PARENT only.
    """
    return student_service.get_students_for_parent_user(
        db=db,
        user_id=current_parent.id,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(
    student_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Student:
    """
    Return one student.
    Access:
        ADMIN: Any student.
        PARENT: Own child only.
        DRIVER: Denied.
    """
    return student_service.get_student_for_user(
        db=db,
        student_id=student_id,
        current_user=current_user,
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_data: StudentUpdate,
    student_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Student:
    """
    Update a student.
    Access:
        ADMIN only.
    """
    return student_service.update_student(
        db=db,
        student_id=student_id,
        student_data=student_data,
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_student(
    student_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
) -> Response:
    """
    Delete a student.
    Access:
        ADMIN only.
    """
    student_service.delete_student(
        db=db,
        student_id=student_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
