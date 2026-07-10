from pydantic import BaseModel


class ParentBase(BaseModel):
    user_id: int
    address: str
    emergency_contact: str
    relationship_to_student: str


class ParentCreate(ParentBase):
    pass


class ParentUpdate(ParentBase):
    pass


class ParentResponse(ParentBase):
    id: int

    class Config:
        from_attributes = True
