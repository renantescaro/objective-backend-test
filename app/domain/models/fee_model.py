from sqlalchemy import Column, Integer, Enum, Float
from app.service.enum.payment_method_enum import PaymentMethod
from app.service.helper.log import Log
from app.domain.models.database import (
    base as Base,
    select,
    engine,
    and_,
)


class FeeModel(Base):
    __tablename__ = "fee"

    id = Column(Integer, primary_key=True, index=True)
    payment_method = Column(Enum(PaymentMethod), unique=False, index=False)
    amount = Column(Float, unique=False, index=False)

    @staticmethod
    def select(
        payment_method: PaymentMethod,
    ):
        connection = engine.connect()
        try:
            conditions = []
            conditions.append(FeeModel.payment_method == payment_method)

            query = select(FeeModel).filter(and_(*conditions))

            return connection.execute(query).fetchone()

        except Exception as error:
            Log.error("fee_model.select: ", error)
            return None

        finally:
            connection.close()
            engine.dispose()
