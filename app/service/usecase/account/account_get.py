from json import dumps
from http import HTTPStatus
from typing import Any
from app.service.usecase.usecase import Usecase, UsecaseReturn


class AccountGet:
    def __init__(
        self,
        account_model: Any,
    ) -> None:
        self._account_model = account_model

    def execute(self, id: int) -> UsecaseReturn:
        try:
            # get account
            account = None
            # account = self._account_model.select()
            if not account:
                return UsecaseReturn(
                    status_code=HTTPStatus.NOT_FOUND,
                    body="Conta não encontrada!",
                )

            return UsecaseReturn(
                status_code=HTTPStatus.OK,
                body=dumps(
                    {
                        "conta_id": account.id,
                        "saldo": account.amount,
                    }
                ),
            )

        except Exception as e:
            print(f"'AccountGet' error in 'execute' {e}")
            return UsecaseReturn(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
