from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: int
    subject_id: int
    subject_name: str | None = None
    author_id: int
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True