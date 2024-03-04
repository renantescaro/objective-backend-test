from http import HTTPStatus
from fastapi import Response, Request
from app.domain.models.account_model import AccountModel
from app.domain.usecases.account import AccountNewParams
from app.main.main import app
from app.service.usecase.account.account_get import AccountGet
from app.service.usecase.account.account_post import AccountPost


@app.post(
    "/conta",
    responses={
        HTTPStatus.CREATED.value: {"model": "", "description": ""},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Internal Server Error",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["conta"],
)
def account_create(
    body: AccountNewParams,
    response: Response,
):
    result = AccountPost(
        account_model=AccountModel,
    ).execute(body)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response


@app.get(
    "/conta",
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
def account_get_by_id(
    id: int,
    request: Request,
    response: Response,
):
    result = AccountGet(
        account_model=AccountModel,
    ).execute(id)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response
