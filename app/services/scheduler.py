from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.config.db import SessionLocal
from app.modules.pm.service import get_due_pms, generate_workorder_from_pm


scheduler = BackgroundScheduler()


def run_pm_cycle():
    """
    Executes PM automation cycle:
    - finds due PMs
    - generates work orders
    - updates schedules
    """
    db: Session = SessionLocal()

    try:
        due_pms = get_due_pms(db)

        for pm in due_pms:
            generate_workorder_from_pm(db, pm)

        if due_pms:
            print(f"[SCHEDULER] Generated {len(due_pms)} PM work orders")

    finally:
        db.close()


def start_scheduler():
    """
    Start background scheduler once per app lifecycle.
    Runs every day at midnight.
    """
    if not scheduler.running:
        scheduler.add_job(run_pm_cycle, "cron", hour=0, minute=0)
        scheduler.start()
