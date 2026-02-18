from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, data):
    if get_user_by_email(db, data.email):
        raise HTTPException(400, "User already exists")

    user = User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session):
    return db.query(User).all()
