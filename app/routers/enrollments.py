from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.services.enrollment_service import enroll_student, get_enrollments, delete_enrollment
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=EnrollmentOut)
def enroll(data: EnrollmentCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    return enroll_student(db, user.id, data)

@router.get("/", response_model=list[EnrollmentOut])
def list_enrollments(user_id: Optional[int] = None, subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_enrollments(db, user_id, subject_id)

@router.delete("/{enrollment_id}", status_code=204)
def unenroll(enrollment_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    delete_enrollment(db, enrollment_id, user.id)