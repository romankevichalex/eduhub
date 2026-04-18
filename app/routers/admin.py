from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.admin import UserAdminOut, AdminSubjectOut
from app.services.admin_service import check_admin, get_all_users, verify_user, get_all_subjects, delete_user
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[UserAdminOut])
def list_users(role: Optional[str] = None, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    check_admin(user)
    return get_all_users(db, role)

@router.patch("/users/{user_id}/verify", response_model=UserAdminOut)
def verify(user_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    check_admin(user)
    return verify_user(db, user_id)

@router.delete("/users/{user_id}", status_code=204)
def delete(user_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    check_admin(user)
    delete_user(db, user_id)

@router.get("/subjects", response_model=list[AdminSubjectOut])
def list_subjects(authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    check_admin(user)
    return get_all_subjects(db)