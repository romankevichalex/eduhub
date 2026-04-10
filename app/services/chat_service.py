from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.chat import ChatMessage
from app.schemas.chat import ChatMessageCreate

MODEL_NAME = "stub"

def send_message(db: Session, user_id: int, data: ChatMessageCreate) -> ChatMessage:
    user_message = ChatMessage(
        subject_id=data.subject_id,
        user_id=user_id,
        role="user",
        content=data.message,
        model_name=MODEL_NAME,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    assistant_reply = f"Заглушка: вы спросили '{data.message}'"

    assistant_message = ChatMessage(
        subject_id=data.subject_id,
        user_id=user_id,
        role="assistant",
        content=assistant_reply,
        model_name=MODEL_NAME,
        created_at=datetime.now(timezone.utc)
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return assistant_message

def get_history(db: Session, user_id: int, subject_id: int) -> list[ChatMessage]:
    return db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id,
        ChatMessage.subject_id == subject_id
    ).order_by(ChatMessage.created_at).all()