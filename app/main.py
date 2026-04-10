import subprocess
from fastapi import FastAPI
from app.routers import auth, subjects, enrollments, posts, chat, materials, admin

app = FastAPI(
    title="EduHub Backend",
    description="",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    subprocess.run(["alembic", "upgrade", "head"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI backend is running!"}

app.include_router(auth.router, prefix="/api/v1")
app.include_router(subjects.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(materials.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
