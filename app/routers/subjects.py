from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectOut
from app.services.subject_service import get_all_subjects, get_subject_by_id, create_subject, update_subject, delete_subject
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return get_all_subjects(db)

@router.get("/{subject_id}", response_model=SubjectOut)
def retrieve_subject(subject_id: int, db: Session = Depends(get_db)):
    return get_subject_by_id(db, subject_id)

@router.post("/", response_model=SubjectOut)
def create(data: SubjectCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администратора")
    return create_subject(db, data)

@router.patch("/{subject_id}", response_model=SubjectOut)
def update(subject_id: int, data: SubjectUpdate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="Доступ только для администратора или преподавателя")
    return update_subject(db, subject_id, data)

@router.delete("/{subject_id}", status_code=204)
def delete(subject_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администратора")
    delete_subject(db, subject_id)