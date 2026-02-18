from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.config.db import Base


class PreventiveMaintenance(Base):
    __tablename__ = "preventive_maintenance"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    frequency = Column(String, nullable=False)  # daily, weekly, monthly
    interval = Column(Integer, default=1)       # every X days/weeks/months

    last_run_date = Column(Date, nullable=True)
    next_run_date = Column(Date, nullable=False)

    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)

    # Relationships
    asset = relationship("Asset")
