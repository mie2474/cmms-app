from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.db import Base


class WorkOrder(Base):
    __tablename__ = "workorders"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String)

    status = Column(String, default="open")

    asset_id = Column(Integer, ForeignKey("assets.id"))
    priority_id = Column(Integer, ForeignKey("priority_codes.id"))
    problem_code_id = Column(Integer, ForeignKey("problem_codes.id"))

    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    # Relationships
    asset = relationship("Asset")
    priority = relationship("PriorityCode")
    problem_code = relationship("ProblemCode")
