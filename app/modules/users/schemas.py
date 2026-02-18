from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
