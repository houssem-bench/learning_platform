from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

    static_dir = Path(__file__).resolve().parent.parent / "static"
    index_file = static_dir / "index.html"
    assets_dir = static_dir / "assets"

    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/", include_in_schema=False)
    def root():
        if index_file.is_file():
            return FileResponse(index_file)
        return {"status": "ok"}

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str):
        if not index_file.is_file():
            return {"detail": "Not Found"}
        file_path = static_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(index_file)

    return app


app = create_app()
