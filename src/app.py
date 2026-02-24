from fastapi import FastAPI, Depends
from src.routing import  user
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.config.app_config import getAppConfig

app = FastAPI()

# Include all routes
app.include_router(user.router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {}
    for error in exc.errors():
        print(f"The error is: {error}")
        errors[error["loc"][-1]] = error["msg"]

    return JSONResponse(
        {"message": "Validation Error", "errors": errors}, status_code=422
    )


@app.get("/")
def root():
    config = getAppConfig()
    return {
        "message": "Hello, Traveller",
        "app_name": config.app_name,
        "app_env": config.app_env,
        "database_url": config.database_url,
    }
