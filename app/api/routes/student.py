from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.services.student_service import (
    get_students,
    get_student,
    create_student,
    update_student,
    delete_student
)

from app.api.deps import (
    get_current_admin,
    get_current_user
)

from app.models.user import User


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



@router.get(
    "/",
    response_model=list[StudentResponse]
)
def read_students(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_admin)
):

    return get_students(db)



@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def read_student(
    student_id:int,
    db:Session=Depends(get_db),
    user:User=Depends(get_current_user)
):

    return get_student(
        db,
        student_id
    )



@router.post(
    "/",
    response_model=StudentResponse
)
def add_student(
    student:StudentCreate,
    db:Session=Depends(get_db),
    user:User=Depends(get_current_admin)
):

    return create_student(
        db,
        student
    )



@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def edit_student(
    student_id:int,
    student:StudentUpdate,
    db:Session=Depends(get_db),
    user:User=Depends(get_current_admin)
):

    return update_student(
        db,
        student_id,
        student
    )



@router.delete(
    "/{student_id}"
)
def remove_student(
    student_id:int,
    db:Session=Depends(get_db),
    user:User=Depends(get_current_admin)
):

    delete_student(
        db,
        student_id
    )

    return {
        "message":
        "Student deleted successfully"
    }
