import time
from json import dumps
from http import HTTPStatus
from app.domain.models.account_model import AccountModel
from app.domain.models.transaction_model import TransactionModel
from app.domain.usecases.transaction import TransactionNewParams
from app.service.enum.payment_method_enum import PaymentMethod
from app.service.enum.transaction_kind_enum import TransactionKind
from app.service.usecase.usecase import UsecaseReturn


class TransactionPost:
    def __init__(
        self,
        transaction_model: TransactionModel,
        account_model: AccountModel,
    ) -> None:
        self._transaction_model = transaction_model
        self._account_model = account_model

    def execute(
        self,
        params: TransactionNewParams,
    ) -> UsecaseReturn:
        try:
            # get account
            account = self._account_model.select(id=params.account_id)
            if not account:
                return UsecaseReturn(
                    status_code=HTTPStatus.BAD_REQUEST,
                    body="Conta não encontrada!",
                )

            # check financial funds
            if account.amount < params.amount:
                return UsecaseReturn(
                    status_code=HTTPStatus.NOT_FOUND,
                    body="Saldo insuficiente!",
                )

            # fee
            fee = 0
            if params.payment_method == PaymentMethod.DEBIT_CARD:
                fee = params.amount * 0.03

            if params.payment_method == PaymentMethod.CREDIT_CARD:
                fee = params.amount * 0.05

            total_value = account.amount - (params.amount + fee)

            # transactions
            transaction_inserted = self._transaction_model.insert(
                payment_method=params.payment_method,
                transaction_kind=TransactionKind.OUTPUT,
                account_id=account.id,
                amount=params.amount,
                timestamp=int(time.time()),
            )
            if not transaction_inserted:
                return UsecaseReturn(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

            account_update_status = self._account_model.update(
                id=account.id,
                amount=total_value,
            )
            if account_update_status:
                account_updated = self._account_model.select(id=params.account_id)
                return UsecaseReturn(
                    status_code=HTTPStatus.CREATED,
                    body=dumps(
                        {
                            "conta_id": account_updated.id,
                            "saldo": account_updated.amount,
                        }
                    ),
                )

            return UsecaseReturn(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            print(f"'TransactionPost' error in 'execute' {e}")
            return UsecaseReturn(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
