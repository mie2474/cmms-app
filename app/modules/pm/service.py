from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import PreventiveMaintenance
from app.modules.workorders.models import WorkOrder


VALID_FREQUENCIES = ["daily", "weekly", "monthly"]


def create_pm(db: Session, data):
    if data.frequency not in VALID_FREQUENCIES:
        raise HTTPException(400, "Invalid frequency")

    pm = PreventiveMaintenance(**data.dict())
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm


def get_due_pms(db: Session):
    today = date.today()
    return db.query(PreventiveMaintenance).filter(
        PreventiveMaintenance.next_run_date <= today
    ).all()


def generate_workorder_from_pm(db: Session, pm: PreventiveMaintenance):
    """
    Core CMMS automation:
    Creates a work order when PM becomes due.
    """

    workorder = WorkOrder(
        title=f"PM: {pm.title}",
        description=pm.description,
        asset_id=pm.asset_id,
        status="open",
        priority="medium",
    )

    db.add(workorder)

    # update PM schedule
    pm.last_run_date = date.today()

    if pm.frequency == "daily":
        pm.next_run_date = pm.last_run_date + timedelta(days=pm.interval)

    elif pm.frequency == "weekly":
        pm.next_run_date = pm.last_run_date + timedelta(weeks=pm.interval)

    elif pm.frequency == "monthly":
        pm.next_run_date = pm.last_run_date + timedelta(days=30 * pm.interval)

    db.commit()
