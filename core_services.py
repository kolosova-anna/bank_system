from __future__ import annotations
from core_interfaces import User, IUsersRepository, IOperationsRepository, IUnitOfWork
import re


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def registration(self, login: str, password: str) -> int | None:
        try:
            with self.uow:
                check_login = self.check_user_availibility(login)
                if not check_login:
                    check_password = self.check_new_password(password)
                    if check_password:
                        user_id = self.uow.users_repo.registration(login, password)
                        if user_id is not None:
                            self.create_account(user_id)
                            return user_id
                        raise BankException('Unexpected error')
                    raise BankException('The password must be at least 8 characters long and '\
                                    'contain uppercase and lowercase letters, numbers, and symbols.')
                raise BankException('This username is already taken')
                return
        except BankException as e:
            print(e)
            return
    
    def create_account(self, user_id: int) -> int:
        return self.uow.users_repo.create_account(user_id)

    def autorization(self, login: str, password: str) -> int | None:
        try:
            res = self.uow.users_repo.autorization(login, password)
            if res is not None:
                return res
            BankException('There was a mistake in your login or password. Please, repeat')
        except BankException as e:
            print(e)
    
    def check_user_availibility(self, login: str) -> bool:
        return self.uow.users_repo.check_user_availibility(login)
     
    def check_new_password(self, password: str) -> bool:
        if (len(password) < 8 or
            not re.search(r'[a-z]', password) or
            not re.search(r'[A-Z]', password) or
            not re.search(r'[0-9]', password) or
            not re.search(r'[^a-zA-Z0-9]', password)):
            return False
        return True

class Operations:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_balance(self, user_id: int) -> float:
        balance = self.uow.ops_repo.get_balance(user_id)
        if balance is not None:
            return balance
        return 0
        
    def get_history(self, user_id: int) -> list | None:
        try:
            history = self.uow.ops_repo.get_history(user_id)
            if history:
                return history
            BankException('Error. Please, repeat')
        except BankException as e:
            print(e)
            return

    def withdraw_cash(self, user_id: int, sum: int) -> None:
        with self.uow:
            try:
                balance = self.uow.ops_repo.get_balance(user_id)
                if balance >= sum:
                    self.uow.ops_repo.withdraw_cash(user_id, sum)
                    op = 'withdrow cash'
                    self.record_changes(user_id, op, sum)
                    print(f'Withdrawn amount: {sum}')
                else:
                    raise BankException('Insufficient funds')
            except BankException as e:
                print(e)
                return

    def deposit_cash(self, user_id: int, sum: int) -> None:
        with self.uow:
            self.uow.ops_repo.deposit_cash(user_id, sum)
            op = 'deposit_cash'
            self.record_changes(user_id, op, sum)
            print(f'Deposited amount: {sum}')
  
    def record_changes(self, user_id: int, operation: str, sum: int) -> None:
        return self.uow.ops_repo.record_changes(user_id, operation, sum)
    
    def show_all_records(self, table: str) -> list | None:
        return self.uow.ops_repo.show_all_records(table)
    
''' def delete_record(self) -> None:
        return self.uow.ops_repo.delete_record()'''
    

class BankException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Error: {self.message}'