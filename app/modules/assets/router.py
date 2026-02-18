# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.config.db import get_db
# from app.middleware.auth import authenticate
# from . import service, schemas

# router = APIRouter(prefix="/assets")


# @router.post("/", response_model=schemas.AssetOut)
# async def create_asset(
#     data: schemas.AssetCreate,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.create_asset(db, data)


# @router.get("/", response_model=list[schemas.AssetOut])
# async def list_assets(
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.list_assets(db)


# @router.get("/{asset_id}", response_model=schemas.AssetOut)
# async def get_asset(
#     asset_id: str,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.get_asset(db, asset_id)


# @router.patch("/{asset_id}", response_model=schemas.AssetOut)
# async def update_asset(
#     asset_id: str,
#     data: schemas.AssetUpdate,
#     db: Session = Depends(get_db),
#     _=Depends(authenticate),
# ):
#     return service.update_asset(db, asset_id, data)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles

from . import service, schemas

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/", response_model=schemas.AssetRead)
def create_asset(
    payload: schemas.AssetCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.create_asset(db, payload)


@router.patch("/{asset_id}", response_model=schemas.AssetRead)
def update_asset(
    asset_id: int,
    payload: schemas.AssetUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor")),
):
    return service.update_asset(db, asset_id, payload)


@router.get("/{asset_id}", response_model=schemas.AssetRead)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.get_asset(db, asset_id)


@router.get("/", response_model=list[schemas.AssetRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.list_assets(db)
