from sqlalchemy.orm import Session

from app.models.parent import Parent
from app.schemas.parent import ParentCreate, ParentUpdate


def get_parents(db: Session):
    return db.query(Parent).all()


def get_parent(db: Session, parent_id: int):
    return db.query(Parent).filter(Parent.id == parent_id).first()


def create_parent(db: Session, parent: ParentCreate):
    db_parent = Parent(**parent.model_dump())

    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)

    return db_parent


def update_parent(db: Session, parent_id: int, parent_data: ParentUpdate):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()

    if not parent:
        return None

    for key, value in parent_data.model_dump().items():
        setattr(parent, key, value)

    db.commit()
    db.refresh(parent)

    return parent


def delete_parent(db: Session, parent_id: int):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()

    if not parent:
        return None

    db.delete(parent)
    db.commit()

    return parent
