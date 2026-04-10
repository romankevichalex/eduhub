from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserCreate, UserOut, Token
from app.services.auth_service import register_user, login_user, get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, data)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, data.email, data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.removeprefix("Bearer ")
    return get_current_user(db, token)
