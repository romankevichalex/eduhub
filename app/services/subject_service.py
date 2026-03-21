from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate

def get_all_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).all()

def get_subject_by_id(db: Session, subject_id: int) -> Subject:
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Предмет не найден")
    return subject

def create_subject(db: Session, data: SubjectCreate) -> Subject:
    existing = db.query(Subject).filter(Subject.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Предмет с таким кодом уже существует")
    subject = Subject(**data.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

def update_subject(db: Session, subject_id: int, data: SubjectUpdate) -> Subject:
    subject = get_subject_by_id(db, subject_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(subject, field, value)
    db.commit()
    db.refresh(subject)
    return subject

def delete_subject(db: Session, subject_id: int) -> None:
    subject = get_subject_by_id(db, subject_id)
    db.delete(subject)
    db.commit()