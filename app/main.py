from fastapi import FastAPI

from app.api.routes.reminders import router as reminders_router
from app.api.routes.services import router as services_router
from app.core.config import get_settings

tags_metadata = [
    {
        "name": "services",
        "description": (
            "Endpoints para cadastrar, atualizar, listar e remover servicos "
            "internos que a plataforma disponibiliza."
        ),
    },
    {
        "name": "reminders",
        "description": (
            "Job manual para verificar boletos em um XLSX e disparar alertas "
            "via WhatsApp (WAHA)."
        ),
    },
]


def create_app() -> FastAPI:
    """Initialize FastAPI application with configured routes and metadata."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_tags=tags_metadata,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )

    register_routers(app)
    register_root_route(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Attach routers grouped by domain."""
    settings = get_settings()
    app.include_router(
        services_router,
        prefix=f"{settings.api_prefix}/services",
        tags=["services"],
    )
    app.include_router(
        reminders_router,
        prefix=f"{settings.api_prefix}/reminders",
        tags=["reminders"],
    )


def register_root_route(app: FastAPI) -> None:
    """Expose a landing route that aponta para a documentacao."""
    settings = get_settings()

    @app.get("/", include_in_schema=False)
    def root() -> dict[str, str]:
        return {
            "message": "API Services operando.",
            "documentation": f"{settings.api_prefix}/docs",
            "openapi": f"{settings.api_prefix}/openapi.json",
        }


app = create_app()
