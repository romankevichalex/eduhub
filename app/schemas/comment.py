from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True