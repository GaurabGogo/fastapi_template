import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.app_config import getAppConfig
from src.core.error_handlers import register_error_handlers
from src.core.logger import register_logging
from src.core.middleware import register_middleware
from src.core.rate_limit import register_rate_limiting
from src.users.controllers import user_controller

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up Travel App API...")
    # Initialize Logging for the lifespan
    register_logging()
    yield
    # Shutdown logic
    logger.info("Shutting down Travel App API...")

# Initialize Logging early
register_logging()

app = FastAPI(title="Travel App API", lifespan=lifespan)

# Register Rate Limiting
register_rate_limiting(app)

# Register Middleware (CORS, etc.)
register_middleware(app)

# Register Global Error Handlers
register_error_handlers(app)

# Include all routes
app.include_router(user_controller.router, prefix="/api")

@app.get("/")
async def root():
    config = getAppConfig()
    return {
        "message": "Hello, Traveller",
        "app_name": config.app_name,
        "app_env": config.app_env,
    }
