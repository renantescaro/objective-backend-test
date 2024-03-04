from http import HTTPStatus
from fastapi import Response, Request
from app.main.main import app
from app.service.usecase.account.account_get import AccountGet


@app.get(
    "/conta?id={id}",
    responses={
        HTTPStatus.OK.value: {"model": "", "description": ""},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Internal Server Error",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["conta"],
)
def account_get_by_id(id: int, request: Request, response: Response):
    result = AccountGet(
        account_model=None,
    ).execute(id)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response
