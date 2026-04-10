from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat import ChatMessageCreate, ChatMessageOut, ChatHistory
from app.services.chat_service import send_message, get_history
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/messages", response_model=ChatMessageOut)
def post_message(data: ChatMessageCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    return send_message(db, user.id, data)

@router.get("/history", response_model=ChatHistory)
def chat_history(subject_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    messages = get_history(db, user.id, subject_id)
    return ChatHistory(messages=messages)