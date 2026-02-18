# from fastapi import APIRouter, Depends, Request
# from sqlalchemy.orm import Session
# from app.config.db import get_db
# from app.middleware.auth import authenticate
# from . import service, schemas

# router = APIRouter(prefix="/workorders")


# @router.post("/", response_model=schemas.WorkOrderOut)
# async def create_work_order(
#     data: schemas.WorkOrderCreate,
#     request: Request,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     user = request.state.user
#     return service.create_work_order(db, data, user_email=user["email"])


# @router.get("/", response_model=list[schemas.WorkOrderOut])
# async def list_work_orders(
#     mine: bool = False,
#     request: Request = None,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     created_by = None
#     if mine and request is not None:
#         created_by = request.state.user["email"]
#     return service.list_work_orders(db, created_by=created_by)


# @router.get("/{wo_id}", response_model=schemas.WorkOrderOut)
# async def get_work_order(
#     wo_id: str,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.get_work_order(db, wo_id)


# @router.patch("/{wo_id}", response_model=schemas.WorkOrderOut)
# async def update_work_order(
#     wo_id: str,
#     data: schemas.WorkOrderUpdate,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.update_work_order(db, wo_id, data)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles

from . import service, schemas

router = APIRouter(prefix="/workorders", tags=["WorkOrders"])


@router.post("/", response_model=schemas.WorkOrderRead)
def create_workorder(
    payload: schemas.WorkOrderCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.create_workorder(db, payload, user_id=user["id"])


@router.patch("/{wo_id}/assign")
def assign_workorder(
    wo_id: int,
    technician_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.assign_workorder(db, wo_id, technician_id)


@router.patch("/{wo_id}/status")
def update_status(
    wo_id: int,
    payload: schemas.WorkOrderStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.change_status(db, wo_id, payload.status)


@router.get("/", response_model=list[schemas.WorkOrderRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.list_workorders(db)
