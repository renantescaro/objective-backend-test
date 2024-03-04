from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.domain.models.database import (
    base as Base,
    select,
    insert,
    delete,
    update,
    engine,
    and_,
)
from app.service.helper.log import Log


class AccountModel(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=False, index=False)
    account_number = Column(String(9), unique=True, index=False)
    document = Column(String(20), unique=True, index=False)
    amount = Column(Float, unique=False, index=False, default=0)

    @staticmethod
    def select(
        id: Optional[int] = None,
        account_number: Optional[str] = None,
        document: Optional[str] = None,
    ):
        connection = engine.connect()
        try:
            conditions = []
            if id:
                conditions.append(AccountModel.id == id)

            if account_number:
                conditions.append(AccountModel.account_number == account_number)

            if document:
                conditions.append(AccountModel.document == document)

            query = select(AccountModel).filter(and_(*conditions))

            return connection.execute(query).fetchone()

        except Exception as error:
            Log.error("account_model.select: ", error)
            return None

        finally:
            connection.close()
            engine.dispose()

    @staticmethod
    def insert(
        name: str,
        document: str,
        account_number: str,
        amount: float,
    ):
        connection = engine.connect()
        try:
            stmt = insert(AccountModel).values(
                name=name,
                account_number=account_number,
                document=document,
                amount=amount,
            )
            result = connection.execute(stmt)
            return result.inserted_primary_key[0]

        except Exception as error:
            Log.error("account_model.insert: ", error)
            return None

        finally:
            connection.close()
            engine.dispose()

    @staticmethod
    def delete(
        id: int,
    ) -> bool:
        connection = engine.connect()
        try:
            query = delete(AccountModel).where(
                AccountModel.id == id,
            )
            connection.execute(query)
            return True

        except Exception as error:
            Log.error("account_model.delete: ", error)
            return False

        finally:
            connection.close()
            engine.dispose()

    @staticmethod
    def update(
        id: int,
        amount: Optional[float] = None,
    ):
        connection = engine.connect()
        try:
            values = {}
            if amount:
                values["amount"] = amount

            stmt = (
                update(AccountModel)
                .values(values)
                .where(
                    AccountModel.id == id,
                )
            )
            connection.execute(stmt)
            return True

        except Exception as error:
            Log.error("account_model.update: ", error)
            return False

        finally:
            connection.close()
            engine.dispose()
