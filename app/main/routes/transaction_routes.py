from http import HTTPStatus
from fastapi import Response
from app.domain.models.account_model import AccountModel
from app.domain.models.fee_model import FeeModel
from app.domain.models.transaction_model import TransactionModel
from app.domain.usecases.transaction import (
    IncomingTransactionParams,
    TransactionNewParams,
)
from app.main.main import app
from app.service.usecase.transaction.transaction_incoming_post import (
    TransactionIncomingPost,
)
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
    body: TransactionNewParams,
    response: Response,
):
    result = TransactionPost(
        transaction_model=TransactionModel(),
        account_model=AccountModel(),
        fee_model=FeeModel(),
    ).execute(body)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response


@app.post(
    "/deposito",
    responses={
        HTTPStatus.CREATED.value: {
            "model": "",
            "description": "Depósito efetuado com sucesso",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Erro ao efetuar depósito",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["transacao"],
)
def incoming_transaction(
    body: IncomingTransactionParams,
    response: Response,
):
    result = TransactionIncomingPost(
        transaction_model=TransactionModel(),
        account_model=AccountModel(),
    ).execute(body)

    response.status_code = result.status_code
    if result.body:
        response.body = result.body
    return response
