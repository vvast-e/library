from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.password import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Библиотекарь не найден")
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user
