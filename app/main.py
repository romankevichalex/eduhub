import subprocess
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routers import auth, subjects, enrollments, posts, chat, materials, admin

from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="EduHub Backend",
    description="",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    subprocess.run(["alembic", "upgrade", "head"])

@app.get("/")
@app.get("/login")
@app.get("/subjects/{p:path}")
@app.get("/register")
@app.get("/settings")
async def serve_index():
    static_path = os.getenv("STATIC_FILES_DIR", "static")
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "message": "FastAPI backend is running!"}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(subjects.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(materials.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/health_check")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend is running!"}

static_path = os.getenv("STATIC_FILES_DIR", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

