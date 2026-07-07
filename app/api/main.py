from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.config.settings import ApiSettings
from app.api.routes import analizar, auth, external_analysis, health, reports


def create_app():
    api = FastAPI(title=ApiSettings.app_name)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=ApiSettings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api.include_router(health.router, prefix=ApiSettings.api_prefix)
    api.include_router(auth.router, prefix=ApiSettings.api_prefix)
    api.include_router(reports.router, prefix=ApiSettings.api_prefix)
    api.include_router(analizar.router)
    api.include_router(external_analysis.router)
    return api


app = create_app()
