import logging
import sys

from src.config.app_config import getAppConfig


def register_logging():
    config = getAppConfig()
    
    # Define logging format
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
    )
    
    # Configure root logger
    logging.basicConfig(
        level=config.log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True # Force override any existing configuration
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    
    logger = logging.getLogger(__name__)
    level_name = logging.getLevelName(config.log_level)
    logger.info(f"Logging initialized at level: {level_name}")
