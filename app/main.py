# app/main.py

from fastapi import FastAPI, Depends


app = FastAPI(
    title="eduhub",
    description="",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": ""}

