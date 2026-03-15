from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.routers.todos import router as todos_router

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Hello To-Do"}


app.include_router(todos_router, prefix="/api/v1")
