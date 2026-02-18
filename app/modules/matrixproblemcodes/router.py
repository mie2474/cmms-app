from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles

from . import service, schemas

router = APIRouter(prefix="/matrixproblemcodes", tags=["Matrix Problem Codes"])


@router.post("/", response_model=schemas.MatrixRead)
def create_mapping(
    payload: schemas.MatrixCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    return service.create_mapping(db, payload)


@router.get("/", response_model=list[schemas.MatrixRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.list_all(db)


@router.get("/location/{location_id}", response_model=list[schemas.MatrixRead])
def get_for_location(
    location_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.get_problem_codes_for_location(db, location_id)
