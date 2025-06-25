from fastapi import FastAPI
from src.app.api import v1
from src.app.api import admin


def create_app() -> FastAPI:
    app = FastAPI(title="Codex")

    app.include_router(v1.domains.router, prefix="/api/v1")
    app.include_router(v1.assets.router, prefix="/api/v1")
    app.include_router(v1.categories.router, prefix="/api/v1")
    app.include_router(v1.users.router, prefix="/api/v1")
    app.include_router(v1.queries.router, prefix="/api/v1")

    app.include_router(admin.users.router, prefix="/admin/v1")
    app.include_router(admin.assets.router, prefix="/admin/v1")
    app.include_router(admin.domains.router, prefix="/admin/v1")
    app.include_router(admin.categories.router, prefix="/admin/v1")
    app.include_router(admin.audit.router, prefix="/admin/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
