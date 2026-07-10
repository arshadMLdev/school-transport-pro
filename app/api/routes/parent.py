from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.parent import ParentCreate, ParentUpdate, ParentResponse
from app.services.parent_service import (
    get_parents,
    get_parent,
    create_parent,
    update_parent,
    delete_parent,
)

router = APIRouter(
    prefix="/parents",
    tags=["Parents"],
)


@router.get("/", response_model=list[ParentResponse])
def read_parents(db: Session = Depends(get_db)):
    return get_parents(db)


@router.get("/{parent_id}", response_model=ParentResponse)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    return get_parent(db, parent_id)


@router.post("/", response_model=ParentResponse)
def add_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    return create_parent(db, parent)


@router.put("/{parent_id}", response_model=ParentResponse)
def edit_parent(
    parent_id: int,
    parent: ParentUpdate,
    db: Session = Depends(get_db),
):
    return update_parent(db, parent_id, parent)


@router.delete("/{parent_id}")
def remove_parent(
    parent_id: int,
    db: Session = Depends(get_db),
):
    delete_parent(db, parent_id)

    return {"message": "Parent deleted successfully"}
