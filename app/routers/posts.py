from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.post import PostCreate, PostOut
from app.schemas.comment import CommentCreate, CommentOut
from app.services.post_service import get_posts_by_subject, create_post, get_comments_by_post, create_comment
from app.services.auth_service import get_current_user

router = APIRouter(tags=["posts"])

@router.get("/subjects/{subject_id}/posts", response_model=list[PostOut])
def list_posts(subject_id: int, db: Session = Depends(get_db)):
    return get_posts_by_subject(db, subject_id)

@router.post("/subjects/{subject_id}/posts", response_model=PostOut)
def add_post(subject_id: int, data: PostCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Доступ только для преподавателя")
    return create_post(db, subject_id, user.id, data)

@router.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return get_comments_by_post(db, post_id)

@router.post("/posts/{post_id}/comments", response_model=CommentOut)
def add_comment(post_id: int, data: CommentCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user = get_current_user(db, authorization.removeprefix("Bearer "))
    return create_comment(db, post_id, user.id, data)