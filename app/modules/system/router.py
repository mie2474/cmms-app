from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.middleware.rbac import require_roles
from app.modules.pm.service import get_due_pms, generate_workorder_from_pm

router = APIRouter(prefix="/system", tags=["System"])


@router.post("/run-pm")
def run_pm_now(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    due_pms = get_due_pms(db)

    for pm in due_pms:
        generate_workorder_from_pm(db, pm)

    return {"generated_workorders": len(due_pms)}
