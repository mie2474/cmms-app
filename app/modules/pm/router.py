from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles

from . import service, schemas

router = APIRouter(prefix="/pm", tags=["Preventive Maintenance"])


@router.post("/", response_model=schemas.PMRead)
def create_pm(
    payload: schemas.PMCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.create_pm(db, payload)


@router.get("/due", response_model=list[schemas.PMRead])
def list_due(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.get_due_pms(db)
