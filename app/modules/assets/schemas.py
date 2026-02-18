# from pydantic import BaseModel
# from typing import Optional


# class AssetBase(BaseModel):
#     name: str
#     code: Optional[str] = None
#     location_id: Optional[str] = None
#     category: Optional[str] = None
#     status: Optional[str] = None


# class AssetCreate(AssetBase):
#     pass


# class AssetUpdate(BaseModel):
#     name: Optional[str] = None
#     code: Optional[str] = None
#     location_id: Optional[str] = None
#     category: Optional[str] = None
#     status: Optional[str] = None


# class AssetOut(AssetBase):
#     id: str

#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from typing import Optional


class AssetBase(BaseModel):
    name: str
    asset_tag: str
    location_id: int


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    location_id: Optional[int] = None


class AssetRead(AssetBase):
    id: int
    status: str

    class Config:
        from_attributes = True
