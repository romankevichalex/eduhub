from fastapi import FastAPI

app = FastAPI(
    title="EduHub backend",
    description="",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "FastAPI backend is running!",
        "project": "EduHub",
    }
