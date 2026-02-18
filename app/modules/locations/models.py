# # app/modules/locations/models.py
# from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.config.db import Base

# class Level1Site(Base):
#     __tablename__ = "level1_sites"

#     id = Column(Integer, primary_key=True, index=True)
#     region_number = Column(Integer, nullable=False)
#     description = Column(String(200), nullable=False)
#     date_opened = Column(Date, nullable=True)

#     buildings = relationship("Level2Building", back_populates="site")


# class Level2Building(Base):
#     __tablename__ = "level2_buildings"

#     id = Column(Integer, primary_key=True, index=True)
#     level1_id = Column(Integer, ForeignKey("level1_sites.id"), nullable=False)

#     region_number = Column(Integer, nullable=False)
#     division_number = Column(Integer, nullable=False)

#     fm_number = Column(Integer, nullable=True)
#     building_name = Column(String(150), nullable=False)

#     date_opened = Column(Date, nullable=True)
#     date_closed = Column(Date, nullable=True)

#     address = Column(String(200), nullable=True)
#     scity = Column(String(100), nullable=True)
#     state = Column(String(50), nullable=True)
#     postal_code = Column(String(20), nullable=True)

#     square_ft = Column(Integer, nullable=True)
#     time_zone = Column(String(50), nullable=True)
#     daylight_savings = Column(Boolean, default=False)
#     ship_country = Column(String(10), nullable=True)
#     status = Column(String(20), nullable=True)

#     site = relationship("Level1Site", back_populates="buildings")
#     floors = relationship("Level3Floor", back_populates="building")


# class Level3Floor(Base):
#     __tablename__ = "level3_floors"

#     id = Column(Integer, primary_key=True, index=True)
#     level2_id = Column(Integer, ForeignKey("level2_buildings.id"), nullable=False)

#     region_number = Column(Integer, nullable=False)
#     division_number = Column(Integer, nullable=False)
#     district_number = Column(Integer, nullable=False)

#     description = Column(String(200), nullable=False)
#     date_opened = Column(Date, nullable=True)
#     date_closed = Column(Date, nullable=True)

#     building = relationship("Level2Building", back_populates="floors")
#     rooms = relationship("Level4Room", back_populates="floor")


# class Level4Room(Base):
#     __tablename__ = "level4_rooms"

#     id = Column(Integer, primary_key=True, index=True)
#     level3_id = Column(Integer, ForeignKey("level3_floors.id"), nullable=False)

#     region_number = Column(Integer, nullable=False)
#     division_number = Column(Integer, nullable=False)
#     district_number = Column(Integer, nullable=False)

#     customer_site = Column(String(100), nullable=True)
#     customer_site_number = Column(Integer, nullable=True)

#     room_desc = Column(String(150), nullable=False)

#     ship_address = Column(String(200), nullable=True)
#     ship_city = Column(String(100), nullable=True)
#     ship_state = Column(String(50), nullable=True)
#     ship_postal = Column(String(20), nullable=True)
#     ship_country = Column(String(10), nullable=True)

#     date_opened = Column(Date, nullable=True)
#     date_closed = Column(Date, nullable=True)

#     floor = relationship("Level3Floor", back_populates="rooms")
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.db import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    parent_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # Self-referencing hierarchy
    parent = relationship("Location", remote_side=[id], backref="children")

    # Relationships
    assets = relationship("Asset", back_populates="location")
