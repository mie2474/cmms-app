from pydantic import BaseModel
from typing import Optional


class PriorityBase(BaseModel):
    name: str
    description: Optional[str] = None


class PriorityCreate(PriorityBase):
    pass


class PriorityRead(PriorityBase):
    id: int

    class Config:
        from_attributes = True
