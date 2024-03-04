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
        HTTPStatus.CREATED.value: {
            "model": "",
            "description": "conta criada com sucesso",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "model": "",
            "description": "Não é possível utilizar esse número de conta",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Erro ao criar conta",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["conta"],
)
def create_account(
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
        HTTPStatus.NOT_FOUND.value: {
            "model": "",
            "description": "Conta não encontrada",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Internal Server Error",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["conta"],
)
def get_account_by_id(
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
