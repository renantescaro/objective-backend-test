from pydantic import BaseModel

# TODO: use field


class AccountNewParams(BaseModel):
    name: str
    account_number: str
    document: str
