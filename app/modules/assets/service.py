# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from . import models, schemas


# def create_asset(db: Session, data: schemas.AssetCreate) -> models.Asset:
#     asset = models.Asset(**data.dict())
#     db.add(asset)
#     db.commit()
#     db.refresh(asset)
#     return asset


# def get_asset(db: Session, asset_id: str) -> models.Asset:
#     asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
#     if not asset:
#         raise HTTPException(status_code=404, detail="Asset not found")
#     return asset


# def list_assets(db: Session):
#     return db.query(models.Asset).all()


# def update_asset(
#     db: Session, asset_id: str, data: schemas.AssetUpdate
# ) -> models.Asset:
#     asset = get_asset(db, asset_id)
#     for field, value in data.dict(exclude_unset=True).items():
#         setattr(asset, field, value)
#     db.commit()
#     db.refresh(asset)
#     return asset

from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Asset


VALID_STATUS = ["active", "maintenance", "retired"]


def create_asset(db: Session, data):
    # unique asset tag enforcement
    if db.query(Asset).filter_by(asset_tag=data.asset_tag).first():
        raise HTTPException(400, "Asset tag already exists")

    asset = Asset(**data.dict())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def update_asset(db: Session, asset_id: int, data):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")

    if data.status and data.status not in VALID_STATUS:
        raise HTTPException(400, "Invalid asset status")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)
    return asset


def get_asset(db: Session, asset_id: int):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    return asset


def list_assets(db: Session):
    return db.query(Asset).all()

