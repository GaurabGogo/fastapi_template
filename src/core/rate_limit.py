from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config.app_config import getAppConfig

config = getAppConfig()

# Initialize the limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[config.rate_limit_default]
)

def register_rate_limiting(app):
    """Register rate limit handlers and state."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
