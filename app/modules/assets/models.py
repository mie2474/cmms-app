# import uuid
# from sqlalchemy import Column, String
# from app.config.db import Base


# class Asset(Base):
#     __tablename__ = "assets"

#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = Column(String, nullable=False)
#     code = Column(String, nullable=True)
#     location_id = Column(String, nullable=True)
#     category = Column(String, nullable=True)
#     status = Column(String, nullable=True)

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.db import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    asset_tag = Column(String, unique=True, nullable=False, index=True)

    status = Column(String, default="active", nullable=False)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # Relationships
    location = relationship("Location", back_populates="assets")
    workorders = relationship("WorkOrder", back_populates="asset")
