from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.post import SubjectPost
from app.models.comment import PostComment
from app.schemas.post import PostCreate
from app.schemas.comment import CommentCreate

def get_posts_by_subject(db: Session, subject_id: int) -> list[SubjectPost]:
    return db.query(SubjectPost).filter(SubjectPost.subject_id == subject_id).all()

def create_post(db: Session, subject_id: int, author_id: int, data: PostCreate) -> SubjectPost:
    post = SubjectPost(
        subject_id=subject_id,
        author_id=author_id,
        content=data.content,
        created_at=datetime.now(timezone.utc)
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_comments_by_post(db: Session, post_id: int) -> list[PostComment]:
    post = db.query(SubjectPost).filter(SubjectPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return db.query(PostComment).filter(PostComment.post_id == post_id).all()

def create_comment(db: Session, post_id: int, author_id: int, data: CommentCreate) -> PostComment:
    post = db.query(SubjectPost).filter(SubjectPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    comment = PostComment(
        post_id=post_id,
        author_id=author_id,
        content=data.content,
        created_at=datetime.now(timezone.utc)
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment