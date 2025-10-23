from fastapi import FastAPI

from app.api.routes.services import router as services_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Initialize FastAPI application with configured routes."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Attach routers grouped by domain."""
    settings = get_settings()
    app.include_router(
        services_router,
        prefix=f"{settings.api_prefix}/services",
        tags=["services"],
    )


app = create_app()
