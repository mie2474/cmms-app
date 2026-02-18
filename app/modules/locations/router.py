# # app/modules/locations/router.py
# from fastapi import APIRouter, Depends, UploadFile, File
# from sqlalchemy.orm import Session
# from app.config.db import get_db
# from . import schemas, service
# from fastapi.responses import StreamingResponse


# router = APIRouter(prefix="/api/locations", tags=["locations"])

# # ---------- Level 1 ----------
# @router.post("/level1", response_model=schemas.Level1Read)
# def create_level1(data: schemas.Level1Create, db: Session = Depends(get_db)):
#     return service.create_level1(db, data)

# @router.get("/level1", response_model=list[schemas.Level1Read])
# def list_level1(db: Session = Depends(get_db)):
#     return service.get_level1_list(db)


# # ---------- Level 2 ----------
# @router.post("/level2", response_model=schemas.Level2Read)
# def create_level2(data: schemas.Level2Create, db: Session = Depends(get_db)):
#     return service.create_level2(db, data)

# @router.get("/level2", response_model=list[schemas.Level2Read])
# def list_level2(db: Session = Depends(get_db)):
#     return service.get_level2_list(db)


# # ---------- Level 3 ----------
# @router.post("/level3", response_model=schemas.Level3Read)
# def create_level3(data: schemas.Level3Create, db: Session = Depends(get_db)):
#     return service.create_level3(db, data)

# @router.get("/level3", response_model=list[schemas.Level3Read])
# def list_level3(building_id: int | None = None, db: Session = Depends(get_db)):
#     return service.get_level3_list(db, building_id)


# # ---------- Level 4 ----------
# @router.post("/level4", response_model=schemas.Level4Read)
# def create_level4(data: schemas.Level4Create, db: Session = Depends(get_db)):
#     return service.create_level4(db, data)

# @router.get("/level4", response_model=list[schemas.LocationHierarchyRow])
# def list_level4(floor_id: int | None = None, db: Session = Depends(get_db)):
#     return service.get_level4_list(db, floor_id)


# # ---------- Bulk Loading ----------

# @router.post("/bulk/level1")
# async def bulk_level1(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     return service.bulk_load_level1(file, db)

# @router.post("/bulk/level2")
# async def bulk_level2(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     return service.bulk_load_level2(file, db)

# @router.post("/bulk/level3")
# async def bulk_level3(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     return service.bulk_load_level3(file, db)

# @router.post("/bulk/level4")
# async def bulk_level4(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     return service.bulk_load_level4(file, db)

# # ---------- Templates (Excel headers only) ----------

# @router.get("/template/l1")
# def download_template_l1():
#     file_obj = service.generate_template_l1()
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level1_template.xlsx"},
#     )


# @router.get("/template/l2")
# def download_template_l2():
#     file_obj = service.generate_template_l2()
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level2_template.xlsx"},
#     )


# @router.get("/template/l3")
# def download_template_l3():
#     file_obj = service.generate_template_l3()
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level3_template.xlsx"},
#     )


# @router.get("/template/l4")
# def download_template_l4():
#     file_obj = service.generate_template_l4()
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level4_template.xlsx"},
#     )


# # ---------- Data exports (all rows, no internal IDs) ----------

# @router.get("/data/l1")
# def download_data_l1(db: Session = Depends(get_db)):
#     file_obj = service.export_data_l1(db)
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level1_data.xlsx"},
#     )


# @router.get("/data/l2")
# def download_data_l2(db: Session = Depends(get_db)):
#     file_obj = service.export_data_l2(db)
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level2_data.xlsx"},
#     )


# @router.get("/data/l3")
# def download_data_l3(db: Session = Depends(get_db)):
#     file_obj = service.export_data_l3(db)
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level3_data.xlsx"},
#     )


# @router.get("/data/l4")
# def download_data_l4(db: Session = Depends(get_db)):
#     file_obj = service.export_data_l4(db)
#     return StreamingResponse(
#         file_obj,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": "attachment; filename=level4_data.xlsx"},
#     )

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles

from . import service, schemas

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/", response_model=schemas.LocationRead)
def create_location(
    payload: schemas.LocationCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    return service.create_location(db, payload)


@router.patch("/{location_id}", response_model=schemas.LocationRead)
def update_location(
    location_id: int,
    payload: schemas.LocationUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    return service.update_location(db, location_id, payload)


@router.get("/{location_id}", response_model=schemas.LocationRead)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.get_location(db, location_id)


@router.get("/", response_model=list[schemas.LocationRead])
def list_all(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "supervisor", "technician")),
):
    return service.list_locations(db)


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    service.delete_location(db, location_id)
    return {"message": "Location deleted"}
