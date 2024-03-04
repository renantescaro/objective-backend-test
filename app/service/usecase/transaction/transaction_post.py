from json import dumps
from http import HTTPStatus
from typing import Any
from app.service.usecase.usecase import Usecase, UsecaseReturn


class TransactionPost:
    def __init__(
        self,
        transaction_model: Any,
        account_model: Any,
    ) -> None:
        self._transaction_model = transaction_model
        self._account_model = account_model

    def execute(self, params: Any) -> UsecaseReturn:
        try:
            # get account
            account = None
            # account = self._account_model.select()
            if not account:
                return UsecaseReturn(
                    status_code=HTTPStatus.BAD_REQUEST,
                    body="Conta não encontrada!",
                )

            if account.amount < params.amount:
                return UsecaseReturn(
                    status_code=HTTPStatus.NOT_FOUND,
                    body="Saldo insuficiente!",
                )

            return UsecaseReturn(
                status_code=HTTPStatus.CREATED,
                body=dumps(
                    {
                        "conta_id": account.id,
                        "saldo": account.amount,
                    }
                ),
            )

        except Exception as e:
            print(f"'TransactionPost' error in 'execute' {e}")
            return UsecaseReturn(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
