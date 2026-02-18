from sqlalchemy import Column, Integer, DateTime, func


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
