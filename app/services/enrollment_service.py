from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate

def enroll_student(db: Session, user_id: int, data: EnrollmentCreate) -> Enrollment:
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.subject_id == data.subject_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Студент уже записан на этот предмет")
    enrollment = Enrollment(user_id=user_id, subject_id=data.subject_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

def get_enrollments(db: Session, user_id: int = None, subject_id: int = None) -> list[Enrollment]:
    query = db.query(Enrollment)
    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    if subject_id:
        query = query.filter(Enrollment.subject_id == subject_id)
    return query.all()

def delete_enrollment(db: Session, enrollment_id: int, user_id: int) -> None:
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if enrollment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой записи")
    db.delete(enrollment)
    db.commit()