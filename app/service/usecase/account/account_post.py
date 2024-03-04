from json import dumps
from http import HTTPStatus
from app.domain.models.account_model import AccountModel
from app.domain.usecases.account import AccountNewParams
from app.service.usecase.usecase import Usecase, UsecaseReturn


class AccountPost:
    def __init__(
        self,
        account_model: AccountModel,
    ) -> None:
        self._account_model = account_model

    def execute(self, params: AccountNewParams) -> UsecaseReturn:
        try:
            # check account exist
            possible_account = self._account_model.select(
                account_number=params.account_number,
            )
            if possible_account:
                return UsecaseReturn(
                    status_code=HTTPStatus.BAD_REQUEST,
                    body="Não é possível utilizar esse número de conta!",
                )

            account_id = self._account_model.insert(
                name=params.name,
                document=params.document,
                account_number=params.account_number,
                amount=0,
            )

            if not account_id:
                return UsecaseReturn(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    body="Erro ao criar conta!",
                )

            return UsecaseReturn(
                status_code=HTTPStatus.OK,
                body=dumps(
                    {
                        "conta_id": account_id,
                        "saldo": 0,
                    }
                ),
            )

        except Exception as e:
            print(f"'AccountPost' error in 'execute' {e}")
            return UsecaseReturn(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
