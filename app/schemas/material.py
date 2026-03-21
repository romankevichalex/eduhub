from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MaterialCreate(BaseModel):
    subject_id: int
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: str

class MaterialOut(BaseModel):
    id: int
    subject_id: int
    teacher_id: int
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True