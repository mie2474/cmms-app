# # app/modules/locations/service.py
# from sqlalchemy.orm import Session
# from datetime import date
# from fastapi import UploadFile
# import pandas as pd
# from math import isnan
# from io import BytesIO
# from openpyxl import Workbook


# from . import models, schemas


# # -------------------------
# # Helper for cleaning dates
# # -------------------------
# def clean_date(value):
#     """
#     Converts Excel NaN or empty cells into None so PostgreSQL DATE accepts it.
#     """
#     if value is None:
#         return None
#     if isinstance(value, float) and isnan(value):
#         return None
#     return value


# # ---------- Level 1 ----------
# def create_level1(db: Session, data: schemas.Level1Create) -> models.Level1Site:
#     obj = models.Level1Site(**data.dict())
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_level1_list(db: Session):
#     return db.query(models.Level1Site).order_by(models.Level1Site.description).all()


# # ---------- Level 2 ----------
# def create_level2(db: Session, data: schemas.Level2Create) -> models.Level2Building:
#     site = db.query(models.Level1Site).get(data.level1_id)

#     obj = models.Level2Building(
#         level1_id=data.level1_id,
#         region_number=site.region_number if site else 0,
#         division_number=data.division_number,
#         building_name=data.building_name,
#         address=data.address,
#         scity=data.scity,
#         state=data.state,
#         postal_code=data.postal_code,
#     )

#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_level2_list(db: Session):
#     return db.query(models.Level2Building).order_by(models.Level2Building.building_name).all()


# # ---------- Level 3 ----------
# def create_level3(db: Session, data: schemas.Level3Create) -> models.Level3Floor:
#     bldg = db.query(models.Level2Building).get(data.level2_id)

#     obj = models.Level3Floor(
#         level2_id=data.level2_id,
#         region_number=bldg.region_number if bldg else 0,
#         division_number=bldg.division_number if bldg else 0,
#         district_number=data.district_number,
#         description=data.description,
#         date_opened=data.date_opened,
#         date_closed=data.date_closed,
#     )

#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_level3_list(db: Session, building_id: int | None = None):
#     today = date.today()

#     q = db.query(models.Level3Floor).filter(
#         (models.Level3Floor.date_closed.is_(None)) |
#         (models.Level3Floor.date_closed > today)
#     )

#     if building_id:
#         q = q.filter(models.Level3Floor.level2_id == building_id)

#     return q.order_by(models.Level3Floor.description).all()


# # ---------- Level 4 ----------
# def create_level4(db: Session, data: schemas.Level4Create) -> models.Level4Room:
#     floor = db.query(models.Level3Floor).get(data.level3_id)

#     obj = models.Level4Room(
#         level3_id=data.level3_id,
#         region_number=floor.region_number if floor else 0,
#         division_number=floor.division_number if floor else 0,
#         district_number=floor.district_number if floor else 0,
#         customer_site=data.customer_site,
#         customer_site_number=data.customer_site_number,
#         room_desc=data.room_desc,
#         ship_address=data.ship_address,
#         ship_city=data.ship_city,
#         ship_state=data.ship_state,
#         ship_postal=data.ship_postal,
#         ship_country=data.ship_country,
#     )

#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_level4_list(db: Session, floor_id: int | None = None):
#     q = (
#         db.query(
#             models.Level4Room,
#             models.Level3Floor,
#             models.Level2Building,
#         )
#         .join(models.Level3Floor, models.Level4Room.level3_id == models.Level3Floor.id)
#         .join(models.Level2Building, models.Level3Floor.level2_id == models.Level2Building.id)
#     )

#     if floor_id:
#         q = q.filter(models.Level4Room.level3_id == floor_id)

#     rows = []
#     for room, floor, bldg in q.all():
#         rows.append(
#             schemas.LocationHierarchyRow(
#                 id=room.id,
#                 region_number=room.region_number,
#                 building_name=bldg.building_name,
#                 floor_description=floor.description,
#                 room_desc=room.room_desc,
#                 customer_site=room.customer_site,
#                 customer_site_number=room.customer_site_number,
#             )
#         )
#     return rows


# # ---------- Bulk Loader ----------

# def clean_date(value):
#     if value is None:
#         return None
#     if isinstance(value, float) and isnan(value):
#         return None
#     return value

# # ---------- BULK LEVEL 1 (Regions) ----------
# def bulk_load_level1(file: UploadFile, db: Session):
#     df = pd.read_excel(file.file)

#     required_cols = ["Region_Number", "Region_Description", "Region_Date_Opened"]
#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")

#     rows_created = 0

#     for _, row in df.iterrows():
#         region = (
#             db.query(models.Level1Site)
#             .filter(models.Level1Site.region_number == row["Region_Number"])
#             .first()
#         )

#         if not region:
#             region = models.Level1Site(
#                 region_number=row["Region_Number"],
#                 description=row["Region_Description"],
#                 date_opened=clean_date(row["Region_Date_Opened"]),
#             )
#             db.add(region)
#             db.commit()
#             db.refresh(region)
#             rows_created += 1

#     return {"status": "success", "rows_processed": rows_created}


# # ---------- BULK LEVEL 2 (Buildings) ----------
# def bulk_load_level2(file: UploadFile, db: Session):
#     df = pd.read_excel(file.file)

#     required_cols = [
#         "Region_Number",
#         "Division_Number",
#         "Building_Name",
#         "Building_Address",
#         "Building_City",
#         "Building_State",
#         "Building_Postal",
#     ]
#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")

#     rows_created = 0

#     for _, row in df.iterrows():
#         region = (
#             db.query(models.Level1Site)
#             .filter(models.Level1Site.region_number == row["Region_Number"])
#             .first()
#         )
#         if not region:
#             # optionally skip or create region; here we create it minimally
#             region = models.Level1Site(
#                 region_number=row["Region_Number"],
#                 description=f"Region {row['Region_Number']}",
#                 date_opened=None,
#             )
#             db.add(region)
#             db.commit()
#             db.refresh(region)

#         building = (
#             db.query(models.Level2Building)
#             .filter(
#                 models.Level2Building.building_name == row["Building_Name"],
#                 models.Level2Building.level1_id == region.id,
#             )
#             .first()
#         )

#         if not building:
#             building = models.Level2Building(
#                 level1_id=region.id,
#                 region_number=region.region_number,
#                 division_number=row["Division_Number"],
#                 building_name=row["Building_Name"],
#                 address=row["Building_Address"],
#                 scity=row["Building_City"],
#                 state=row["Building_State"],
#                 postal_code=row["Building_Postal"],
#             )
#             db.add(building)
#             db.commit()
#             db.refresh(building)
#             rows_created += 1

#     return {"status": "success", "rows_processed": rows_created}


# # ---------- BULK LEVEL 3 (Floors) ----------
# def bulk_load_level3(file: UploadFile, db: Session):
#     df = pd.read_excel(file.file)

#     required_cols = [
#         "Building_Name",
#         "District_Number",
#         "Floor_Description",
#         "Floor_Date_Opened",
#         "Floor_Date_Closed",
#     ]
#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")

#     rows_created = 0

#     for _, row in df.iterrows():
#         building = (
#             db.query(models.Level2Building)
#             .filter(models.Level2Building.building_name == row["Building_Name"])
#             .first()
#         )
#         if not building:
#             # skip if building not found
#             continue

#         floor = (
#             db.query(models.Level3Floor)
#             .filter(
#                 models.Level3Floor.description == row["Floor_Description"],
#                 models.Level3Floor.level2_id == building.id,
#             )
#             .first()
#         )

#         if not floor:
#             floor = models.Level3Floor(
#                 level2_id=building.id,
#                 region_number=building.region_number,
#                 division_number=building.division_number,
#                 district_number=row["District_Number"],
#                 description=row["Floor_Description"],
#                 date_opened=clean_date(row["Floor_Date_Opened"]),
#                 date_closed=clean_date(row["Floor_Date_Closed"]),
#             )
#             db.add(floor)
#             db.commit()
#             db.refresh(floor)
#             rows_created += 1

#     return {"status": "success", "rows_processed": rows_created}


# # ---------- BULK LEVEL 4 (Rooms) ----------
# def bulk_load_level4(file: UploadFile, db: Session):
#     df = pd.read_excel(file.file)

#     required_cols = [
#         "Floor_Description",
#         "Customer_Site",
#         "Customer_Site_Number",
#         "Room_Description",
#         "Ship_Address",
#         "Ship_City",
#         "Ship_State",
#         "Ship_Postal",
#         "Ship_Country",
#     ]
#     for col in required_cols:
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")

#     rows_created = 0

#     for _, row in df.iterrows():
#         floor = (
#             db.query(models.Level3Floor)
#             .filter(models.Level3Floor.description == row["Floor_Description"])
#             .first()
#         )
#         if not floor:
#             # skip if floor not found
#             continue

#         room = models.Level4Room(
#             level3_id=floor.id,
#             region_number=floor.region_number,
#             division_number=floor.division_number,
#             district_number=floor.district_number,
#             customer_site=row["Customer_Site"],
#             customer_site_number=row["Customer_Site_Number"],
#             room_desc=row["Room_Description"],
#             ship_address=row["Ship_Address"],
#             ship_city=row["Ship_City"],
#             ship_state=row["Ship_State"],
#             ship_postal=row["Ship_Postal"],
#             ship_country=row["Ship_Country"],
#         )

#         db.add(room)
#         db.commit()
#         rows_created += 1

#     return {"status": "success", "rows_processed": rows_created}

# # ---------- Excel helpers ----------

# def _workbook_to_bytes(wb: Workbook) -> BytesIO:
#     bio = BytesIO()
#     wb.save(bio)
#     bio.seek(0)
#     return bio


# # ---------- Templates (headers only) ----------

# def generate_template_l1() -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level1_Region"

#     headers = [
#         "region_number",
#         "description",
#         "date_opened",
#     ]
#     ws.append(headers)

#     return _workbook_to_bytes(wb)


# def generate_template_l2() -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level2_Building"

#     headers = [
#         "level1_id",
#         "region_number",
#         "division_number",
#         "fm_number",
#         "building_name",
#         "date_opened",
#         "date_closed",
#         "address",
#         "scity",
#         "state",
#         "postal_code",
#         "square_ft",
#         "time_zone",
#         "daylight_savings",
#         "ship_country",
#         "status",
#     ]
#     ws.append(headers)

#     return _workbook_to_bytes(wb)


# def generate_template_l3() -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level3_Floor"

#     headers = [
#         "level2_id",
#         "region_number",
#         "division_number",
#         "district_number",
#         "description",
#         "date_opened",
#         "date_closed",
#     ]
#     ws.append(headers)

#     return _workbook_to_bytes(wb)


# def generate_template_l4() -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level4_Room"

#     headers = [
#         "level3_id",
#         "region_number",
#         "division_number",
#         "district_number",
#         "customer_site",
#         "customer_site_number",
#         "room_desc",
#         "ship_address",
#         "ship_city",
#         "ship_state",
#         "ship_postal",
#         "ship_country",
#         "date_opened",
#         "date_closed",
#     ]
#     ws.append(headers)

#     return _workbook_to_bytes(wb)


# # ---------- Data exports (all rows, no internal IDs) ----------

# def export_data_l1(db: Session) -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level1_Region"

#     headers = [
#         "region_number",
#         "description",
#         "date_opened",
#     ]
#     ws.append(headers)

#     rows = db.query(models.Level1Site).order_by(models.Level1Site.description).all()
#     for r in rows:
#         ws.append([
#             r.region_number,
#             r.description,
#             r.date_opened,
#         ])

#     return _workbook_to_bytes(wb)


# def export_data_l2(db: Session) -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level2_Building"

#     headers = [
#         "level1_id",
#         "region_number",
#         "division_number",
#         "fm_number",
#         "building_name",
#         "date_opened",
#         "date_closed",
#         "address",
#         "scity",
#         "state",
#         "postal_code",
#         "square_ft",
#         "time_zone",
#         "daylight_savings",
#         "ship_country",
#         "status",
#     ]
#     ws.append(headers)

#     rows = db.query(models.Level2Building).order_by(models.Level2Building.building_name).all()
#     for b in rows:
#         ws.append([
#             b.level1_id,
#             b.region_number,
#             b.division_number,
#             getattr(b, "fm_number", None),
#             b.building_name,
#             getattr(b, "date_opened", None),
#             getattr(b, "date_closed", None),
#             b.address,
#             b.scity,
#             b.state,
#             b.postal_code,
#             getattr(b, "square_ft", None),
#             getattr(b, "time_zone", None),
#             getattr(b, "daylight_savings", None),
#             getattr(b, "ship_country", None),
#             getattr(b, "status", None),
#         ])

#     return _workbook_to_bytes(wb)


# def export_data_l3(db: Session) -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level3_Floor"

#     headers = [
#         "level2_id",
#         "region_number",
#         "division_number",
#         "district_number",
#         "description",
#         "date_opened",
#         "date_closed",
#     ]
#     ws.append(headers)

#     rows = db.query(models.Level3Floor).order_by(models.Level3Floor.description).all()
#     for f in rows:
#         ws.append([
#             f.level2_id,
#             f.region_number,
#             f.division_number,
#             f.district_number,
#             f.description,
#             f.date_opened,
#             f.date_closed,
#         ])

#     return _workbook_to_bytes(wb)


# def export_data_l4(db: Session) -> BytesIO:
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Level4_Room"

#     headers = [
#         "level3_id",
#         "region_number",
#         "division_number",
#         "district_number",
#         "customer_site",
#         "customer_site_number",
#         "room_desc",
#         "ship_address",
#         "ship_city",
#         "ship_state",
#         "ship_postal",
#         "ship_country",
#         "date_opened",
#         "date_closed",
#     ]
#     ws.append(headers)

#     rows = db.query(models.Level4Room).order_by(models.Level4Room.room_desc).all()
#     for r in rows:
#         ws.append([
#             r.level3_id,
#             r.region_number,
#             r.division_number,
#             r.district_number,
#             r.customer_site,
#             r.customer_site_number,
#             r.room_desc,
#             r.ship_address,
#             r.ship_city,
#             r.ship_state,
#             r.ship_postal,
#             r.ship_country,
#             getattr(r, "date_opened", None),
#             getattr(r, "date_closed", None),
#         ])

#     return _workbook_to_bytes(wb)

from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Location


def create_location(db: Session, data):
    # validate parent exists
    if data.parent_id:
        parent = db.get(Location, data.parent_id)
        if not parent:
            raise HTTPException(404, "Parent location not found")

    location = Location(**data.dict())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location_id: int, data):
    location = db.get(Location, location_id)
    if not location:
        raise HTTPException(404, "Location not found")

    # prevent circular hierarchy
    if data.parent_id == location_id:
        raise HTTPException(400, "Location cannot be its own parent")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)
    return location


def get_location(db: Session, location_id: int):
    location = db.get(Location, location_id)
    if not location:
        raise HTTPException(404, "Location not found")
    return location


def list_locations(db: Session):
    return db.query(Location).all()


def delete_location(db: Session, location_id: int):
    location = db.get(Location, location_id)
    if not location:
        raise HTTPException(404, "Location not found")

    if location.children:
        raise HTTPException(400, "Cannot delete location with child locations")

    if location.assets:
        raise HTTPException(400, "Cannot delete location with assets")

    db.delete(location)
    db.commit()

