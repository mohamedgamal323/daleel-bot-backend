from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api import v1
from src.api import admin
from src.common.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    if settings.USE_MONGODB:
        from src.infrastructure_persistence.database.mongodb import connect_to_mongo, close_mongo_connection
        await connect_to_mongo()
    yield
    # Shutdown
    if settings.USE_MONGODB:
        await close_mongo_connection()


def create_app() -> FastAPI:
    app = FastAPI(title="Codex", lifespan=lifespan)

    app.include_router(v1.domain_controller.router, prefix="/api/v1")
    app.include_router(v1.asset_controller.router, prefix="/api/v1")
    app.include_router(v1.category_controller.router, prefix="/api/v1")
    app.include_router(v1.user_controller.router, prefix="/api/v1")
    app.include_router(v1.query_controller.router, prefix="/api/v1")
    app.include_router(v1.auth_controller.router, prefix="/api/v1")

    app.include_router(admin.user_controller.router, prefix="/admin/v1")
    app.include_router(admin.asset_controller.router, prefix="/admin/v1")
    app.include_router(admin.domain_controller.router, prefix="/admin/v1")
    app.include_router(admin.category_controller.router, prefix="/admin/v1")
    app.include_router(admin.audit_controller.router, prefix="/admin/v1")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app
