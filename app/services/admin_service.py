from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from app.models.user import User
from app.models.subject import Subject

def check_admin(user: User) -> None:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администратора")

def get_all_users(db: Session, role: Optional[str] = None) -> list[User]:
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()

def verify_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user

def get_all_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).all()