from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Nested Schemas
# -----------------------------

class AssetNested(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PriorityNested(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProblemCodeNested(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -----------------------------
# Base
# -----------------------------

class WorkOrderBase(BaseModel):
    title: str
    description: Optional[str] = None
    asset_id: int
    priority_id: int
    problem_code_id: int


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderStatusUpdate(BaseModel):
    status: str


# -----------------------------
# Read
# -----------------------------

class WorkOrderRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    asset: AssetNested
    priority: PriorityNested
    problem_code: ProblemCodeNested

    assigned_to: Optional[int]
    created_by: int
    created_at: datetime
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True
