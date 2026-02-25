from fastapi import Response

from src.config.app_config import getAppConfig


def set_auth_cookie(response: Response, token: str) -> None:
    config = getAppConfig()
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=config.access_token_expire_minutes * 60,
        samesite="lax",
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
    )
