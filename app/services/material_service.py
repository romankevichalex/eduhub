from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.material import SubjectMaterial
from app.schemas.material import MaterialCreate

def create_material(db: Session, teacher_id: int, data: MaterialCreate) -> SubjectMaterial:
    material = SubjectMaterial(
        subject_id=data.subject_id,
        teacher_id=teacher_id,
        title=data.title,
        description=data.description,
        file_path=data.file_path,
        file_type=data.file_type,
        created_at=datetime.now(timezone.utc)
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

def get_materials(db: Session, subject_id: int = None) -> list[SubjectMaterial]:
    query = db.query(SubjectMaterial)
    if subject_id:
        query = query.filter(SubjectMaterial.subject_id == subject_id)
    return query.all()

def get_material_by_id(db: Session, material_id: int) -> SubjectMaterial:
    material = db.query(SubjectMaterial).filter(SubjectMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    return material

def delete_material(db: Session, material_id: int, teacher_id: int) -> None:
    material = db.query(SubjectMaterial).filter(SubjectMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    if material.teacher_id != teacher_id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому материалу")
    db.delete(material)
    db.commit()