from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.post import SubjectPost
from app.models.comment import PostComment
from app.schemas.post import PostCreate
from app.schemas.comment import CommentCreate
from app.models.subject import Subject

from app.models.user import User

def get_posts_by_subject(db: Session, subject_id: int) -> list:
    results = db.query(
        SubjectPost,
        User.first_name,
        User.middle_name,
        User.last_name,
        Subject.name.label("subject_name")
    ).join(User, SubjectPost.author_id == User.id)\
     .join(Subject, SubjectPost.subject_id == Subject.id)\
     .filter(SubjectPost.subject_id == subject_id).all()

    output = []
    for post, fn, mn, ln, sname in results:
        post_data = {
            "id": post.id,
            "subject_id": post.subject_id,
            "subject_name": sname,
            "author_id": post.author_id,
            "first_name": fn,
            "middle_name": mn,
            "last_name": ln,
            "content": post.content,
            "created_at": post.created_at,
        }
        output.append(post_data)
    return output

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

def get_comments_by_post(db: Session, post_id: int) -> list:
    post = db.query(SubjectPost).filter(SubjectPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    results = db.query(
        PostComment,
        User.first_name,
        User.middle_name,
        User.last_name
    ).join(User, PostComment.author_id == User.id)\
     .filter(PostComment.post_id == post_id).all()

    output = []
    for comment, fn, mn, ln in results:
        comment_data = {
            "id": comment.id,
            "post_id": comment.post_id,
            "author_id": comment.author_id,
            "first_name": fn,
            "middle_name": mn,
            "last_name": ln,
            "content": comment.content,
            "created_at": comment.created_at,
        }
        output.append(comment_data)
    return output

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