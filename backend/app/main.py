from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, attempts, auth, quizzes
from app.core.config import get_settings
from app.db.init_db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="Learning Platform API")

    settings = get_settings()
    cors_origins = [
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(quizzes.router)
    app.include_router(attempts.router)
    app.include_router(admin.router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    @app.get("/")
    def root() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
