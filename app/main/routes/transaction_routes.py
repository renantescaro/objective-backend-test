from http import HTTPStatus
from fastapi import Response, Request
from app.main.main import app
from app.service.usecase.transaction.transaction_post import TransactionPost


@app.get(
    "/transacao",
    responses={
        HTTPStatus.OK.value: {"model": "", "description": ""},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "model": "",
            "description": "Internal Server Error",
        },
    },
    status_code=HTTPStatus.OK,
    tags=["transacao"],
)
def transaction_new(
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
