from sqlalchemy import Column, Integer, String, Boolean
from app.config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)

    role = Column(String, nullable=False)  # admin, supervisor, technician
    is_active = Column(Boolean, default=True)
