# TODO: add models account and transactions

from .database import engine, base

base.metadata.create_all(engine)
