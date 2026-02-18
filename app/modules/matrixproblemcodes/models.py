from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.config.db import Base


class MatrixProblemCode(Base):
    __tablename__ = "matrix_problem_codes"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    problem_code_id = Column(Integer, ForeignKey("problem_codes.id"), nullable=False)

    location = relationship("Location")
    problem_code = relationship("ProblemCode")

    __table_args__ = (
        UniqueConstraint("location_id", "problem_code_id", name="uix_location_problem"),
    )
