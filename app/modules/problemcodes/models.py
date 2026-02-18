from sqlalchemy import Column, Integer, String
from app.config.db import Base


class ProblemCode(Base):
    __tablename__ = "problem_codes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
