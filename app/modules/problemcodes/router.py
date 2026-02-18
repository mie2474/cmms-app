from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.middleware.rbac import require_roles
from . import service, schemas

router = APIRouter(prefix="/problemcodes", tags=["Problem Codes"])


@router.post("/", response_model=schemas.ProblemRead)
def create(
    payload: schemas.ProblemCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.create_Problem(db, payload)


@router.get("/", response_model=list[schemas.ProblemRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.list_problem_codes(db)
