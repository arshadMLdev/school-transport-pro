from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import hash_password

from app.models.user import User
from app.models.parent import Parent
from app.models.student import Student

from app.schemas.parent import (
    ParentCreate,
    ParentUpdate
)


def _parent_to_response(parent: Parent) -> dict:
    """
    Convert Parent ORM object into API response format.

    Parent table contains parent-specific data.
    User table contains login-related data.

    This function combines both.
    """

    return {
        "id": parent.id,

        # User information
        "full_name": parent.user.full_name,
        "email": parent.user.email,
        "mobile": parent.user.mobile,

        # Parent information
        "address": parent.address,
        "emergency_contact": parent.emergency_contact,
        "relationship_to_student": parent.relationship_to_student,

        # User status
        "status": parent.user.status,
    }



def create_parent(
    db: Session,
    parent_data: ParentCreate
):
    """
    Creates:
    
    User
      |
      |
    Parent profile

    Flow:

    1. Check duplicate email
    2. Check duplicate mobile
    3. Create User account
    4. Hash password
    5. Assign role=PARENT
    6. Create Parent record
    7. Return response
    """


    # Check email already exists

    existing_user = (
        db.query(User)
        .filter(
            User.email == parent_data.email
        )
        .first()
    )


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    # Check mobile already exists

    existing_mobile = (
        db.query(User)
        .filter(
            User.mobile == parent_data.mobile
        )
        .first()
    )


    if existing_mobile:
        raise HTTPException(
            status_code=400,
            detail="Mobile number already exists"
        )


    # Create User account

    db_user = User(
        full_name=parent_data.full_name,
        email=parent_data.email,
        mobile=parent_data.mobile,

        password_hash=hash_password(
            parent_data.password
        ),

        role="PARENT",
        status="ACTIVE"
    )


    db.add(db_user)

    # Generates user id before creating Parent
    db.flush()



    # Create Parent profile

    db_parent = Parent(
        user_id=db_user.id,

        address=parent_data.address,

        emergency_contact=
            parent_data.emergency_contact,

        relationship_to_student=
            parent_data.relationship_to_student
    )


    db.add(db_parent)

    db.commit()


    db.refresh(db_parent)


    return _parent_to_response(db_parent)





def get_parents(
    db: Session
):

    """
    Return all parents.
    """

    parents = (
        db.query(Parent)
        .all()
    )


    return [
        _parent_to_response(parent)
        for parent in parents
    ]





def get_parent(
    db: Session,
    parent_id: int
):

    """
    Return single parent.
    """

    parent = (
        db.query(Parent)
        .filter(
            Parent.id == parent_id
        )
        .first()
    )


    if not parent:

        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )


    return _parent_to_response(parent)





def update_parent(
    db: Session,
    parent_id: int,
    parent_data: ParentUpdate
):

    """
    Update:

    User fields:
        full_name
        email
        mobile


    Parent fields:
        address
        emergency_contact
        relationship_to_student
        status
    """


    parent = (
        db.query(Parent)
        .filter(
            Parent.id == parent_id
        )
        .first()
    )


    if not parent:

        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )


    update_data = (
        parent_data
        .model_dump(
            exclude_unset=True
        )
    )


    user_fields = {
        "full_name",
        "email",
        "mobile"
    }



    for key, value in update_data.items():


        if key in user_fields:

            setattr(
                parent.user,
                key,
                value
            )

        else:

            setattr(
                parent,
                key,
                value
            )


    db.commit()


    db.refresh(parent)


    return _parent_to_response(parent)





def delete_parent(
    db: Session,
    parent_id: int
):

    """
    Delete parent safely.

    Rule:

    If parent has students:
        Block deletion.

    Otherwise:
        Delete User.
        Cascade deletes Parent.
    """


    parent = (
        db.query(Parent)
        .filter(
            Parent.id == parent_id
        )
        .first()
    )


    if not parent:

        raise HTTPException(
            status_code=404,
            detail="Parent not found"
        )



    student_count = (
        db.query(Student)
        .filter(
            Student.parent_id == parent_id
        )
        .count()
    )


    if student_count > 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete parent with existing "
                "student records. Remove students first."
            )
        )



    # Delete User
    #
    # Because User model has:
    #
    # cascade="all, delete-orphan"
    #
    # Parent record will also be removed.

    db.delete(parent.user)

    db.commit()


    return {
        "message": "Parent deleted successfully"
    }
