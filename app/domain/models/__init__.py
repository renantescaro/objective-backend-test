from .account_model import AccountModel
from .transaction_model import TransactionModel

from .database import engine, base

base.metadata.create_all(engine)
