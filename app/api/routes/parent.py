from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.deps import (
    get_current_admin,
    get_current_user
)

from app.schemas.parent import (
    ParentCreate,
    ParentUpdate,
    ParentResponse
)

from app.services.parent_service import (
    create_parent,
    get_parents,
    get_parent,
    update_parent,
    delete_parent
)


router = APIRouter(
    prefix="/parents",
    tags=["Parents"]
)



# ============================
# Create Parent
# Admin Only
# ============================

@router.post(
    "/",
    response_model=ParentResponse
)
def add_parent(
    parent: ParentCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return create_parent(
        db,
        parent
    )



# ============================
# Get All Parents
# Admin Only
# ============================

@router.get(
    "/",
    response_model=list[ParentResponse]
)
def read_parents(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return get_parents(db)



# ============================
# Get Single Parent
# Admin OR Own Parent
# ============================

@router.get(
    "/{parent_id}",
    response_model=ParentResponse
)
def read_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_parent(
        db,
        parent_id
    )



# ============================
# Update Parent
# Admin Only
# ============================

@router.put(
    "/{parent_id}",
    response_model=ParentResponse
)
def edit_parent(
    parent_id: int,
    parent: ParentUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return update_parent(
        db,
        parent_id,
        parent
    )



# ============================
# Delete Parent
# Admin Only
# ============================

@router.delete(
    "/{parent_id}"
)
def remove_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return delete_parent(
        db,
        parent_id
    )
