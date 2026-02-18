from sqlalchemy.orm import Session
from .models import ProblemCode


def create_problemcodes(db: Session, data):
    problem = ProblemCode(**data.dict())
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def list_problem_codes(db: Session):
    return db.query(ProblemCode).all()
