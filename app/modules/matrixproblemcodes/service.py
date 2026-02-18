from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import MatrixProblemCode


def create_mapping(db: Session, data):
    exists = db.query(MatrixProblemCode).filter_by(
        location_id=data.location_id,
        problem_code_id=data.problem_code_id
    ).first()

    if exists:
        raise HTTPException(400, "Mapping already exists")

    mapping = MatrixProblemCode(**data.dict())
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return mapping


def get_problem_codes_for_location(db: Session, location_id: int):
    return db.query(MatrixProblemCode).filter_by(
        location_id=location_id
    ).all()


def list_all(db: Session):
    return db.query(MatrixProblemCode).all()
