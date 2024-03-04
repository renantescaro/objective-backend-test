from http import HTTPStatus
from fastapi import Response, Request
from app.main.main import app
from app.service.usecase.transaction.transaction_post import TransactionPost


@app.post(
    "/transacao",
    responses={
        HTTPStatus.CREATED.value: {
            "model": "",
            "description": "Transação efetuada com sucesso",
        },
        HTTPStatus.NOT_FOUND.value: {
            "model": "",
            "description": "Saldo insuficiente",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Erro ao efetuar transação",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["transacao"],
)
def new_transaction(
    request: Request,
    response: Response,
):
    result = TransactionPost(
        transaction_model=None,
        account_model=None,
    ).execute(None)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response
