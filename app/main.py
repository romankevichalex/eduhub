import subprocess
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
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

static_path = os.getenv("STATIC_FILES_DIR", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):

    file_path = os.path.join(static_path, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"detail": "Not Found"}, 404

@app.get("/health_check")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend is running!"}