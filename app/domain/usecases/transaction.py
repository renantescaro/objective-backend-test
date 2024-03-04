from pydantic import BaseModel, Field
from app.service.enum.payment_method_enum import PaymentMethod


class TransactionNewParams(BaseModel):
    payment_method: PaymentMethod = Field(alias="forma_pagamento")
    account_id: int = Field(alias="conta_id")
    amount: float = Field(alias="valor")


class IncomingTransactionParams(BaseModel):
    account_id: int = Field(alias="conta_id")
    amount: float = Field(alias="valor")
