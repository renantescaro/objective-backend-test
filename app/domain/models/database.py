import os
from sqlalchemy import (
    create_engine,
    MetaData,
    select,
    insert,
    delete,
    update,
    or_,
    and_,
)
from sqlalchemy.orm import declarative_base

metadata_obj = MetaData()
engine = create_engine(
    str(os.getenv("JAWSDB_MARIA_URL")),
)

base = declarative_base()
