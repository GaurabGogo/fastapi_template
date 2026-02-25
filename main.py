from src.app import app
from src.config.app_config import getAppConfig

if __name__ == "__main__":
    import uvicorn
    config = getAppConfig()
    uvicorn.run(app, host=config.app_host, port=config.app_port)
