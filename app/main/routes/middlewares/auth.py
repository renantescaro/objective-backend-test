from typing import Any
from base64 import b64decode
from fastapi import Request
from http import HTTPStatus
from starlette.responses import JSONResponse
from app.main.main import app
from app.service.helper.environment import is_dev
from app.service.helper.log import Log


PUBLIC_PATHS = [
    {
        "path": "/docs",
        "method": ["GET"],
    },
    {
        "path": "/openapi.json",
        "method": ["GET"],
    },
    {
        "path": "/conta",
        "method": ["GET", "POST", "OPTIONS"],
    },
    {
        "path": "/transacao",
        "method": ["GET", "POST", "OPTIONS"],
    },
    {
        "path": "/deposito",
        "method": ["GET", "POST", "OPTIONS"],
    },
]


@staticmethod
def _is_valid_credentials(headers: Any, path: str) -> bool:
    try:
        type, credentials = str(headers.get("authorization")).split(" ")
        user_login, user_password = b64decode(credentials).decode().split(":")

        # check user and return bool

        return True

    except Exception as error:
        Log.error("auth._is_valid_credentials", error)
        return False


def _mount_unauthorized_payload() -> JSONResponse:
    return JSONResponse(
        content={"message": "Unauthorized"},
        status_code=HTTPStatus.UNAUTHORIZED,
    )


@staticmethod
@app.middleware("http")
async def auth(request: Request, call_next):
    path = request.get("path", "")
    method = request.get("method")

    # public routes
    for item in PUBLIC_PATHS:
        if path == item["path"] and method in item["method"]:
            return await call_next(request)

    # private routes
    if not _is_valid_credentials(request.headers, path):

        # tests with frontends
        if method == "OPTIONS" and is_dev():
            return await call_next(request)

        return _mount_unauthorized_payload()

    return await call_next(request)
