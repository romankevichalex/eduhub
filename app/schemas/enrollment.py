from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    subject_id: int

class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    subject_id: int
    subject_name: str | None = None

    class Config:
        from_attributes = True