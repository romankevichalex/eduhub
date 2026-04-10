from pydantic import BaseModel
from datetime import datetime

class ChatMessageCreate(BaseModel):
    subject_id: int
    message: str

class ChatMessageOut(BaseModel):
    id: int
    subject_id: int
    user_id: int
    role: str
    content: str
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    messages: list[ChatMessageOut]