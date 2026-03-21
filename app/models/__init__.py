from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.subject import Subject
from app.models.enrollment import Enrollment
from app.models.post import SubjectPost
from app.models.comment import PostComment
from app.models.material import SubjectMaterial
from app.models.chat import ChatMessage