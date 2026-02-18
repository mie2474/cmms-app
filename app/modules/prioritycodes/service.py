from sqlalchemy.orm import Session
from .models import PriorityCode


def create_priority(db: Session, data):
    priority = PriorityCode(**data.dict())
    db.add(priority)
    db.commit()
    db.refresh(priority)
    return priority


def list_priorities(db: Session):
    return db.query(PriorityCode).all()
