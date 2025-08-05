from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class User:
    user_id: int
    login: str
    password: str


@dataclass
class UserAccount:
    account_id: int
    user_id: int
    balance: float = 0


@dataclass
class History:
    op_id: int
    user_id: int
    date_time: str
    op_name: str
    sum: float


class IUnitOfWork(ABC):
    users_repo: IUsersRepository
    ops_repo: IOperationsRepository

    @abstractmethod
    def __enter__(self) -> IUnitOfWork:
        raise NotImplementedError
    
    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError


class IUsersRepository(ABC):
    '''Интерфейс для регистрации, авторизации и получения данных из кабинета пользователя'''
    @abstractmethod
    def registration(self, login: str, password: str) -> int | None:
        pass

    @abstractmethod
    def create_account(self, user_id: int) -> int:
        pass

    @abstractmethod
    def autorization(self, login: str, password: str) -> int | None:
        pass

    @abstractmethod
    def check_user_availibility(self, login: str) -> bool:
        pass

    @abstractmethod
    def check_new_password(self, password: str) -> bool:
        pass


class IOperationsRepository(ABC):
    '''Интерфейс для выполнения операций по счету'''
    @abstractmethod
    def get_balance(self, user_id: int) -> float:
        pass

    @abstractmethod
    def get_history(self, user_id: int) -> list | None:
        pass

    @abstractmethod
    def withdraw_cash(self, user_id: int, sum: int) -> None:
        pass

    @abstractmethod
    def deposit_cash(self, user_id: int, sum: int) -> None:
        pass

    @abstractmethod
    def record_changes(self, user_id: int, operation: str, sum: int) -> None:
        pass

    @abstractmethod
    def show_all_records(self, table: str) -> list | None:
        pass
