from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.middleware.rbac import require_roles
from . import service, schemas

router = APIRouter(prefix="/prioritycodes", tags=["Priority Codes"])


@router.post("/", response_model=schemas.PriorityRead)
def create(
    payload: schemas.PriorityCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    return service.create_priority(db, payload)


@router.get("/", response_model=list[schemas.PriorityRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.list_priorities(db)
