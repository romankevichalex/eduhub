from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.material import MaterialCreate, MaterialOut
from app.services.material_service import create_material, get_materials, delete_material
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("/", response_model=MaterialOut)
def upload_material(data: MaterialCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Доступ только для преподавателя")
    return create_material(db, user.id, data)

@router.get("/", response_model=list[MaterialOut])
def list_materials(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_materials(db, subject_id)

@router.delete("/{material_id}", status_code=204)
def remove_material(material_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    delete_material(db, material_id, user.id)