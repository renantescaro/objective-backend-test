from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from app.domain.models.database import (
    base as Base,
    select,
    insert,
    delete,
    update,
    engine,
    and_,
)
from app.service.enum.payment_method_enum import PaymentMethod
from app.service.enum.transaction_kind_enum import TransactionKind
from app.service.helper.log import Log


class TransactionModel(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, unique=False, index=False)
    payment_method = Column(Enum(PaymentMethod), unique=False, index=False)
    transaction_kind = Column(Enum(TransactionKind), unique=False, index=False)
    account_id = Column(Integer, ForeignKey("account.id"))
    timestamp = Column(Integer, unique=False, index=False)

    @staticmethod
    def select(
        id: Optional[int] = None,
        payment_method: Optional[PaymentMethod] = None,
        transaction_kind: Optional[TransactionKind] = None,
        account_id: Optional[int] = None,
    ):
        connection = engine.connect()
        try:
            conditions = []
            if id:
                conditions.append(TransactionModel.id == id)

            if payment_method:
                conditions.append(TransactionModel.payment_method == payment_method)

            if transaction_kind:
                conditions.append(TransactionModel.transaction_kind == transaction_kind)

            if account_id:
                conditions.append(TransactionModel.account_id == account_id)

            query = select(TransactionModel).filter(and_(*conditions))

            return connection.execute(query).fetchone()

        except Exception as error:
            Log.error("transaction_model.select: ", error)
            return None

        finally:
            connection.close()
            engine.dispose()

    @staticmethod
    def insert(
        account_id: int,
        amount: float,
        timestamp: int,
        transaction_kind: Optional[TransactionKind],
        payment_method: Optional[PaymentMethod] = None,
    ):
        connection = engine.connect()
        try:
            stmt = insert(TransactionModel).values(
                payment_method=payment_method,
                transaction_kind=transaction_kind,
                account_id=account_id,
                amount=amount,
                timestamp=timestamp,
            )
            result = connection.execute(stmt)
            return result.inserted_primary_key[0]

        except Exception as error:
            Log.error("transaction_model.insert: ", error)
            return None

        finally:
            connection.commit()
            connection.close()
            engine.dispose()

    @staticmethod
    def delete(
        id: int,
    ) -> bool:
        connection = engine.connect()
        try:
            query = delete(TransactionModel).where(
                TransactionModel.id == id,
            )
            connection.execute(query)
            return True

        except Exception as error:
            Log.error("transaction_model.delete: ", error)
            return False

        finally:
            connection.commit()
            connection.close()
            engine.dispose()

    @staticmethod
    def update(
        id: int,
        amount: Optional[float] = None,
        payment_method: Optional[PaymentMethod] = None,
        transaction_kind: Optional[TransactionKind] = None,
    ):
        connection = engine.connect()
        try:
            values = {}
            if amount:
                values["amount"] = amount

            if payment_method:
                values["payment_method"] = payment_method

            if transaction_kind:
                values["transaction_kind"] = transaction_kind

            stmt = (
                update(TransactionModel)
                .values(values)
                .where(
                    TransactionModel.id == id,
                )
            )
            connection.execute(stmt)
            return True

        except Exception as error:
            Log.error("transaction_model.update: ", error)
            return False

        finally:
            connection.commit()
            connection.close()
            engine.dispose()
