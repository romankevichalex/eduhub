from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate


from app.models.user import User
from app.models.subject import Subject

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

def get_enrollments(db: Session, user_id: int = None, subject_id: int = None) -> list:
    query = db.query(
        Enrollment,
        User.first_name,
        User.middle_name,
        User.last_name,
        Subject.name.label("subject_name")
    ).join(User, Enrollment.user_id == User.id).join(Subject, Enrollment.subject_id == Subject.id)

    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    if subject_id:
        query = query.filter(Enrollment.subject_id == subject_id)

    results = query.all()
    output = []
    for enrollment, fn, mn, ln, sname in results:
        enrollment_data = {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "first_name": fn,
            "middle_name": mn,
            "last_name": ln,
            "subject_id": enrollment.subject_id,
            "subject_name": sname,
        }
        output.append(enrollment_data)
    return output 

def delete_enrollment(db: Session, enrollment_id: int, user_id: int) -> None:
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if enrollment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа к этой записи")
    db.delete(enrollment)
    db.commit()