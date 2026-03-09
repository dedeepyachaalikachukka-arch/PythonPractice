from fastapi import FastAPI

from app.api.routes import analytics, health, streams, violations
from app.core.config import settings
from app.db.session import init_db


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)
    init_db()
    app.include_router(health.router)
    app.include_router(streams.router, prefix="/streams", tags=["streams"])
    app.include_router(violations.router, prefix="/violations", tags=["violations"])
    app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
    return app


app = create_app()
