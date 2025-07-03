from dataclasses import dataclass
from abc import ABC, abstractmethod



@dataclass
class UserAccount:
    user_id: int
    login: str
    password: str
    balance: float = 0
    history: list = []


class IUsersRepository(ABC):
    '''Интерфейс для регистрации, авторизации и получения данных из кабинета пользователя'''

    @abstractmethod
    def registration(self, login: str, password: str) -> UserAccount:
        pass

    @abstractmethod
    def autorization(self, login: str, password: str) -> UserAccount:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserAccount:
        pass


class IOperations(ABC):
    '''Интерфейс для выполнения операций по счету'''

    @abstractmethod
    def get_balance(self, user_id: int) -> float:
        pass

    @abstractmethod
    def get_history(self, user_id: int) -> list:
        pass

    @abstractmethod
    def withdraw_cash(self, user_id: int, sum: int) -> None:
        pass

    @abstractmethod
    def up_user_balance(self, user_id: int, sum: int) -> None:
        pass
