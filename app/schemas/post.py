from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: int
    subject_id: int
    author_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True