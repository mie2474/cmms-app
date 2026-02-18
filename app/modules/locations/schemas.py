# app/modules/locations/schemas.py
from datetime import date
from pydantic import BaseModel

# ---------- Level 1 ----------
class Level1Base(BaseModel):
    region_number: int
    description: str
    date_opened: date | None = None
    
class Level1Create(Level1Base):
    pass

class Level1Read(Level1Base):
    id: int
    class Config:
        from_attributes = True


# ---------- Level 2 ----------
class Level2Base(BaseModel):
    level1_id: int
    division_number: int
    building_name: str
    address: str | None = None
    scity: str | None = None
    state: str | None = None
    postal_code: str | None = None

class Level2Create(Level2Base):
    pass

class Level2Read(Level2Base):
    id: int
    region_number: int
    class Config:
        from_attributes = True


# ---------- Level 3 ----------
class Level3Base(BaseModel):
    level2_id: int
    district_number: int
    description: str
    date_opened: date | None = None
    date_closed: date | None = None

class Level3Create(Level3Base):
    pass

class Level3Read(Level3Base):
    id: int
    region_number: int
    division_number: int
    class Config:
        from_attributes = True


# ---------- Level 4 ----------
class Level4Base(BaseModel):
    level3_id: int
    customer_site: str | None = None
    customer_site_number: int | None = None
    room_desc: str
    ship_address: str | None = None
    ship_city: str | None = None
    ship_state: str | None = None
    ship_postal: str | None = None
    ship_country: str | None = None

class Level4Create(Level4Base):
    pass

class Level4Read(Level4Base):
    id: int
    region_number: int
    division_number: int
    district_number: int
    class Config:
        from_attributes = True


# ---------- For hierarchy table ----------
# class LocationHierarchyRow(BaseModel):
#     id: int
#     region_number: int
#     building_name: str
#     floor_description: str
#     room_desc: str
#     customer_site: str | None = None
#     customer_site_number: int | None = None

#     class config:
#         from_attributes = True
from pydantic import BaseModel
from typing import Optional, List


class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class LocationRead(LocationBase):
    id: int

    class Config:
        from_attributes = True


class LocationTree(LocationRead):
    children: List["LocationTree"] = []
