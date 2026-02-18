from pydantic import BaseModel
from datetime import date
from typing import Optional


class PMBase(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str
    interval: int = 1
    next_run_date: date
    asset_id: int


class PMCreate(PMBase):
    pass


class PMUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    interval: Optional[int] = None
    next_run_date: Optional[date] = None


class PMRead(PMBase):
    id: int
    last_run_date: Optional[date]

    class Config:
        from_attributes = True
