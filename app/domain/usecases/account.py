from pydantic import BaseModel


class AccountNewParams(BaseModel):
    name: str
    account_number: str
    document: str
