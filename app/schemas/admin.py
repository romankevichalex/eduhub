from pydantic import BaseModel, EmailStr
from typing import Optional

class UserAdminOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    role: str
    is_verified: bool

    class Config:
        from_attributes = True

class AdminSubjectOut(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True