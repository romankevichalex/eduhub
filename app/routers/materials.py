from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.material import MaterialOut
from app.services.material_service import create_material, get_materials, delete_material, get_material_by_id
from app.services.auth_service import get_current_user
from app.services.storage_service import upload_file, delete_file

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/", response_model=MaterialOut)
async def upload_material(
        subject_id: int = Form(...),
        title: str = Form(...),
        description: Optional[str] = Form(None),
        file_type: str = Form(...),
        file: UploadFile = File(...),
        authorization: str = Header(...),
        db: Session = Depends(get_db)
):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Доступ только для преподавателя")

    file_bytes = await file.read()
    file_path = upload_file(file_bytes, file.filename, file.content_type)

    from app.schemas.material import MaterialCreate
    data = MaterialCreate(
        subject_id=subject_id,
        title=title,
        description=description,
        file_path=file_path,
        file_type=file_type
    )
    return create_material(db, user.id, data)


@router.get("/", response_model=list[MaterialOut])
def list_materials(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_materials(db, subject_id)


@router.get("/{material_id}", response_model=MaterialOut)
def get_material(material_id: int, db: Session = Depends(get_db)):
    return get_material_by_id(db, material_id)


@router.delete("/{material_id}", status_code=204)
def remove_material(material_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    material = get_material_by_id(db, material_id)
    delete_file(material.file_path)
    delete_material(db, material_id, user.id)