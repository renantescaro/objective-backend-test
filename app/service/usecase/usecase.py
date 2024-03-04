from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Optional


class UsecaseReturn:
    def __init__(self, status_code: HTTPStatus, body: Any = None):
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return f"UsecaseReturn (status_code={self.status_code}, body={self.body})"


class Usecase(ABC):
    @abstractmethod
    def execute(self, *args: Optional[Any]) -> UsecaseReturn:
        raise NotImplementedError('This contract method must be implemented')
