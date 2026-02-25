from fastapi.middleware.cors import CORSMiddleware

from src.config.app_config import getAppConfig


def register_middleware(app):
    config = getAppConfig()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=config.allowed_methods,
        allow_headers=config.allowed_headers,
    )
