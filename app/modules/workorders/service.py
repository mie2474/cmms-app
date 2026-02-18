
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from .models import WorkOrder


VALID_TRANSITIONS = {
    "open": ["in_progress"],
    "in_progress": ["closed"],
    "closed": [],
}


def create_workorder(db: Session, data, user_id: int):
    wo = WorkOrder(**data.dict(), created_by=user_id)
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return wo


def assign_workorder(db: Session, wo_id: int, technician_id: int):
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(404, "Work order not found")

    wo.assigned_to = technician_id
    db.commit()
    db.refresh(wo)
    return wo


def change_status(db: Session, wo_id: int, new_status: str):
    wo = db.get(WorkOrder, wo_id)
    if not wo:
        raise HTTPException(404, "Work order not found")

    if new_status not in VALID_TRANSITIONS.get(wo.status, []):
        raise HTTPException(400, "Invalid status transition")

    # closing logic
    if new_status == "closed":
        if not wo.assigned_to:
            raise HTTPException(400, "Cannot close unassigned work order")
        wo.closed_at = datetime.utcnow()

    wo.status = new_status
    db.commit()
    db.refresh(wo)
    return wo


from sqlalchemy.orm import joinedload


def list_workorders(db: Session):
    return (
        db.query(WorkOrder)
        .options(
            joinedload(WorkOrder.asset),
            joinedload(WorkOrder.priority),
            joinedload(WorkOrder.problem_code),
        )
        .all()
    )
