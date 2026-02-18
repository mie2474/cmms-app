from pydantic import BaseModel
from typing import Optional


class ProblemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class ProblemRead(ProblemBase):
    id: int

    class Config:
        from_attributes = True
