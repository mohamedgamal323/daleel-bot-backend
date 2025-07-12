from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
from src.backend.api import v1
from src.backend.api import admin
from src.backend.common.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = get_settings()
    if settings.USE_MONGODB:
        from src.backend.infrastructure_persistence.database.mongodb import connect_to_mongo, close_mongo_connection
        await connect_to_mongo()
    yield
    # Shutdown
    if settings.USE_MONGODB:
        await close_mongo_connection()


def create_app() -> FastAPI:
    app = FastAPI(title="Daleel Bot", lifespan=lifespan)

    # API routes
    app.include_router(v1.domain_controller.router, prefix="/api/v1")
    app.include_router(v1.asset_controller.router, prefix="/api/v1")
    app.include_router(v1.category_controller.router, prefix="/api/v1")
    app.include_router(v1.user_controller.router, prefix="/api/v1")
    app.include_router(v1.query_controller.router, prefix="/api/v1")
    app.include_router(v1.auth_controller.router, prefix="/api/v1")

    # Admin routes
    app.include_router(admin.user_controller.router, prefix="/admin/v1")
    app.include_router(admin.asset_controller.router, prefix="/admin/v1")
    app.include_router(admin.domain_controller.router, prefix="/admin/v1")
    app.include_router(admin.category_controller.router, prefix="/admin/v1")
    app.include_router(admin.audit_controller.router, prefix="/admin/v1")

    # Health check
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    # Serve static files (frontend build)
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=static_path), name="static")
        
        # Serve frontend for all non-API routes
        @app.get("/{path:path}")
        async def serve_frontend(path: str = ""):
            # Don't serve frontend for API routes
            if path.startswith("api/") or path.startswith("admin/") or path.startswith("docs") or path.startswith("redoc"):
                return {"error": "Not found"}
            
            # Serve index.html for all frontend routes
            index_path = static_path / "index.html"
            if index_path.exists():
                return FileResponse(index_path)
            
            return {"error": "Frontend not built"}

    return app


# Create the app instance for uvicorn
app = create_app()
