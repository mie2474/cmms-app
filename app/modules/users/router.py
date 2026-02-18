from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles
from . import service, schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserRead)
def create_user(
    payload: schemas.UserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    return service.create_user(db, payload)


@router.get("/", response_model=list[schemas.UserRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.list_users(db)
